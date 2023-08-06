import copy
import datetime
import json
import logging
import os
import pickle
import random
import string
import sys
import uuid
import traceback

import numpy
import pandas
import yaml
from d3m.metadata.base import ArgumentType
from d3m.metadata.base import Context as PipelineContext
from d3m.metadata.pipeline import Pipeline, PrimitiveStep, PlaceholderStep
from d3m.primitives.data_transformation.construct_predictions import Common as ConstructPredictions
from d3m.primitives.data_transformation.horizontal_concat import DataFrameCommon as HorizontalConcat
from d3m.primitives.data_transformation.conditioner import StaticEnsembler
if os.getenv('TPOT') is not None:
    from sri_tpot.export_utils import expr_to_tree as tpot_expr_to_tree
    from sri_tpot.export_utils import get_by_name
    from sri_tpot.operator_utils import D3MWrapperClassFactory
from d3m.primitives.data_preprocessing.label_encoder import Common as LabelEncoder
from d3m.runtime import Runtime
from d3m.metadata import base as Base
from d3m import utils

# init logger
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)

PIPELINE_FORMAT_VERSION = 'https://metadata.datadrivendiscovery.org/schemas/v0/problem.json'


def timestamp():
    ts = datetime.datetime.now(datetime.timezone.utc)
    ts = ts.astimezone(datetime.timezone.utc)
    return ts.replace(tzinfo=None).isoformat('T') + 'Z'


def get_primitive(ppath):
    mpath, pname = ppath.rsplit('.', 1)
    module = sys.modules[mpath]
    prim = getattr(module, pname)
    return prim


