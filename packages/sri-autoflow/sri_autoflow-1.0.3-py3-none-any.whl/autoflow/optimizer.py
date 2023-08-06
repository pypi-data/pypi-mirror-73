import copy
import logging
import math
import os
import os.path
import pickle
import sys
import shutil
import threading
import time
import traceback
from datetime import datetime
from threading import Lock

import d3m
import numpy.random
import pandas as pd
from d3m.base import utils as base_utils
from d3m.container import Dataset, DataFrame

# from d3m.container.dataset import D3MDatasetLoader
# from common_primitives.datamart_augment import Hyperparams as hyper_augment, DataMartAugmentPrimitive
# from common_primitives.datamart_download import Hyperparams as hyper_download, DataMartDownloadPrimitive
#
# from d3m.container.dataset import Dataset, D3MDatasetLoader
# from common_primitives.denormalize import Hyperparams as hyper_denormalize, DenormalizePrimitive
# import os
# from dsbox.datapreprocessing.cleaner.wikifier import WikifierHyperparams, Wikifier

from d3m.metadata import base as Base
from d3m.metadata.pipeline import PlaceholderStep
from d3m.runtime import Runtime

#TODO: Uncomment this and add the gama code base as a peer to 'autoflow' to get your local version of GAMA overlayed
#      on a Docker image
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(os.path.abspath('../gama'))
sys.path.append(os.path.abspath('../sri_tpot'))

from gama import GamaClassifier, GamaRegressor, GamaTimeSeriesForecaster, GamaTimeSeriesClassifier
from google.protobuf.timestamp_pb2 import Timestamp
from pathos.multiprocessing import ProcessPool

if os.getenv('TPOT') is not None:
    from sri_tpot import TPOTClassifier, TPOTRegressor

from sri.d3mglue.d3mwrap import D3MWrapper, TRANSFORMER_FAMILIES

from .config_converter import config_to_d3m
from .gama_classifier_config import classifier_config_dict
from .gama_regressor_config import regressor_config_dict
# There are two possible configurations for TSF, one that mixes in standard regressors, and one that
# uses only time series forecasting algorithms (pure).
import os
# When we are running outside of docker dont try to import problematic (difficult to install) primitives
if os.getenv('AUTOFLOW_WITH_NO_DOCKER') is None:
    from .gama_tsf_config import tsf_config_dict, tsf_config_dict_pure
else:
    from .gama_tsf_reduced_config import tsf_config_dict, tsf_config_dict_pure
from .nbest import NBest
from .pipeline import GraphPipeline, GamaPipeline, GamaEnsemblePipeline
from pipelines import find_pipeline_class
from pipelines.base import KEY_TYPES, DATETIME_TYPE, TARGET_TYPE, TRUE_TARGET_TYPE

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')

_logger = logging.getLogger(__name__)

gamalog = logging.getLogger('gama')
gamalog.setLevel(logging.INFO)


class UnfitException(Exception):
    pass


