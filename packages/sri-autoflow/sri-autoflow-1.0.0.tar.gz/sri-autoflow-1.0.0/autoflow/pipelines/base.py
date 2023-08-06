import os.path
import inspect
import logging
import copy
import stopit

from d3m.metadata.pipeline import Pipeline, PrimitiveStep
from d3m.metadata.base import Context as D3MPipelineContext
from d3m.metadata.base import ArgumentType
from d3m.runtime import Runtime

# from datamart_isi.entries import Datamart, DatamartSearchResult
# import datamart
# import datamart_nyu
# import datamart_isi
from common_primitives.datamart_augment import Hyperparams as hyper_augment, DataMartAugmentPrimitive

# DATAMART_URI = "http://dsbox02.isi.edu:9001/blazegraph/namespace/datamart4/sparql"

ENTRY_POINT_TYPE = 'https://metadata.datadrivendiscovery.org/types/DatasetEntryPoint'
ATTRIBUTE_TYPE = "https://metadata.datadrivendiscovery.org/types/Attribute"
SUGGESTED_TARGET_TYPE = "https://metadata.datadrivendiscovery.org/types/SuggestedTarget"
TRUE_TARGET_TYPE = "https://metadata.datadrivendiscovery.org/types/TrueTarget"
TARGET_TYPE = "https://metadata.datadrivendiscovery.org/types/Target"
PRIMARY_KEY_TYPE = 'https://metadata.datadrivendiscovery.org/types/PrimaryKey'
GROUPING_KEY_TYPE = 'https://metadata.datadrivendiscovery.org/types/GroupingKey'
UNIQUE_KEY_TYPE = 'https://metadata.datadrivendiscovery.org/types/UniqueKey'
PRIMARY_MULTI_KEY_TYPE = 'https://metadata.datadrivendiscovery.org/types/PrimaryMultiKey'
SUGGESTED_GROUPING_KEY_TYPE = 'https://metadata.datadrivendiscovery.org/types/SuggestedGroupingKey'

BOOLEAN_TYPE = 'http://schema.org/Boolean'
CATEGORICAL_TYPE = 'https://metadata.datadrivendiscovery.org/types/CategoricalData'
INTEGER_TYPE = 'http://schema.org/Integer'
FLOAT_TYPE = 'http://schema.org/Float'
FLOAT_VECTOR_TYPE = 'https://metadata.datadrivendiscovery.org/types/FloatVector'
DATETIME_TYPE = 'http://schema.org/DateTime'
TEXT_TYPE = 'http://schema.org/Text'

KEY_TYPES = [PRIMARY_KEY_TYPE, GROUPING_KEY_TYPE, UNIQUE_KEY_TYPE, PRIMARY_MULTI_KEY_TYPE, SUGGESTED_GROUPING_KEY_TYPE]
SCALAR_TYPES = [BOOLEAN_TYPE, CATEGORICAL_TYPE, INTEGER_TYPE, FLOAT_TYPE, DATETIME_TYPE]


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)


class AutoflowPipelineFragment(Pipeline):

    name = None
    description = None
    configuration = {}
    outputs = {}

    # Set to the name of the file containing my pipeline spec
    label = None

    def to_json_structure(self, **kwargs):
        obj = super().to_json_structure(**kwargs)
        if hasattr(self, 'label'):
            obj['autoflow'] = {}
            obj['autoflow']['label'] = self.label
        return obj

    def has_configuration_option(self, hp):
        return hp in self.configuration

    def configure(self, **config):
        for key, val in config.items():
            stepi, hp = self.configuration[key]
            # if stepi >= self.augmentation_start:
            #     stepi += self.augmentation_steps
            step = self.steps[stepi]
            step.hyperparams[hp] = dict(type=ArgumentType.VALUE, data=val)