class AutoflowPipeline(object):
    """
    Base class representing the result of Autoflow pipeline optimization,
    essentially a wrapper around either TPOT pipelines or simple pipelines
    based on PSL graph primitives.
    """

    def __init__(self,
                 pipeline=None,
                 optimizer=None,
                 pipeline_name=None,
                 rank=None,
                 score=None,
                 created=None,
                 **args):
        """
        We assume there are two ways of instantiating a pipeline object:
           1. After optimization, and given some TPOT pipeline.
           2. Through unpickling and before testing.
        """
        self.optimizer = optimizer
        self.context = "TESTING"
        self.primitive_ids = {}
        # We're creating a new pipeline
        if pipeline_name is None:
            self.name = str(uuid.uuid4())
            # Some picklable resource, typically a TPOT pipeline
            self.pipeline = pipeline
            self.score = score
            self.rank = rank
            if created is None:
                self.created = datetime.datetime.now(datetime.timezone.utc)
            else:
                self.created = created
        # We're unpickling from file
        else:
            self.name = pipeline_name
            self.unpickle()

    def _add_attrs(self, args, *attrs):
        for attr in attrs:
            if attr in args:
                setattr(self, attr, args[attr])

    def unique_id(self):
        return str(uuid.uuid1())

    def unique_primitive_id(self, pname):
        if pname not in self.primitive_ids:
            self.primitive_ids[pname] = str(uuid.uuid1())
        return self.primitive_ids[pname]

    # TODO: This is verly likely dead code - remove on the next checkin cycle
    # def save_predictions(self, inputs, fname):
        """
        Produce predictions and save them in D3M-compliant format to
        the indicated file.
        """
        # predictions = self.produce(inputs=inputs)
        # d3mIndices = self.optimizer.config.d3m_indices(self.optimizer.dataset)
        # with open(fname, 'w') as output_file:
        #     output_file.write("d3mIndex,%s\n" % self.optimizer.config.get_target_name())
        #     TODO: This is a bogus way to do this.
            # We should really retain d3mIndexes and use them directly.
            # Fix.
            # index = 0
            # for idx, prediction in predictions.iterrows():
            #                for idx,prediction in enumerate(predictions):  We're now always a dataframe
            #     output_file.write(d3mIndices[index] + "," + str(prediction[0]) + "\n")
            #     index += 1

    # Abstract method
    def pickle(self):
        """
        Serialize yourself to file.
        """
        raise NotImplementedError()

    def pickle_attributes(self, *attrs):
        """
        Convenience method that musters and pickles just the indicated attrs
        """
        temp = "%s/%s" % (self.optimizer.config.temp, self.name)

        if not os.path.exists(temp):
            os.makedirs(temp, exist_ok=True)

        fname = "%s/%s.ppln" % (temp, self.name)
        me = {}
        for attr in attrs:
            me[attr] = getattr(self, attr)
        with open(fname, "wb") as fh:
            pickle.dump(me, fh)

    # Abstract method
    def unpickle(self):
        """
        Read in your relevant info from a pickle file.
        """
        raise NotImplementedError()

    def unpickle_attributes(self, *attrs):
        """
        Convenience method that unpickles and recovers just the indicated attrs
        """
        fname = "%s/%s/%s.ppln" % (self.optimizer.config.temp, self.name, self.name)
        me = pickle.load(open(fname, "rb"))
        for attr in attrs:
            setattr(self, attr, me[attr])

    def log(self, merely_considered=False):
        pipeline_id = self.name
        me = self.json(pipeline_id=pipeline_id)
        if merely_considered:
            outdir = self.optimizer.config.pipelines_scored
        else:
            outdir = self.optimizer.config.pipelines_ranked
        logFileName = "%s/%s.json" % (outdir, pipeline_id)
        with open(logFileName, "w") as outfile:
            outfile.write(me)
        if self.rank is not None:
            rankFileName = "%s/%s.rank" % (outdir, pipeline_id)
            with open(rankFileName, "w") as rank_outfile:
                rank_outfile.write(str(self.rank))

    # Abstract method
    def primitives(self):
        """
        Return a list of the names of primitives used in the pipeline.
        """
        raise NotImplementedError()

    # Abstract method
    def produce(self, inputs=None):
        """
        Produce predictions as a panda frame.
        """
        raise NotImplementedError()

    # Abstract method
    def add_d3m_pipeline_steps(self, pipeline):
        """
        Add pipeline steps in a subclass-specific fashion.
        """
        raise NotImplementedError()

    def add_d3m_pipeline_step(self, pipeline, prim, **args):
        pclass = type(prim)
        mdata = pclass.metadata.query()
        pstep = PrimitiveStep(primitive_description=mdata)
        pargs = mdata['primitive_code'].get('arguments', {})
        for arg, node in args.items():
            if pargs.get(arg, None) is not None:
                pstep.add_argument(arg, ArgumentType.CONTAINER, node)
        pstep.add_output("produce")
        for hp, val in prim.hyperparams.items():
            pstep.add_hyperparameter(name=hp,
                                     argument_type=ArgumentType.VALUE,
                                     data=val)
        pipeline.add_step(pstep)
        return "steps.%d.produce" % (len(pipeline.steps) - 1)

    def as_d3m_pipeline(self, name, description, pipeline_id):
        """
        Creates an instance of the D3M Pipeline class that represents
        the Autoflow pipeline.
        """
        pipeline = Pipeline(pipeline_id=pipeline_id,
                            context=PipelineContext.PRETRAINING,
                            source={
                                "name": "SRI Autoflow",
                                "contact": "mailto:freitag@ai.sri.com"
                            },
                            name=name,
                            description=description,
                            created=self.created
                            #                            pipeline_rank=self.rank
                            )
        pipeline.add_input(name="inputs")
        #        pipeline.add_input(name="targets")
        output = self.add_d3m_pipeline_steps(pipeline)
        pipeline.add_output(data_reference=output)
        return pipeline


    def json(self, pipeline_id=None):
        """
        Produce a string representation of the pipeline in D3M JSON format.
        """
        # Json serializer doesn't know what to do with int64s
        def default(o):
            if isinstance(o, numpy.int64):
                return int(o)
            if isinstance(o, numpy.bool_):
                return bool(o)
            print("Can't serialize %s of type %s" % (o, type(o)))
            raise TypeError

        obj = self.as_d3m_pipeline("Autoflow Pipeline", "Pipeline generated by Autoflow optimizer", pipeline_id)
        obj = obj.to_json_structure()
        if self.score is not None:
            obj['cross_validation_score'] = self.score

        # Recompute the digest before export since we altered the pipeline object by adding the cross_validation_score.
        obj['digest'] = utils.compute_digest(obj)

        return json.dumps(obj, indent=4, default=default)


    # Abstract method
    def __str__(self):
        """
        Define this to produce a pretty representation of the pipeline.
        """
        raise NotImplementedError()