class AutoflowOptimizer(object):
    """
    Abstract base class for several optimization sub-problems, each of
    which is addressed separately through subclassing.
    """
    mutex = Lock()

    # List to manage active solution ids
    solution_ids = []

    # Keep track of which id is at which index
    solution_ids_to_index = {}
    solution_ids_to_predictions = {}

    # Initialize time
    _start_time = datetime.now()
    _logger.info("Start time has been set as initially: %s" %  _start_time)

    # Flag to ensure we dont generate these every single time a pipeline is exported
    considered_pipelines_generated = False

    @staticmethod
    def enable_pipeline_caching(enable):
        D3MWrapper.enable_cache(enable)

    def __init__(self, config=None):
        """
        We'll assume for the moment that constructing an optimizer does
        all the heavy lifting of reading the config file and
        remembering all the important info it contains.  We probably will
        want a class method to return the appropriate subclass based
        on the config contents, so top-level autoflow doesn't need to hold
        that logic.
        """
        self.config = config
        logging.info("Dataset Schema to be loaded is %s" % config.dataset_schema)
        if "http" not in config.dataset_schema:
            uri = "file://%s" % os.path.abspath(config.dataset_schema)
        else:
            # Open ML datasets are already fully formed.
            uri = config.dataset_schema
        _logger.info("Loading %s" % uri)
        self.dataset = Dataset.load(uri)

        # If the flag is set - load the Test Data to check the internal Gama scores
        self.test_dataset = None
        if self.config.use_test_dataset:
            # test_uri = "file://%s" % os.path.abspath(config.dataset_schema.replace("TRAIN", "TEST"))
            test_uri = "file://%s" % os.path.abspath(config.dataset_schema.replace("TRAIN", "SCORE", 1))
            test_uri = test_uri.replace("TRAIN", "TEST", 1)
            _logger.info("Loading Test Data %s" % test_uri)
            self.test_dataset = Dataset.load(test_uri)

        _logger.info("Dataset loaded")

        if self.config.enable_pipeline_caching():
            _logger.info("Pipeline caching enabled")
            self.enable_pipeline_caching(True)


    def _minutes_remaining(self):
        """
        Used to track how long we have been searching so we can stay beneath our allocated budget
        """
        minutes = self.config.timeout - ((datetime.now() - self._start_time).total_seconds() / 60)
        _logger.info("Minutes Remaining: %s" % minutes)
        return minutes


    def _initialize_start_time(self):
        _start_time = datetime.now()
        _logger.info("Initializing start time for ta3 mode %s" % _start_time)


    def get_pipeline_count(self):
        """
        Each optimizer has a different approach so it is asked how many solutions it plans to return. CROptimizer
        generally does 20 but the GraphOptimizer can only generate 1 solution
        """
        raise NotImplementedError()


    def adjust_target_column(self, dataset=None):
        # The learning data is the resource that needs to be altered for the target change, if necessary
        resource_id = 'learningData'
        # Check to see if the target specified by the ta3 matches up with the suggestedTarget in the dataset
        specified_target = self.config.target_name
        specified_target_index = -1
        suggested_target = -1
        suggested_target_index = -1
        # Iterate over the features in the dataset
        for index, feature in enumerate(dataset['learningData'].columns):
            # Keep track of the column index of the target specified by ta3
            if specified_target in feature:
                specified_target_index = index
            # When the suggested target is found, keep its column index and name
            if self.dataset.metadata.has_semantic_type((resource_id, Base.ALL_ELEMENTS, index),
                                                       'https://metadata.datadrivendiscovery.org/types/SuggestedTarget'):
                suggested_target_index = index
                suggested_target = feature
        # If the suggested target and the specified target match, no adjustments are necessary
        if specified_target in suggested_target:
            _logger.info("Suggested target and specified target match")
        # Otherwise we need to adjust the semantic types of the two features so the correct feature is set as the
        # target for training
        else:
            _logger.info("Suggested Target %s is being overriden by TA3 as %s" % (suggested_target, specified_target))

            # Remove Suggested Target attribute from Dataset
            dataset.metadata = dataset.metadata.remove_semantic_type(
                (resource_id, Base.ALL_ELEMENTS, suggested_target_index),
                'https://metadata.datadrivendiscovery.org/types/SuggestedTarget')

            dataset.metadata = dataset.metadata.add_semantic_type(
                (resource_id, Base.ALL_ELEMENTS, suggested_target_index),
                'https://metadata.datadrivendiscovery.org/types/Attributes')

            # Add Suggested Target to At Bat
            dataset.metadata = dataset.metadata.remove_semantic_type(
                (resource_id, Base.ALL_ELEMENTS, specified_target_index),
                'https://metadata.datadrivendiscovery.org/types/Attributes')

            dataset.metadata = dataset.metadata.add_semantic_type(
                (resource_id, Base.ALL_ELEMENTS, specified_target_index),
                'https://metadata.datadrivendiscovery.org/types/SuggestedTarget')
        return dataset


    def remove_attribute_from_target(self, dataset=None, test_dataset=None):
        #TODO: Fix this once the SuggestedTarget is replaced by TrueTarget in the data
        suggested_target_type = 'https://metadata.datadrivendiscovery.org/types/SuggestedTarget'
        true_target_type = 'https://metadata.datadrivendiscovery.org/types/TrueTarget'
        attribute_type = 'https://metadata.datadrivendiscovery.org/types/Attribute'
        if dataset is None:
            dataset = self.dataset
            test_dataset = self.test_dataset

        # TODO: Do we need to handle test data when dataset is provided as a parameter?

        resource_id, resource = base_utils.get_tabular_resource(dataset, None)
        for index, feature in enumerate(dataset[resource_id].columns):
            selector = (resource_id, Base.ALL_ELEMENTS, index)
            if dataset.metadata.has_semantic_type(selector, suggested_target_type):
                dataset.metadata = dataset.metadata.remove_semantic_type(selector, attribute_type)
            if dataset.metadata.has_semantic_type(selector, true_target_type):
                dataset.metadata = dataset.metadata.remove_semantic_type(selector, attribute_type)

        if test_dataset is not None:
            resource_id, resource = base_utils.get_tabular_resource(test_dataset, None)
            for index, feature in enumerate(test_dataset[resource_id].columns):
                selector = (resource_id, Base.ALL_ELEMENTS, index)
                if test_dataset.metadata.has_semantic_type(selector, suggested_target_type):
                    test_dataset.metadata = test_dataset.metadata.remove_semantic_type(selector, attribute_type)
                if test_dataset.metadata.has_semantic_type(selector, true_target_type):
                    test_dataset.metadata = test_dataset.metadata.remove_semantic_type(selector, attribute_type)

        return dataset, test_dataset


    def fit(self):
        """
        Optimize against the training data.
        """
        raise NotImplementedError()


    def pipelines(self, index=None):
        """
        Return an iterator over the best pipelines found, which are
        AutoflowPipeline objects.  Raise an exception if fit has not
        been run yet.
        """
        raise NotImplementedError()


    def running_pipelines(self):
        raise NotImplementedError()


    def considered_pipelines(self):
        """
        Return an iterator over the best pipelines found, which are
        AutoflowPipeline objects.  Raise an exception if fit has not
        been run yet.
        """
        raise NotImplementedError()


    def use_dataset(self, data_uri):
        self.dataset = Dataset.load(data_uri)


    '''
    This is to support the DescribeSolution call for TA3
    '''
    def get_pipeline(self, solution_id):
        raise NotImplementedError()


    def checkpoint(self, break_after_first=False, index=None):
        _logger.info("Checkpointing pipelines... Index: %s" % index)
        count = 0
        for pipeline in self.pipelines(index=index):
            if pipeline is None:
                continue
            pipeline.log()
            if break_after_first:
                return pipeline.name
            count += 1
        _logger.info("Checkpointed %s pipelines" % count)

        # Only perform this step once
        if not self.considered_pipelines_generated:
            self.considered_pipelines_generated = True
            _logger.info("Checkpointing considered pipelines...")
            considered_count = 0
            for pipeline in self.considered_pipelines():
                pipeline.log(True)
                considered_count += 1
                # TODO: Dont check in! In production make sure you do not limit the # of considered pipelines we generate
                # if considered_count >= 100:
                #     break
            _logger.info("Checkpointed %s considered pipelines" % considered_count)

        return count


    def checkpoint_state(self):
        pid = os.getpid()
        troot = self.config.temp
        state = self.get_checkpoint_state()
        state['pid'] = pid
        path = "%s/%d" % (troot, pid)
        with open(path, "wb") as fh:
            pickle.dump(state, fh)


    def get_checkpoint_state(self):
        """
        Basically, a no-op state.  Ideally, subclasses will provide a version that supports warn restarts.
        """
        return {}

    def get_state(self):
        """
        Return a hash containing all relevant aspects of state to restore about restart.
        """
        raise NotImplementedError()

    def set_state(self, stateobj):
        """
        Set internal state based on previously saved state object, a hash.
        """
        raise NotImplementedError()


    def reload_state(self, statefile):
        with open(statefile, "rb") as fh:
            stateobj = pickle.load(fh)
        self.set_state(stateobj)


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class GraphOptimizer(AutoflowOptimizer):

    pipeline_count = 1
    pipeline_complete = False

    def __init__(self, **kw):
        super().__init__(**kw)
        self.pipeline = self.pipeline_class.generate(self.dataset)