#            step.add_hyperparameter(name=hp, argument_type=ArgumentType.VALUE, data=val)

    def study_dataset(self, dataset):
        pass

    def generate_dataset_steps(self):
        raise NotImplementedError()

    def perform_augmentation(self, node, hints=None, config=None):
        self.augmentation_start = len(self.steps)
        self.augmentation_steps = 0

        if hints is None or config is None:
            return node

        provider = config.datamart_service()
        if provider is None:
            return node

        datamart_url = config.datamarts[provider]

        if provider == 'ISI':
            dm = Datamart(connection_url=datamart_url)
            query = None
        elif provider == 'NYU':
            dm = datamart_nyu.RESTDatamart(datamart_url)
            query = datamart.DatamartQuery(keywords=hints[0]['domain'], variables=[])
        else:
            raise NotImplementedError("Unknown datamart: %s" % provider)

        _logger.info("Performing augmentation: %s" % provider)

        dc = self.execute(node, config.static_volumes)

        cursor = None
        with stopit.ThreadingTimeout(300):
            cursor = dm.search_with_data(query=query, supplied_data=dc)

        if cursor is None:
            _logger.error("%s datatmart returned no result: aborting augmentation" % provider)
            return node

        _logger.info("Received a cursor from datamart")

        try:
            with stopit.ThreadingTimeout(300, swallow_exc=False):
                search_results = cursor.get_next_page(timeout=295)
        except stopit.TimeoutException:
            _logger.error("get_next_page timed out: aborting augmentation")
            return node
        except:
            _logger.error("get_next_page call failed: aborting augmentation")
            return node

        if search_results is None:
            _logger.info("Augmentation returned no results")
            return node

        _logger.info("Got some results back")

        search_results = sorted(search_results, key=lambda sr: sr.score(), reverse=True)

        hp_defaults = hyper_augment.defaults()
        hp_defaults = hp_defaults.replace({"system_identifier": provider})

        for result in search_results:
            hps = hp_defaults.replace({"search_result": result.serialize()})
            prim = DataMartAugmentPrimitive(hyperparams=hps)
            node = self.add_af_step(prim, node)
            self.augmentation_steps += 1
            # TODO: Experiment with different policies here
            if self.augmentation_steps >= 3:
                break

        _logger.info("Added %d augmentation steps" % self.augmentation_steps)

        return node


    def perform_augmentation_nyu(self, node, hints=None, config=None):

        _logger.info("Performing augmentation: NYU")

        dc = self.execute(node)
        url = config.datamarts['NYU']
        dm = datamart_nyu.RESTDatamart(url)
        cursor = dm.search_with_data(
            query=datamart.DatamartQuery(
                keywords=hints[0]['domain'],
                variables=[],
            ),
            supplied_data=dc,
        )
        search_results = cursor.get_next_page()

        _logger.info("Got some results back")

        hp_defaults = hyper_augment.defaults()
        hp_defaults = hp_defaults.replace({"system_identifier": "NYU"})

        for result in search_results:
            hps = hp_defaults.replace({"search_result": result.serialize()})
            prim = DataMartAugmentPrimitive(hyperparams=hps)
            node = self.add_af_step(prim, node)
            self.augmentation_steps += 1
            break

        return node

    def perform_augmentation_isi(self, node, hints=None, config=None):

        _logger.info("Performing augmentation: ISI")

        # Set HPs to contact ISI datamart
        hp_defaults = hyper_augment.defaults()
        hp_defaults = hp_defaults.replace({"system_identifier": "ISI"})

        wikifier = DatamartSearchResult(search_result={}, supplied_data=None, query_json={}, search_type="wikifier")
        hps = hp_defaults.replace({"search_result": wikifier.serialize()})
        prim = DataMartAugmentPrimitive(hyperparams=hps)
        node = self.add_af_step(prim, node)
        self.augmentation_steps += 1

        dataset = self.execute(node)
        augment_res = prim.produce(inputs=dataset).value

        # run search, it will return wikidata search results first (if found)
        # and then the general search results with highest score first
        datamart = Datamart(connection_url=DATAMART_URI)
        search_unit = datamart.search_with_data(query=None, supplied_data=augment_res)
        results = search_unit.get_next_page(timeout=60)

        for result in (r for r in results if r.search_type == "wikidata"):
            hps = hp_defaults.replace({"search_result": result.serialize()})
            prim = DataMartAugmentPrimitive(hyperparams=hps)
            node = self.add_af_step(prim, node)
            self.augmentation_steps += 1

        results.sort(key=lambda x: x.score(), reverse=True)
        for result in (r for r in results if r.search_type == "general"):
            hps = hp_defaults.replace({"search_result": result.serialize()})
            prim = DataMartAugmentPrimitive(hyperparams=hps)
            node = self.add_af_step(prim, node)
            self.augmentation_steps += 1
            break

        return node

    def generate_dataframe_steps(self, node):
        raise NotImplementedError()

    def execute(self, node, static_volumes):
        copyself = copy.deepcopy(self)
        copyself.add_output(data_reference=node)
        _logger.info("Static volume is: %s" % static_volumes)
        rt = Runtime(copyself, context=D3MPipelineContext.TESTING, volumes_dir=static_volumes)
        rt.fit(inputs=[self.dataset])
        result = rt.produce(inputs=[self.dataset])
        return result.values['outputs.0']

    # Todo: Implement this, which will be the primary access point to preambles by the optimizer
    def process_dataset(self, dataset):
        pass

    @classmethod
    def get_instance(cls):
        myyaml = cls.get_yaml_path()
        with open(myyaml, "r") as fh:
            pipeline = Pipeline.from_yaml(fh)
        pipeline.__class__ = cls
        return pipeline

    @classmethod
    def get_yaml_path(cls):
        if cls.label is None:
            raise NotImplementedError()
        mydir = os.path.dirname(__file__)
        return "%s/pipelines/%s.yaml" % (mydir, cls.label)

    @classmethod
    def yaml_up_to_date(cls):
        myyaml = cls.get_yaml_path()
        try:
            clsfile = inspect.getfile(cls)