class GraphPipeline(AutoflowPipeline):
    """
    Our treatment of graph data is slightly different, so we subclass
    to accommodate the differences.
    """

    def __init__(self, **args):
        super().__init__(**args)
        self._add_attrs(args, 'pipeline', 'fitted_pipeline', 'rank')

    """
    OBSOLETE?
    def primitives(self):
        return self.primitive_list
    """

    def produce(self, inputs=None):
        outputs = self.fitted_pipeline.produce(inputs=inputs)[0]
        target = self.optimizer.config.get_target_name()
        task_type = self.optimizer.config.taskType
        outputs = outputs.drop(columns=['d3mIndex'])
        if task_type == 'communityDetection':
            outputs[target] = outputs[target].astype(int)
        return outputs

    def add_d3m_pipeline_steps(self, pipeline):
        for step in self.pipeline.steps:
            pipeline.steps.append(step)
        return "steps.%d.produce" % (len(pipeline.steps) - 1)

    def __str__(self):
        return "%s(input_matrix)" % type(self.pipeline).__name__


class CRPipeline(AutoflowPipeline):
    def produce(self, inputs=None, need_d3m_indices=False):
        inputs_without_target = self.optimizer.remove_attribute_from_target(dataset=inputs[0])
        values = self.fitted_pipeline.produce(inputs=[inputs_without_target[0]])
        predictions = pandas.DataFrame(values.values['outputs.0'])

        # We've encoded non-integer classification targets
        # Recover original value
        if self.target_series is not None:
            # Not sure why there is a difference here in the output between GAMA and TPOT
            if self.optimizer.config.backend == "TPOT":
                predictions.iloc[:, 0] = [self.target_series[i] for i in predictions.iloc[:, 0]]
            elif self.optimizer.config.backend == "GAMA":
                predictions.iloc[:, 1] = [self.target_series[i] for i in predictions.iloc[:, 1]]
            else:
                _logger.error("Unrecognized backend %s" % self.optimizer.config.backend)

        if need_d3m_indices:
            return predictions, inputs[0]["learningData"]["d3mIndex"]
        return predictions


    '''
    This method is a workaround for TA3
    '''
    def produce_ta3(self, dataset=None, index=None):
        # Fit the pipeline before producing.
        try:
            dataset = self.optimizer.remove_attribute_from_target()
            dataset = self.optimizer.subselect_dataset(dataset)
            d3mp = self.as_d3m_pipeline("Autoflow Pipeline", "Pipeline generated by AutoFlow optimizer", None)
            self.fitted_pipeline = Runtime(d3mp, context=Base.Context.TESTING, volumes_dir=self.optimizer.config.static_volumes)
            self.fitted_pipeline.fit(inputs=[dataset[0]])
        except Exception as e:
            _logger.warning("Encountered an issue fitting pipeline: %s (%d, %f): %s" % (
            self.name, self.rank, self.score, self))
            _logger.warning("Exception %s" % str(e))
            _logger.warning(traceback.format_exc())

        inputs = [dataset[0]]
        predictions, d3m_indices = self.produce(inputs=inputs, need_d3m_indices=True)
        d3m_indices = d3m_indices.tolist()

        predictions_path = "%s/%s" % (self.optimizer.config.predictions_dir, self.name)

        if not os.path.exists(predictions_path):
            os.makedirs(predictions_path)

        predictions_file = "%s/%s" % (predictions_path, "predictions.csv")
        with open(predictions_file, 'w') as output_file:
            output_file.write("d3mIndex,%s\n" % self.optimizer.config.get_target_name())
            for idx, prediction in predictions.iterrows():
                # Not sure why there is a difference here in the output between GAMA and TPOT
                if self.optimizer.config.backend == "TPOT":
                    output_file.write(d3m_indices[idx] + "," + str(prediction[0]) + "\n")
                elif self.optimizer.config.backend == "GAMA":
                    output_file.write(d3m_indices[idx] + "," + str(prediction[1]) + "\n")
                else:
                    _logger.error("Unrecognized backend %s" % self.optimizer.config.backend)
        return predictions_file


    def __str__(self):
        return self.optimizer.clean_pipeline_string(self.pipeline)