#        self.pipeline = self.pipeline_class.get_instance()


    def get_pipeline_count(self):
        return self.pipeline_count


    @threaded
    def spinoff_fit(self, search_id, solution_ids, ta3_preamble):
        """
        Threaded entrypoint for the TA3TA2api to initiate a fit call on a separate thread.
        """
        # Adjust the output paths to use the search_id as the directory between the dataset and the
        # pipeline files
        self.config.update_paths(search_id)

        _logger.info("GraphOptimizer spinoff_fit")
        self.solution_ids = solution_ids

        for i in range(0, 1):
            self.solution_ids_to_index[solution_ids[i]] = i

        self.fit()


    def fit(self):
        """
        Fit for the Graph Problems
        :return:
        """
        _logger.info("GraphOptimizer fit")
        self.fitted_pipeline = Runtime(self.pipeline, context=Base.Context.TESTING, volumes_dir=self.config.static_volumes)
        dataset = self.remove_attribute_from_target()
        self.fitted_pipeline.fit(inputs=[dataset[0]])
        self.pipeline_obj = GraphPipeline(optimizer=self,
                                          pipeline=self.pipeline,
                                          fitted_pipeline=self.fitted_pipeline,
                                          rank=1)
        _logger.info("Created pipeline %s (%d)" %
                     (self.pipeline_obj.name, self.pipeline_obj.rank))
        self.pipeline_complete = True


    def pipelines(self, index=None):
        if self.pipeline is None:
            raise UnfitException()
        yield self.pipeline_obj


    def get_pipeline(self, solution_id):
        if self.pipeline is None:
            _logger.info("Pipeline is not yet ready to describe for this solution id: %s" % solution_id)
        return self.pipeline_obj


    def considered_pipelines(self):
        for p in self.pipelines():
            yield p


    def running_pipelines(self):
        """
        Depending on the state of the pipelines this method will return a "running" pipeline
        structure or a completed pipeline structure to the TA3TA2-api layer for communication
        to the TA3 client
        """
        timestamp = Timestamp()
        start = timestamp
        end = timestamp
        start.GetCurrentTime()
        end.GetCurrentTime()

        state = "running"
        time_left = self._minutes_remaining()
        if time_left < 2:
            state = "completed"
            _logger.info("%s minutes left, tell TA3 so it can harvest the pipelines..." % time_left)
        else:
            _logger.info("%s minutes left, keep improving..." % time_left)

        if not self.pipeline_complete:
            _logger.info("No valid pipelines have been returned yet")
            for index in range(0, self.pipeline_count):
                pipeline_state = dict(
                    state="running",
                    status="running",
                    start=start,
                    end=end,
                    done_ticks=0,
                    all_ticks=0,
                    solution_id=self.solution_ids[index],
                    score=0,
                    rank=index + 1
                )
                yield pipeline_state
        else:
            self.checkpoint()
            _logger.info("Candidate pipelines present...")
            for index in range(0, self.pipeline_count):
                # TODO: Use the reference runtime to score the pipeline
                pipeline_score = 0.1
                pipeline_state = dict(
                    state=state,
                    status="successful",
                    start=start,
                    end=end,
                    done_ticks=0,
                    all_ticks=0,
                    solution_id=self.solution_ids[index],
                    score=pipeline_score,
                    rank=index + 1
                )
                yield pipeline_state


    def completed_pipeline(self, solution_id):
        """
        Once processing is complete return the score results to the TA3TA2-api layer
        """
        solution_index = self.solution_ids_to_index[solution_id]

        timestamp = Timestamp()
        start = timestamp
        end = timestamp
        start.GetCurrentTime()
        end.GetCurrentTime()
        pipeline_state = None


        if not self.pipeline_complete:
            _logger.info("No valid pipelines have been returned yet")

            pipeline_state = dict(
                state="running",
                status="running",
                start=start,
                end=end,
                metric=self.config.metric,
                score=0.0,
                rank=1
            )
        else:
            _logger.info("Candidate pipelines present...")

            # TODO: use the reference runtime to score the pipeline to get this value
            pipeline_score = 0.1

            pipeline_state = dict(
                state="completed",
                status="successful",
                start=start,
                end=end,
                metric=self.config.metric,
                score=pipeline_score,
                rank=solution_index
            )

        return pipeline_state


    def spinoff_export(self, fitted_solution_id=None, rank=None):
        _logger.info("Exporting pipeline for fitted_solution_id: %s and rank: %s" % (fitted_solution_id, rank))

        # TODO: Currently already done for Graphs? so this is a no-op?
        # self.checkpoint()

        _logger.info("Exported pipelines for problem: %s", self.config.problem_id)

    def end_search(self, search_id):
        _logger.info("Removing search associated with search_id: %s" % search_id)
        # TODO: Probably need to purge the solution ids


    def unpickle_pipeline(self, pipeline_name):
        return GraphPipeline(optimizer=self, pipeline_name=pipeline_name)


    def get_state(self):
        """ We currently don't support restarting long-running optimizations, no this is a no-op """
        return {}


    def set_state(self, stateobj):
        """ We currently don't support restarting long-running optimizations, no this is a no-op """
        pass


class VertexClassificationOptimizer(GraphOptimizer):
    pipeline_class = find_pipeline_class(label="vertex_classification")

class VertexClassificationJHUOptimizer(GraphOptimizer):
    pipeline_class = find_pipeline_class(label="vertex_classification_jhu")

class GraphMatchingJHUOptimizer(GraphOptimizer):
    pipeline_class = find_pipeline_class(label="graph_matching_jhu")

class LinkPredictionJHUOptimizer(GraphOptimizer):
    pipeline_class = find_pipeline_class(label="link_prediction_jhu")

class CommunityDetectionJHUOptimizer(GraphOptimizer):
    pipeline_class = find_pipeline_class(label="community_detection_jhu")

class ObjectDetectionOptimizer(GraphOptimizer):
    # Until we have a better way to do object detection
    pipeline_class = find_pipeline_class(label="baseline")