#            print("Testing for up-to-date")
#            print(clsfile)
            my_mtime = os.path.getmtime(clsfile)
            yaml_mtime = os.path.getmtime(myyaml)
#            print(cls, my_mtime, yaml_mtime)
            return yaml_mtime > my_mtime
        except:
            return False

    @classmethod
    def generate(cls, dataset, augmentation_hints=None, config=None):
        self = cls.scratch_pipeline(cls.name, cls.description)
        self.dataset = dataset
        node = self.generate_dataset_steps()
        # _logger.info("About to perform augmentation")
        # node = self.perform_augmentation(node, hints=augmentation_hints, config=config)
        # _logger.info("Augmentation complete")
        node, target_node, retained_target_node = self.generate_dataframe_steps(node)
        _logger.info("Generate Dataframe Steps complete")
        self.add_output(data_reference=node)
        self.add_output(data_reference=target_node)
        self.add_output(data_reference=retained_target_node)
        self.config = config
        return self

    @classmethod
    def generate_yaml(cls, force=False):
        """
        Produce a serialization to the yaml file for this class. 
        If the on-disk representation already
        exists, this method declines to produce a new one, unless force=True.
        """
        if cls.yaml_up_to_date() and not force:
            return
        pipeline = cls.generate()
        path = cls.get_yaml_path()
        with open(path, "w") as fh:
            pipeline.to_yaml(fh)
        print("%s: generated YAML" % cls.__name__)


    ##############################################################
    # Convenience methods for generating pipelines in code
    ##############################################################

    @classmethod
    def scratch_pipeline(cls, name, description):
        pipeline = Pipeline(None, 
                            context=D3MPipelineContext.PRETRAINING,
                            source= {
                                "name": "SRI Autoflow",
                                "contact": "mailto:freitag@ai.sri.com"
#                                "from": "scratch"
                            },
                            name=cls.name,
                            description=cls.description)
        pipeline.add_input(name="inputs")
        pipeline.__class__ = cls
        return pipeline

    def add_af_step(self, prim, node, **oinputs):
        pclass = type(prim)
        mdata = pclass.metadata.query()
        pstep = PrimitiveStep(primitive_description=mdata)
        pstep.add_argument("inputs", ArgumentType.CONTAINER, node)
        for arg, onode in oinputs.items():
            pstep.add_argument(arg, ArgumentType.CONTAINER, onode)
        pstep.add_output("produce")
        for k, v in prim.hyperparams.items():
#            print(k, v)
            pstep.add_hyperparameter(name=k, argument_type=ArgumentType.VALUE, data=v)
        self.add_step(pstep)
        return "steps.%d.produce" % (len(self.steps)-1)