class TPOTPipeline(CRPipeline):
    """
    Pipeline constructed from TPOT optimization
    """

    def __init__(self, **args):
        super().__init__(**args)
        self._add_attrs(args, 'preamble', 'fitted_preamble', 'fitted_pipeline',
                        'target_dict', 'target_series', 'ta3_preamble')

    def expr_to_tree(self):
        return tpot_expr_to_tree(self.pipeline, self.optimizer.pipeline_optimizer._pset)

    def add_d3m_pipeline_steps(self, pipeline):

        if hasattr(self, 'ta3_preamble') and self.ta3_preamble is not None:
            for step in self.ta3_preamble:
                if not isinstance(step, PlaceholderStep):
                    pipeline.steps.append(step)
        nsteps = len(pipeline.steps)

        def update_argument(arg):
            if nsteps == 0:
                return arg
            if arg == 'inputs.0':
                return 'steps.%d.produce' % nsteps
            else:
                steps, stepi, meth = arg.split('.')
                stepi = nsteps + int(stepi)
                return 'steps.%d.%s' % (stepi, meth)

        for step in self.preamble.steps:
            scopy = copy.copy(step)
            for arg in scopy.arguments.values():
                arg['data'] = update_argument(arg['data'])
            pipeline.steps.append(scopy)

        node = update_argument(self.preamble.outputs[0]['data'])
        target = update_argument(self.preamble.outputs[1]['data'])

        operators = self.optimizer.pipeline_optimizer.operators

        def serialize_pipeline(steps, node, depth=0):
            op = steps[0]

            if op == "CombineDFs":
                return serialize_combine(steps[1], steps[2], node)

            input_name, args = steps[1], steps[2:]