class CROptimizer(AutoflowOptimizer):
    """
    Base class for all classification and regression optimization.
    """

    solution_fitted = False
    # Default to 20 as this is what the D3M eval expects
    pipeline_count = 20

    def __init__(self, **args):

        super().__init__(**args)

        # Check for the presence of a Pipeline Count over-ride - this is used by the integration test
        if 'D3M_Pipeline_Count' in os.environ:
            self.pipeline_count = int(os.environ['D3M_Pipeline_Count'])

        # Define a callback for when pipelines are evaluated by TPOT
        def pipeline_eval_callback(pipeline, score):
            if math.isinf(score):
                return
            # Ensure safe access to the nbest structure
            acquire = False
            try:
                acquire = self.mutex.acquire()
                _logger.debug("Trying to insert pipeline with score %f" % score)
                inserted = self.nbest.insert(pipeline, score)
                if inserted:
                    _logger.info("Internal scores for Problem: %s. Inserted pipeline with score %f into nbest. Current size: (%d)" %
                                 (self.config.problem_id, score, len(self.nbest)))

                self.solution_fitted = True
            finally:
                if acquire:
                    self.mutex.release()
                else:
                    logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")

        # Save to field, because Gama optimization wants to instantiate a new optimizer with each round of fitting
        self.pipeline_eval_callback = pipeline_eval_callback

        # Define a function to call at the end of each TPOT generation
        def gen_callback():
            # We used to checkpoint pipelines here due to stability concerns but have since removed it due to thread lock issues.
            _logger.info("End of generation gen_callback() invoked from sri_tpot")

        # Save to field, because Gama optimization wants to instantiate a new optimizer with each round of fitting
        self.gen_callback = gen_callback

        optr_args = self.optimizer_arguments = {}
        self.get_optimizer_arguments(pipeline_eval_callback, gen_callback)

        _logger.info("Creating optimizer: %s(%s)" % (self.optimizer_class.__name__, str(optr_args)))
        _logger.info("Using %s CPU's", optr_args['n_jobs'])

        self.pipeline_optimizer = self.optimizer_class(**optr_args)


    def get_pipeline_count(self):
        return self.pipeline_count


    def get_optimizer_arguments(self, pipeline_eval_callback, gen_callback):
        optr_args = self.optimizer_arguments

        optr_args['n_jobs'] = int(self.config.cpus)

        # Set any arguments specified by the config file
        for arg, val in self.config.optimizer_arguments():
            optr_args[arg] = val


    @threaded
    def spinoff_fit(self, search_id, solution_ids, ta3_preamble):
        """
        Threaded entrypoint for the TA3TA2api to initiate a fit call on a separate thread.
        """
        # Adjust the output paths to use the search_id as the directory between the dataset and the
        # pipeline files
        self.config.update_paths(search_id)

        self.solution_ids = solution_ids
        for i in range(0, self.pipeline_count):
            self.solution_ids_to_index[solution_ids[i]] = i

        # Tell TPOT not to bother with generation-level timeout,
        # because the signal-based timeout does not play well
        # with threading.
        self.pipeline_optimizer.max_generation_time_mins = None

        # size = len(self.search_id_map)
        # _logger.info("Adding search_id: %s to other %s running searches" % (search_id, size))
        # self.search_id_map.add(search_id)
        # TODO: Can we associate this search_id with the thread so we can kill it when requested?
        self.pipeline_optimizer.max_generation_time_mins = None
        self.fit(ta3_preamble=ta3_preamble)


    def fit(self, ta3_preamble=None):
        """
        Fit for the Classification/Regression Problems
        This step could actually be called search as it is searching for valid pipelines. After valid
        pipelines are discovered, fit_pipeline is called (see the pipelines function below) which then
        fits the data to each of the found pipelines.
        """
        _logger.info("optimizer::fit() called")
        # Ensure safe access to the nbest structure
        _logger.info("\toptimizer::fit() mutex acquired")
        acquire = False
        try:
            acquire = self.mutex.acquire()
            _logger.info("\toptimizer::fit() setting up nbest")
            # Set up pipeline tracking
            self.nbest = NBest(self.pipeline_count)
            self.nbest.set_item_hash(lambda p: self.clean_pipeline_string(p))
            _logger.info("\toptimizer::fit() nbest established")
        finally:
            _logger.info("\toptimizer::fit() mutex release")
            if acquire:
                self.mutex.release()
            else:
                logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")

        _logger.info("\toptimizer::fit() calling prep_data")
        self.features, self.targets, self.test_features, self.test_targets = self.prep_data()

        _logger.info("Fitting %s" % self.config.backend)
        picklePath = "%s/best.mdl" % self.config.temp

        # Drop this down to accelerate learning (at the expense of model performance).
        # 1000 is the default, 200 for speed
        sample_size = 1000
        while sample_size < self.features.shape[0] and self._minutes_remaining() > 2:
            _logger.info("Early fitting with %d examples" % sample_size)
            self.fit_sample(self._minutes_remaining(), picklePath, sample_size)
            sample_size *= 10

        minutes_remaining = self._minutes_remaining()
        if minutes_remaining > 5:
            self.fit_sample(minutes_remaining, picklePath)
        else:
            _logger.warning("Insufficiant time remaining (%s minutes) to fit_sample, GAMA exiting..." % minutes_remaining)

        _logger.info("%s fitting completed" % self.config.backend)

        if self.test_features is not None:
            try:
                score = self.pipeline_optimizer.score(self.test_features, self.test_targets)
                _logger.info("Score of best gama pipeline on Test dataset is: %s" % score)
            except Exception as e:
                # This is bonus information so lets not blow up the run due to failure
                _logger.info("Encountered exception while trying to get the inner Gama scores: %s" % e)
                _logger.warning(traceback.format_exc())



    def fit_optimizer(self, feats, targs, picklePath):
        """
        Method introduced to accommodate differences in arguments between TPOT.fit and GAMA.fit
        """
        raise NotImplementedError()


    def running_pipelines(self):
        """
        Depending on the state of the pipelines this method will return a "running" pipeline
        structure or a completed pipeline structure to the TA3TA2-api layer for communication
        to the TA3 client
        """
        timestamp = Timestamp()
        start = timestamp
        end = timestamp
        start.GetCurrentTime()
        end.GetCurrentTime()

        state = "running"
        time_left = self._minutes_remaining()
        if time_left < 2:
            state = "completed"
            _logger.info("%s minutes left, tell TA3 so it can harvest the pipelines..." % time_left)
        else:
            _logger.info("%s minutes left, keep improving..." % time_left)

        # Ensure safe access to the nbest structure
        acquire = False
        try:
            acquire = self.mutex.acquire()
            completed_pipeline_count = 0
            pipeline_count = 0
            if hasattr(self, 'nbest'):
                completed_pipeline_count = self.nbest.item_list.__len__()
                pipeline_count = self.nbest.size

            if completed_pipeline_count == 0:
                _logger.info("No valid pipelines have been returned yet")
                for index in range(0, pipeline_count):
                    pipeline_state = dict(
                        state="running",
                        status="running",
                        start=start,
                        end=end,
                        done_ticks=0,
                        all_ticks=0,
                        solution_id=self.solution_ids[index],
                        score=0,
                        rank=index
                    )
                    yield pipeline_state
            else:
                _logger.info("Candidate pipelines present...")
                for index, pipeline in enumerate(self.nbest.item_list):
                    pipeline_score = pipeline[2]
                    if isinstance(self.pipeline_optimizer, GamaRegressor):
                        _logger.info("Converting pipeline score from %s" % pipeline_score)
                        pipeline_score *= -1
                        _logger.info("to %s" % pipeline_score)
                    pipeline_state = dict(
                        state=state,
                        status="successful",
                        start=start,
                        end=end,
                        done_ticks=0,
                        all_ticks=0,
                        solution_id=self.solution_ids[index],
                        score=pipeline_score,
                        rank=index + 1 # Rank is a 1 based system so there is no rank 0
                    )
                    yield pipeline_state

        finally:
            if acquire:
                self.mutex.release()
            else:
                logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")


    def completed_pipeline(self, solution_id):
        """
        Once processing is complete return the score results to the TA3TA2-api layer
        """
        solution_index = self.solution_ids_to_index[solution_id]

        timestamp = Timestamp()
        start = timestamp
        end = timestamp
        start.GetCurrentTime()
        end.GetCurrentTime()

        pipeline_state = None

        # Ensure safe access to the nbest structure
        acquire = False
        try:
            acquire = self.mutex.acquire()
            completed_pipeline_count = self.nbest.item_list.__len__()

            if completed_pipeline_count <= solution_index:
                _logger.info("No valid pipelines have been returned yet")
                pipeline_state = dict(
                    state="running",
                    status="running",
                    start=start,
                    end=end,
                    metric=self.config.metric,
                    score=0.0,
                    rank=0.0
                )
            else:
                _logger.info("Candidate pipelines present...")
                pipeline_score = self.nbest.item_list[solution_index][2]
                if isinstance(self.pipeline_optimizer, GamaRegressor):
                    _logger.info("Converting pipeline score from %s" % pipeline_score)
                    pipeline_score *= -1
                    _logger.info("to %s" % pipeline_score)
                pipeline_state = dict(
                    state="completed",
                    status="successful",
                    start=start,
                    end=end,
                    metric=self.config.metric,
                    score=pipeline_score,
                    rank=solution_index
                )
        finally:
            if acquire:
                self.mutex.release()
            else:
                logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")

        return pipeline_state


    def fitted_result(self, solution_id=None):
        """
        Return the fitting of a solution status to the GetFitSolutionResults call in the TA3TA2-api layer
        """
        # This tells us which of the pipelines is associated with this solution id
        index = self.solution_ids_to_index[solution_id]
        timestamp = Timestamp()
        start = timestamp
        end = timestamp
        start.GetCurrentTime()
        end.GetCurrentTime()

        # Convert to a d3m pipeline so we can get the fitted output
        pipeline = self.pipelines(index=index)
        d3m_pipeline = pipeline[0].as_d3m_pipeline("Autoflow Pipeline", "Pipeline generated by AutoFlow optimizer", None)
        fitted_pipeline = Runtime(d3m_pipeline, context=Base.Context.TESTING, volumes_dir=self.config.static_volumes)
        fit_result = fitted_pipeline.fit(inputs=[self.dataset])

        pipeline_state = None

        # Ensure safe access to the nbest structure
        acquire = False
        try:
            acquire = self.mutex.acquire()
            completed_pipeline_count = self.nbest.item_list.__len__()

            if completed_pipeline_count <= index:
                _logger.info("No fitted pipelines have been returned yet")
                pipeline_state = dict(
                    state="running",
                    status="running",
                    start=start,
                    end=end,
                    metric=self.config.metric
                )
            else:
                _logger.info("Fitted pipelines now ready to return...")
                pipeline_state = dict(
                    state="completed",
                    status="successful",
                    start=start,
                    end=end,
                    metric=self.config.metric,
                    fit_result = fit_result
                )

        finally:
            if acquire:
                self.mutex.release()
            else:
                logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")

        return pipeline_state


    def spinoff_produce_solution(self, dataset_schema, solution_id):
        while not self.solution_fitted:
            time.sleep(20)

        index = self.solution_ids_to_index[solution_id]

        predictions_file = None
        i = 0
        # Ensure safe access to the nbest structure
        for pipeline in self.pipelines():
            if i == index:
                if pipeline is None:
                    _logger.warning("There was a problem with this pipeline")
                    return None
                dataset = Dataset.load(dataset_schema)
                dataset = self.remove_attribute_from_target(dataset=dataset)
                try:
                    predictions_file = pipeline.produce_ta3(dataset=dataset, index=index)
                except Exception as e:
                    _logger.error("Exception encountered while producing. This is the Issue Tufts encountered "
                                  "at the July 2019 event that we could not repro. Should be fixed by Daraghs checkin on Nov 4th 2019...: %s", e)
                    _logger.warning(traceback.format_exc())
                break
            else:
                i += 1
        self.solution_ids_to_predictions[solution_id] = predictions_file


    def solution_results(self):
        return


    def spinoff_export(self, solution_id=None, rank=None):
        """
        Threaded entrypoint for the TA3TA2api to export the solutions to disk
        """
        _logger.info("Exporting pipeline for fitted_solution_id: %s and rank: %s" % (solution_id, rank))

        # what index goes with the fitted_solution_id specified
        solution_index = self.solution_ids_to_index[solution_id]
        self.checkpoint(index=solution_index)

        _logger.info("Exported pipelines for problem: %s", self.config.problem_id)


    def end_search(self, search_id):
        _logger.info("Removing search associated with search_id: %s" % search_id)
        # TODO: Probably need to purge the solution ids


    def convert_to_frame(self, table_index):
        table = self.dataset[table_index]
        columns = self.config.column_names(table_index)
        frame = pd.DataFrame(table, None, columns)

        # Suppress privileged columns for now
        # We'll have to figure out how to do something more sophisticated
        # for LUPI problems later
        if table_index in self.config.privileged_columns:
            pcols = self.config.privileged_columns[table_index]
            for col in pcols:
                #                print("Dropping privileged column", col)
                frame.drop(col, axis=1)

        for join_tabi, join_column in self.config.table_references(table_index):
            join_frame = self.convert_to_frame(join_tabi)
            frame = pd.merge(frame, join_frame, on=join_column, how='left')
        return frame


    def get_features(self):
        table_index, target_index = self.config.key_table_indexes()
        frame = self.convert_to_frame(table_index)
        target_name = self.config.get_target_name()
        frame = frame.drop(target_name, axis=1)
        return frame


    def get_targets(self, targs):
        raise NotImplementedError()


    def get_lupi_columns(self, dataset):
        tab, col = self.config.key_table_indexes()
        try:
            return list(self.config.privileged_columns[tab])
        except KeyError:
            return []


    def get_preamble_pipeline(self, dataset, skip_augmentation=False):
        # Enhance this to study the data and selecting an appropriate ppln
        if self.config.taskType == 'semiSupervisedClassification':
            classname = 'SingleTableSemiFragment'
        elif self.config.taskType == 'timeSeriesForecasting':
            classname = 'TimeSeriesForecastingFragment'
        elif self.config.taskType == 'timeSeriesClassification':
            classname = 'TimeSeriesClassificationFragment'
        elif len(dataset) == 1:
            #TODO: Add this Fragment back in when we figure out how they are structing the datasets with the
            # MIN_Metadata formatr (Jan 16 2020)
            # self.lupi_columns = self.get_lupi_columns(dataset)
            # if len(self.lupi_columns) > 0:
            #     classname = 'SingleTableLUPIFragment'
            # else:
            classname = 'SingleTableSRIFragment'
        else:
            # restypes = self.config.data_resource_types()
            # if len(restypes) == 2 and 'timeseries' in restypes:
            #     classname = 'TimeSeriesClassificationFragment'
            #TODO: Add these back in when we have a working solution for image/video. Until then use the fallback
            # MultiTableSRIFragment
            # elif len(restypes) == 2 and 'image' in restypes:
            #     classname = 'ImageRecognitionFragment'
            # elif len(restypes) == 2 and 'video' in restypes:
            #     classname = 'VideoClassificationFragment'
            # else:
            classname = 'MultiTableSRIFragment'

        ppclass = find_pipeline_class(name=classname)
        logging.info("Using Fragment: %s for %s problem" % (classname, self.config.problem_id))

        if skip_augmentation:
            ahints = None
        elif self.config.augmentation_enabled():
            ahints = self.config.data_augmentation
        else:
            ahints = None
        logging.info("Generate the preamble pipeline")
        self.preamble_pipeline = ppclass.generate(dataset, config=self.config, augmentation_hints=ahints)
        logging.info("Preamble pipeline generation complete")
        preamble_args = dict(max_tokenized_expansion=30)
        for arg, val in self.config.preamble_arguments():
            preamble_args[arg] = val
        preamble_args = dict((k, v) for k,v in preamble_args.items()
                             if self.preamble_pipeline.has_configuration_option(k))
        self.preamble_pipeline.configure(**preamble_args)
        self.preamble_pipeline.study_dataset(dataset)
        return self.preamble_pipeline



    def execute_ta3_preamble(self, ta3_preamble, dataset):
        if ta3_preamble is None:
            self.ta3_preamble = None
            return dataset

        _logger.info("Executing TA3 preamble pipeline")
        self.ta3_preamble = ta3_preamble
        ta3_preamble = copy.copy(ta3_preamble)
        last_step = ta3_preamble.steps[-1]
        # If the last step is a placeholder, we remove it, making the
        # pipeline's output its inputs
        if isinstance(last_step, PlaceholderStep):
            outputs = [v['data'] for v in last_step.arguments.values()]
            ta3_preamble.steps.pop()
            ta3_preamble.outputs = outputs
        rt = Runtime(ta3_preamble, context=Base.Context.TESTING, volumes_dir=self.config.static_volumes)
        rt.fit(inputs=[dataset])
        outputs = rt.produce(inputs=[dataset])
        return outputs[0]


    def subselect_dataset(self, dataset):
        if not hasattr(self.config, 'maximum_rows'):
            return dataset
        maxrows = self.config.maximum_rows
        tab, col = self.config.key_table_indexes()
        df = dataset[tab]
        if df.shape[0] > maxrows:
            _logger.info("Selecting %d of %d rows" % (maxrows, df.shape[0]))
            dataset[tab] = df[0:maxrows]
        return dataset


    def prep_data(self, ta3_preamble=None):
        _logger.info("optimizer::prep_data called")

        dataset, test_dataset = self.remove_attribute_from_target()
        dataset = self.execute_ta3_preamble(ta3_preamble, dataset)
        dataset = self.subselect_dataset(dataset)

        if test_dataset is not None:
            test_dataset = self.execute_ta3_preamble(ta3_preamble, test_dataset)
            # No need to do this for test data as we want to use everything.
            # test_dataset = self.subselect_dataset(test_dataset)

        # try:
        #     return self.get_features_and_targets(dataset, test_dataset)
        # except Exception as e:
        #     _logger.warning("Attempted augmentation: Exception %s" % str(e))
        #     _logger.warning(traceback.format_exc())
        #     if self.config.augmentation_enabled() and self.config.data_augmentation is not None:
        #         _logger.error("Data augmentation failed. Attempting without augmentation.")
        return self.get_features_and_targets(dataset, test_dataset, skip_augmentation=True)
            # else:
            #     raise


    def get_features_and_targets(self, dataset, test_dataset, skip_augmentation=False):
        features, targets = self.get_features_and_targets_from_dataset(dataset, skip_augmentation)
        test_features = None
        test_targets = None
        if test_dataset is not None:
            self.fitted_preamble.fit(inputs=[test_dataset])
            result = self.fitted_preamble.produce(inputs=[test_dataset])
            test_features = result.values['outputs.0']
            test_targets = self.get_targets(result.values['outputs.1'])
            # test_features, test_targets = self.get_features_and_targets_from_dataset(test_dataset, skip_augmentation)

        return features, targets, test_features, test_targets

    def get_features_and_targets_from_dataset(self, dataset, skip_augmentation):
        _logger.info("\toptimizer::fit() getting preamble")
        self.get_preamble_pipeline(dataset, skip_augmentation=skip_augmentation)
        _logger.info("\toptimizer::fit() Preamble obtained")
        self.fitted_preamble = Runtime(self.preamble_pipeline, context=Base.Context.TESTING, volumes_dir=self.config.static_volumes)
        _logger.info("\toptimizer::fit() Fitted Preamble obtained")

        target_column_index = -1
        if hasattr(self.config, 'target_column_name'):
            # Use the column name to get the index of the target column
            target_column_index = int(numpy.where(dataset['learningData'].columns == self.config.target_column_name)[0][0])
        else:
            # This is for the open ml datasets which dont have a problemDoc.json containing a target_column_name
            for index, feature in enumerate(dataset['learningData'].columns):
                # When the suggested target is found, keep its column index and name
                if self.dataset.metadata.has_semantic_type(('learningData', Base.ALL_ELEMENTS, index),
                                                           'https://metadata.datadrivendiscovery.org/types/SuggestedTarget'):
                    target_column_index = index

        # Apply the TrueTarget metadata to the target column.
        dataset.metadata = dataset.metadata.add_semantic_type(
            ('learningData', Base.ALL_ELEMENTS, target_column_index),
            'https://metadata.datadrivendiscovery.org/types/TrueTarget')

        # why do we have a '0' data element in the dataset object for video but not for baseball?
        fit_result = self.fitted_preamble.fit(inputs=[dataset])
        if fit_result.pipeline_run.status.get('state', None) == 'FAILURE':
            _logger.error(fit_result.pipeline_run.status['message'])
        # Now prep the data for TPOT by running through a cleaning pipeline
        _logger.info("optimizer::prep_data Before data prep")
        result = self.fitted_preamble.produce(inputs=[dataset])
        features = result.values['outputs.0']
        targets = self.get_targets(result.values['outputs.1'])
        _logger.info("optimizer::prep_data After data prep")
        return features, targets

    def unpickle_pipeline(self, pipeline_name):
        return TPOTPipeline(optimizer=self, pipeline_name=pipeline_name)


    def list_primitives(self):
        """
        Collects and returns the primitive data assocaited with all available primitives for the the
        TA3 client to review
        """
        # need to be updated to current api, because `d3m.index.search()` does not longer return a dict
        primitives_info = []
        primitives = d3m.index.search()
        for primitive in primitives.values():
            id = primitive.metadata.query()['id']
            version = primitive.metadata.query()['version']
            python_path = primitive.metadata.query()['python_path']
            name = primitive.metadata.query()['name']
            digest = primitive.metadata.query()['digest']
            primitive_info = {
                'id': id,
                'version': version,
                'python_path': python_path,
                'name': name,
                'digest': digest
            }
            primitives_info.append(primitive_info)
        return primitive_info


    # This needs to be elaborated, so that we can resume search where we left off
    def get_state(self):
        return {}


    # Needs elaboration
    def set_state(self, stateobj):
        pass


class RegressionOptimizer(CROptimizer):

    # Regression needs floating-point targets
    def get_targets(self, targs):

        # We should no longer need to convert to float, as ColumnParser does this
        self.target_dict = None
        self.target_series = None
        return targs


class ClassificationOptimizer(CROptimizer):

    # We want integers
    def get_targets(self, targs):

        # The kind of intervention we engage in below is no longer sanctioned
        # Processing is provided by SimpleColumnParser
        self.target_series = None
        self.target_dict = None
        return targs


class TPOTOptimizer(CROptimizer):

    def get_optimizer_arguments(self, pipeline_eval_callback, gen_callback):
        optr_args = self.optimizer_arguments
        optr_args['scoring'] = self.config.metric
        optr_args['update_callback'] = pipeline_eval_callback
        optr_args['generation_callback'] = gen_callback
        # search_time = self.config.timeout * 0.66
        # logging.info("Adjustime search time from %s to: %s" % (self.config.timeout, search_time))
        optr_args['max_time_mins'] = self.config.timeout
        optr_args['max_eval_time_mins'] = 4
        optr_args['verbosity'] = 2
        optr_args['random_state'] = 42
        config_path = self.get_config_path()
        _logger.info("Using config file: %s" % config_path)
        optr_args['config_dict'] = config_path
        super().get_optimizer_arguments(pipeline_eval_callback, gen_callback)


    def fit_sample(self, max_minutes, picklePath, sample_size=None):
        """
        Fit on a sample of the data.
        """
        if max_minutes <= 0:
            return
        if sample_size is None:
            self.pipeline_optimizer.max_time_mins = max_minutes
            feats = self.features
            targs = self.targets
        else:
            self.pipeline_optimizer.max_time_mins = None
            self.pipeline_optimizer.generations = 3
            permutation = list(range(self.features.shape[0]))
            numpy.random.shuffle(permutation)
            feats = self.features.iloc[permutation[0:sample_size], :]
            targs = self.targets.iloc[permutation[0:sample_size], :]
        self.fit_optimizer(feats, targs, picklePath)


    def fit_optimizer(self, feats, targs, picklePath):
        self.pipeline_optimizer.fit(feats, targs, picklePath, **dict(self.config.fit_arguments()))


    def clean_pipeline_string(self, p):
        return self.pipeline_optimizer.clean_pipeline_string(p)


    def pipelines(self, index=None):
        # Ensure safe access to the nbest structure
        acquire = False
        try:
            acquire = self.mutex.acquire()
            top_pipelines = self.nbest.result(True, True)
        finally:
            if acquire:
                self.mutex.release()
            else:
                logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")

        pipelines = []
        if index is not None:
            score, pipeline, created = top_pipelines[index]
            pln = TPOTPipeline(ta3_preamble=self.ta3_preamble,
                               preamble=self.preamble_pipeline,
                               fitted_preamble=self.fitted_preamble,
                               pipeline=pipeline,
                               target_dict=self.target_dict,
                               target_series=self.target_series,
                               optimizer=self,
                               score=score,
                               rank=index + 1,
                               created=created
                               )
            _logger.info("Created pipeline at index %s %s (%d, %f): %s" %
                         (index, pln.name, pln.rank, pln.score, pln))
            pipelines.append(pln)
        else:
            rank = 1
            for score, pipeline, created in top_pipelines:
                pln = TPOTPipeline(ta3_preamble=self.ta3_preamble,
                                       preamble=self.preamble_pipeline,
                                       fitted_preamble=self.fitted_preamble,
                                       pipeline=pipeline,
                                       target_dict=self.target_dict,
                                       target_series=self.target_series,
                                       optimizer=self,
                                       score=score,
                                       rank=rank,
                                       created=created
                                       )
                _logger.info("Created pipeline %s (%d, %f): %s" %
                             (pln.name, pln.rank, pln.score, pln))
                pipelines.append(pln)
                rank += 1
        return pipelines


    def get_pipeline(self, solution_id):
        solution_index = self.solution_ids_to_index[solution_id]
        _logger.info("Requesting Pipeline Description for solution_id %s and index %s" % (solution_id, solution_index))
        pipeline = self.pipelines(index=solution_index)
        if pipeline is None:
            _logger.info("Pipeline is not yet ready to describe for this solution id: %s" % solution_id)
        return pipeline


    def considered_pipelines(self):
        """
        Generator yielding all evaluated pipelines
        """
        # Ensure safe access to the nbest structure
        acquire = False
        try:
            acquire = self.mutex.acquire()
            all_pipelines = self.nbest.all_items(True, True)
            for score, pipeline, created in all_pipelines:
                pln = TPOTPipeline(ta3_preamble=self.ta3_preamble,
                                       preamble=self.preamble_pipeline,
                                       pipeline=pipeline,
                                       optimizer=self,
                                       score=score,
                                       created=created
                                       )
                yield pln
        finally:
            if acquire:
                self.mutex.release()
            else:
                logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")