#             tpot_op = get_by_name(op, operators)
            if input_name != 'input_matrix':
                node = serialize_pipeline(input_name, node, depth + 1)
            innode = node

            tpot_op = get_by_name(op, operators)
            obj = tpot_op.instance(*args)
            node = self.add_d3m_pipeline_step(pipeline, obj._prim, inputs=node, outputs=target)

            # If the step is an estimator and is not the last step then we must
            # add its guess as synthetic feature(s)
            # classification prediction for both regression and classification
            # classification probabilities for classification if available
            if tpot_op.root and depth > 0:
                _logger.info("Adding tpot_op.root & depth > 1 horizontal Concat for %s" % self.name)
                concat = HorizontalConcat(hyperparams={})
                node = self.add_d3m_pipeline_step(pipeline, concat, left=innode, right=node)

            return node

        def serialize_combine(left, right, node):

            def make_branch(branch, node):
                if branch == "input_matrix":
                    return node
                elif branch[0] == "CombineDFs":
                    return serialize_combine(branch[1], branch[2], node)
                else:
                    tpot_op = get_by_name(branch[0], operators)
                    innode = serialize_pipeline(branch, node)
                    # We're at a depth > 1, so we simply add our predictions to the columns in the DF
                    if tpot_op.root:
                        _logger.info("Adding tpot_op.root horizontal Concat for %s" % self.name)
                        concat = HorizontalConcat(hyperparams={})
                        node = self.add_d3m_pipeline_step(pipeline, concat, left=innode, right=node)
                    # This is a transformer
                    else:
                        node = innode
                    return node

            left_node = make_branch(left, node)
            right_node = make_branch(right, node)

            _logger.info("Adding horizontal Concat for %s" % self.name)
            concat = HorizontalConcat(hyperparams={})
            node = self.add_d3m_pipeline_step(pipeline, concat, left=left_node, right=right_node)

            return node

        #        steps = interpret_tree(
        #            expr_to_tree(self.pipeline, self.optimizer.pipeline_optimizer._pset),
        #            self.optimizer.pipeline_optimizer.operators)

        steps = tpot_expr_to_tree(self.pipeline, self.optimizer.pipeline_optimizer._pset)
        node = serialize_pipeline(steps, node)

        # Find the Dataset To DataFrame step and use that as the input to the last step: ConstructPredictions. This
        # is required as the ConstructPredictions primitive needs the original input data with the d3mIndex column
        for idx, step in enumerate(pipeline.steps):
            if step.primitive.__name__ == 'DatasetToDataFramePrimitive':
                reference_step = 'steps.%s.produce' % idx

        # Add in the ConstructPredictions primitive as the last step - this will format the predictions appropriately
        format_predictions = ConstructPredictions(hyperparams={})

        # The ConstructPredictions primitive will need a reference=DataFrame during produce
        node = self.add_d3m_pipeline_step(pipeline, format_predictions, inputs=node,
                                          reference=reference_step, outputs=target)

        return node


    """
    OBSOLETE?
    def primitives(self):
        # We always use the DSBox encoder for now
        primitives = ['d3m.primitives.dsbox.Encoder'] 
        tree = expr_to_tree(self.pipeline, self.optimizer.pipeline_optimizer._pset)

        def gather_primitives(tree):
            primitive = self.qualify_primitive_name(tree[0])
            if not primitive in primitives:
                primitives.append(primitive)
            for arg in tree[1:]:
                if isinstance(arg, list):
                    gather_primitives(arg)

        return primitives
    """




class GamaPipeline(CRPipeline):
    """
    Pipeline representing the result of GAMA optimization.  We should implement the following methods in analogy
    with TPOTPipeline:
      __init__
      __str__
      pickle  (maybe OBSOLETE?)
      unpickle (maybe OBSOLETE?)
      produce: apply the pipeline, returning a set of predictions
      add_d3m_pipeline_steps: populate a D3M Pipeline object
    """

    def __init__(self, **args):
        super().__init__(**args)
        self._add_attrs(args, 'preamble', 'fitted_preamble', 'fitted_pipeline',
                        'target_dict', 'target_series', 'ta3_preamble')

    def add_d3m_pipeline_steps(self, pipeline):

        if hasattr(self, 'ta3_preamble') and self.ta3_preamble is not None:
            for step in self.ta3_preamble:
                if not isinstance(step, PlaceholderStep):
                    pipeline.steps.append(step)
        nsteps = len(pipeline.steps)

        def update_argument(arg):
            if nsteps == 0:
                return arg
            if arg == 'inputs.0':
                return 'steps.%d.produce' % nsteps
            else:
                steps, stepi, meth = arg.split('.')
                stepi = nsteps + int(stepi)
                return 'steps.%d.%s' % (stepi, meth)

        for step in self.preamble.steps:
            scopy = copy.copy(step)
            for arg in scopy.arguments.values():
                arg['data'] = update_argument(arg['data'])
            pipeline.steps.append(scopy)

        node = update_argument(self.preamble.outputs[0]['data'])
        target = update_argument(self.preamble.outputs[1]['data'])

        for primitive_node in reversed(self.pipeline.primitives):
            hp = dict((t.output, t.value) for t in primitive_node._terminals)
            obj = primitive_node._primitive.identifier(**hp)
            node = self.add_d3m_pipeline_step(pipeline, obj._prim, inputs=node, outputs=target)

        # Find the Dataset To DataFrame step and use that as the input to the last step: ConstructPredictions. This
        # is required as the ConstructPredictions primitive needs the original input data with the d3mIndex column
        reference_step = None
        for idx, step in enumerate(pipeline.steps):
            if step.primitive.__name__ == 'DatasetToDataFramePrimitive':
                reference_step = 'steps.%s.produce' % idx

        # Add in the ConstructPredictions primitive as the last step - this will format the predictions appropriately
        format_predictions = ConstructPredictions(hyperparams={})

        # The ConstructPredictions primitive will need a reference=DataFrame during produce
        node = self.add_d3m_pipeline_step(pipeline, format_predictions, inputs=node,
                                          reference=reference_step, outputs=target)

        return node