class TPOTRegressionOptimizer(TPOTOptimizer, RegressionOptimizer):

    if os.getenv('TPOT') is not None:
        optimizer_class = TPOTRegressor

    def get_config_path(self):
        return "%s/tpot-regressor-config.py" % self.config.code_directory()


class TPOTClassificationOptimizer(TPOTOptimizer, ClassificationOptimizer):

    if os.getenv('TPOT') is not None:
        optimizer_class = TPOTClassifier

    def get_config_path(self):
        return "%s/tpot-classifier-config.py" % self.config.code_directory()


class GamaOptimizer(CROptimizer):

    """
    Disabled.  The point of this was to set callback methods on the backend, but the Gama logic creates a new one
    with each fit, so we're going to set callbacks at fitting time.
    def __init__(self, **args):
        self.pipeline_evaluation_callback = None
        self.generation_callback = None
        # The above fields are set to meaningful values in the super init
        super().__init__(**args)
        peval_callback = self.pipeline_evaluation_callback
        gen_callback = self.generation_callback
        self.pipeline_optimizer.evaluation_completed(lambda pl: peval_callback(pl, pl.fitness.values[0]))
        self.pipeline_optimizer._observer.on_pareto_updated(lambda _: gen_callback())
    """

    def get_optimizer_arguments(self, pipeline_eval_callback, gen_callback):
        # Store the callbacks for a later step
        self.pipeline_evaluation_callback = pipeline_eval_callback
        self.generation_callback = gen_callback

        optr_args = self.optimizer_arguments
        optr_args['max_eval_time'] = 4*60
        optr_args['random_state'] = 42
        metric = self.config.metric if self.config.metric != 'f1_true' else 'f1'
        optr_args['scoring'] = metric
        # search_time = self.config.timeout * 0.66
        # logging.info("Adjust search time from %s to: %s" % (self.config.timeout, search_time))
        optr_args['max_total_time'] = (self.config.timeout) * 60
        fname, rule_name = self.config.grammar_rule()
        optr_args['grammar_file_name'] = fname
        optr_args['rule_name'] = rule_name
        optr_args['cache_dir'] = "%s/%s" % (self.config.temp, datetime.now().strftime("%Y%m%d_%H%M%s"))
        optr_args['post_processing_method'] = self.config.gama_postprocessor()
        _logger.info("Max total time: %s" % optr_args['max_total_time'])
        super().get_optimizer_arguments(pipeline_eval_callback, gen_callback)


    def clean_pipeline_string(self, p):
        return str(p)


    def fit_sample(self, max_minutes, picklePath, sample_size=None):
        """
        Fit on a sample of the data.
        """
        if max_minutes <= 0:
            return
        if sample_size is None:
            #self.pipeline_optimizer.max_time_mins = max_minutes
            feats = self.features
            targs = self.targets
        else:
            #self.pipeline_optimizer.max_time_mins = None
            #self.pipeline_optimizer.generations = 3
            permutation = list(range(self.features.shape[0]))
            numpy.random.shuffle(permutation)
            feats = self.features.iloc[permutation[0:sample_size], :]
            targs = self.targets.iloc[permutation[0:sample_size], :]

        self.optimizer_arguments['max_total_time'] = max_minutes * 60
        self.pipeline_optimizer = self.optimizer_class(**self.optimizer_arguments)
        self.fit_optimizer(feats, targs, picklePath)

    def fit_arguments(self):
        args = dict(self.config.fit_arguments())
        args['d3m_mode'] = True
        return args

    def fit_optimizer(self, feats, targs, picklePath):
        peval_callback = self.pipeline_evaluation_callback
        gen_callback = self.gen_callback
        popt = self.pipeline_optimizer

        def eval_complete_func(pl):
            score = pl.fitness.values[0]
            peval_callback(pl, score)

        popt.evaluation_completed(eval_complete_func)
        popt._observer.on_pareto_updated(lambda _: gen_callback())
        popt.fit(feats, targs, **self.fit_arguments())

    # Convenience method to make the next one shorter and easier to understand
    def _make_pipeline(self, rank, score=0, ensemble=None, pipeline=None, created=None):
        if ensemble:
            return GamaEnsemblePipeline(preamble=self.preamble_pipeline,
                                        ta3_preamble=self.ta3_preamble,
                                        fitted_preamble=self.fitted_preamble,
                                        ensemble=self.pipeline_optimizer.model,
                                        score=score,
                                        rank=rank,
                                        optimizer=self)
        else:
            return GamaPipeline(ta3_preamble=self.ta3_preamble,
                                preamble=self.preamble_pipeline,
                                fitted_preamble=self.fitted_preamble,
                                pipeline=pipeline,
                                target_dict=self.target_dict,
                                target_series=self.target_series,
                                optimizer=self,
                                score=score,
                                rank=rank,
                                created=created)


    def pipelines(self, index=None):
        # Ensure safe access to the nbest structure
        acquire = False
        try:
            acquire = self.mutex.acquire()
            top_pipelines = self.nbest.result(include_scores=True, include_timestamps=True)
        finally:
            if acquire:
                self.mutex.release()
            else:
                logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")

        def rerank_pipelines(pipelines, k=7):
            """ Performs k-fold CV on selected pipeline, re-order them by this score a sort of overfit protection.
                k should be different from 5, as that would generate the same splits as gama
            """
            from gama.genetic_programming.compilers.scikitlearn import cross_val_predict_score
            checked_top_pipelines = []
            for score, individual, created in pipelines:
                _, scores = cross_val_predict_score(
                    individual.pipeline,
                    self.pipeline_optimizer._X,
                    self.pipeline_optimizer._y,
                    self.pipeline_optimizer._metrics,
                    cv=k
                )
                checked_top_pipelines.append((scores[0], individual, created))
            checked_top_pipelines = list(sorted(checked_top_pipelines, key=lambda t: t[0], reverse=True))

            _logger.info("Comparison of pipeline ranks:")
            _logger.info(f"{'Pipeline': <20} Rank1  Rank2  Score1  Score2")
            for (i, (s1, i1, c1)) in enumerate(pipelines):
                j, (s2, i2, c2) = [(j, (s, i, c)) for j, (s, i, c) in enumerate(checked_top_pipelines)
                                   if i.pipeline_str() == i1.pipeline_str()][0]
                _logger.info(f"{i1.pipeline_str()[5:25]: <20} {i:5d}  {j:5d}  {s1:.4f}  {s2:.4f}")

            return checked_top_pipelines

        if False:
            top_pipelines = rerank_pipelines(top_pipelines)

        # Special case: The caller has requested a particular index.
        # We return a single pipeline
        if index is not None:
            if len(top_pipelines) < index + 1:
                return None
            score, pipeline, created = top_pipelines[index]
            # Index is 0 based but rank is 1 based so we must increment first
            return [self._make_pipeline(index + 1, score=score, pipeline=pipeline, created=created)]

        rank = 1
        pipelines = []

        if self.config.ensembling_enabled():
            # TODO: When we enable Ensembling we will need to experiment with creating the correct structure for TA3
            logging.error("Implement proper TA3 handling of ensemble pipelines")
            # TODO: Figure out how to come up with a good score for ensembles
            pln = self._make_pipeline(1, ensemble=self.pipeline_optimizer.model)
            _logger.info("Created ensemble pipeline %s (%d, %f): %s" %
                             (pln.name, pln.rank, pln.score, pln))
            pipelines.append(pln)
            rank += 1

        for score, pipeline, created in top_pipelines:
            pln = self._make_pipeline(rank, score=score, pipeline=pipeline, created=created)
            _logger.info("Created all pipeline %s (%d, %f): %s" %
                         (pln.name, pln.rank, pln.score, pln))
            pipelines.append(pln)
            rank += 1

        return pipelines


    def considered_pipelines(self):
        """
        Generator yielding the top-ranked pipelines
        """
        # Ensure safe access to the nbest structure
        acquire = False
        try:
            acquire = self.mutex.acquire()
            all_pipelines = self.nbest.all_items(True, True)
            for score, pipeline, created in all_pipelines:
                pln = GamaPipeline(ta3_preamble=self.ta3_preamble,
                                       preamble=self.preamble_pipeline,
                                       pipeline=pipeline,
                                       optimizer=self,
                                       score=score,
                                       created=created
                                       )
                yield pln
        finally:
            if acquire:
                self.mutex.release()
            else:
                logging.warning("Issue #31: Potential deadlock avoided - self.mutex.acquire() failed to complete")


    def get_pipeline(self, solution_id):
        solution_index = self.solution_ids_to_index[solution_id]
        _logger.info("Requesting Pipeline Description for solution_id %s and index %s" % (solution_id, solution_index))
        pipeline = self.pipelines(index=solution_index)
        if pipeline is None:
            _logger.info("Pipeline is not yet ready to describe for this solution id: %s" % solution_id)
        return pipeline


class GamaClassificationOptimizer(GamaOptimizer, ClassificationOptimizer):

    optimizer_class = GamaClassifier

    def get_optimizer_arguments(self, pipeline_eval_callback, gen_callback):
        super().get_optimizer_arguments(pipeline_eval_callback, gen_callback)
        classification_white_list_file = None
        if self.config.use_whitelist:
            classification_white_list_file = "whitelist_classification.json"
        self.optimizer_arguments['config'] = config_to_d3m(classifier_config_dict,
                                                           d3m_white_list_file=classification_white_list_file,
                                                           family="classification")

    def fit_arguments(self):
        args = super().fit_arguments()
        args['pos_label'] = self.config.pos_label
        return args

class GamaRegressionOptimizer(GamaOptimizer, RegressionOptimizer):

    optimizer_class = GamaRegressor

    def get_optimizer_arguments(self, pipeline_eval_callback, gen_callback):
        super().get_optimizer_arguments(pipeline_eval_callback, gen_callback)
        regression_white_list_file = None
        if self.config.use_whitelist:
            regression_white_list_file = "whitelist_regression.json"
        self.optimizer_arguments['config'] = config_to_d3m(regressor_config_dict,
                                                           d3m_white_list_file=regression_white_list_file,
                                                           family="regression")


class GamaTimeSeriesForecastingOptimizer(GamaOptimizer, RegressionOptimizer):

    optimizer_class = GamaTimeSeriesForecaster

    def fit_sample(self, max_minutes, picklePath, sample_size=None):
        # We never sample for time series problems.  It introduces too many difficulties.
        super().fit_sample(max_minutes, picklePath, None)

    def get_features_and_targets_from_dataset(self, dataset, skip_augmentation):
        features, targets = super().get_features_and_targets_from_dataset(dataset, skip_augmentation)

        # Now introspect the data and tell data transformation primitives to keep their hands off
        # any time columns or grouping keys
        sequestered_columns = features.metadata.list_columns_with_semantic_types([DATETIME_TYPE] + KEY_TYPES)
        if len(sequestered_columns) > 0:
            for family in TRANSFORMER_FAMILIES:
                #D3MWrapper.set_family_hyperpameters(family, exclude_columns=sequestered_columns)
                D3MWrapper.set_family_hyperpameters(family, exclude_columns=sequestered_columns,
                                                    use_semantic_types=True, return_result='append')

        # Also, as a temporary workaround for a bug in VAR, add the target type to target columns
        target_columns = targets.metadata.list_columns_with_semantic_types([TRUE_TARGET_TYPE])
        for column_index in target_columns:
            targets.metadata = targets.metadata.add_semantic_type((Base.ALL_ELEMENTS, column_index), TARGET_TYPE)

        return features, targets

    def get_optimizer_arguments(self, pipeline_eval_callback, gen_callback):
        super().get_optimizer_arguments(pipeline_eval_callback, gen_callback)
        regression_white_list_file = None
        if self.config.use_whitelist:
            regression_white_list_file = "whitelist_regression.json"
        # self.optimizer_arguments['n_jobs'] = 1
        # You can use 'tsf_config_dict' or 'tsf_config_dict_pure' below to get different behaviors
        self.optimizer_arguments['config'] = config_to_d3m(tsf_config_dict,
                                                           d3m_white_list_file=regression_white_list_file,
                                                           family="regression")


class GamaTimeSeriesClassificationOptimizer(GamaOptimizer, ClassificationOptimizer):

    optimizer_class = GamaTimeSeriesClassifier

    def fit_sample(self, max_minutes, picklePath, sample_size=None):
        # We never sample for time series problems.  It introduces too many difficulties.
        super().fit_sample(max_minutes, picklePath, None)

    def get_optimizer_arguments(self, pipeline_eval_callback, gen_callback):
        super().get_optimizer_arguments(pipeline_eval_callback, gen_callback)
        classification_white_list_file = None
        if self.config.use_whitelist:
            classification_white_list_file = "whitelist_classification.json"
        self.optimizer_arguments['config'] = config_to_d3m(classifier_config_dict,
                                                           d3m_white_list_file=classification_white_list_file,
                                                           family="classification")