class GamaEnsemblePipeline(CRPipeline):

    def __init__(self, **args):
        super().__init__(**args)
        self._add_attrs(args, 'preamble', 'ta3_preamble', 'ensemble')

    def add_d3m_pipeline_steps(self, pipeline):

        if hasattr(self, 'ta3_preamble') and self.ta3_preamble is not None:
            for step in self.ta3_preamble:
                if not isinstance(step, PlaceholderStep):
                    pipeline.steps.append(step)
        nsteps = len(pipeline.steps)

        def update_argument(arg):
            if nsteps == 0:
                return
            data = arg['data']
            if data == 'inputs.0':
                arg['data'] = 'steps.%d.produce' % nsteps
            else:
                steps, stepi, meth = arg['data'].split('.')
                stepi = nsteps + int(stepi)
                arg['data'] = 'steps.%d.%s' % (stepi, meth)

        for step in self.preamble.steps:
            scopy = copy.copy(step)
            scopy.arguments = dict((k, update_argument(v)) for k, v in scopy.arguments.items())
            pipeline.steps.append(step)

        node = 'steps.%d.produce' % (len(pipeline.steps) - 1)
        target = self.preamble.outputs[1]['data']
        steps, stepi, meth = target.split('.')
        target = 'steps.%d.%s' % (int(stepi) + nsteps, meth)

        # A list of sub-pipeline end points with their associated weights
        pieces = [ (self._extend_d3m_pipeline(pipeline, m, node, target), w) for m,w in self.ensemble._fit_models ]

        # Create a prediction frame through a series of horizontal concats
        node = None
        weights = []
        for endpoint, weight in pieces:
            if node is None:
                node = endpoint
            else:
                concat = HorizontalConcat(hyperparams={})
                node = self.add_d3m_pipeline_step(pipeline, concat, left=node, right=endpoint)
            weights.append(weight)

        # TODO: Figure out if this is the best remedy to Issue #3 part II (regression failure)
        # if self.ensemble._metric.task_type.name is 'REGRESSION':
        #     classes = self.ensemble._y.values[:,0]
        # else:

        # Stitch them all together with an ensembler primitive
        classes = self.ensemble._one_hot_encoder.categories_[0]
        nclasses = len(classes)
        ensembler = StaticEnsembler(hyperparams=dict(weights=[float(w) for e,w in pieces], class_count=nclasses))
        node = self.add_d3m_pipeline_step(pipeline, ensembler, inputs=node)

        # Find the Dataset To DataFrame step and use that as the input to the last step: ConstructPredictions. This
        # is required as the ConstructPredictions primitive needs the original input data with the d3mIndex column
        reference_step = None
        for idx, step in enumerate(pipeline.steps):
            if step.primitive.__name__ == 'DatasetToDataFramePrimitive':
                reference_step = 'steps.%s.produce' % idx

        # Add in the ConstructPredictions primitive as the last step - this will format the predictions appropriately
        format_predictions = ConstructPredictions(hyperparams={})

        # The ConstructPredictions primitive will need a reference=DataFrame during produce
        node = self.add_d3m_pipeline_step(pipeline, format_predictions, inputs=node,
                                          reference=reference_step, outputs=target)

        return node

    def _extend_d3m_pipeline(self, pipeline, model, node, target):
        for key, operator in model.steps:
            primitive = operator._prim
            node = self.add_d3m_pipeline_step(pipeline, primitive, inputs=node, outputs=target)
        return node

    def __str__(self):
        return "Ensemble(" + " ".join("%s=%f" % (str(m), w) for m,w in self.ensemble._fit_models) + ")"
