import logging
import sys
import pytz
import inspect
import frozendict
import d3m.index

from d3m.metadata.pipeline import Pipeline, PrimitiveStep, SubpipelineStep, PlaceholderStep, NoResolver
from d3m.metadata.base import ArgumentType
from d3m.metadata.base import Context as D3MPipelineContext
import pipeline_pb2
from pipeline_pb2 import PipelineDescription
from pipeline_pb2 import PipelineSource
from pipeline_pb2 import PipelineDescriptionUser
from pipeline_pb2 import PipelineDescriptionInput
from pipeline_pb2 import PipelineDescriptionOutput
from pipeline_pb2 import PipelineDescriptionStep
from pipeline_pb2 import PrimitivePipelineDescriptionStep
from pipeline_pb2 import ContainerArgument
from pipeline_pb2 import StepOutput
from pipeline_pb2 import PrimitiveStepHyperparameter
from pipeline_pb2 import PrimitiveStepArgument
from primitive_pb2 import Primitive
from pipeline_pb2 import ValueArgument
from core_pb2 import DescribeSolutionResponse
from core_pb2 import PrimitiveStepDescription
from core_pb2 import SubpipelineStepDescription
from core_pb2 import StepDescription
from value_pb2 import Value
from value_pb2 import ValueRaw
from value_pb2 import ValueList
from value_pb2 import ValueDict
# from modules.pipeline_generator.utils import pipelines as pipeline_utils
# from modules.pipeline_generator.utils import custom_resolver

from google.protobuf.timestamp_pb2 import Timestamp

from pprint import pprint

# init logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)

'''
 This class offers two functions:
    1) Converts a pipeline message format from the TA3 layer to a pipeline object that TA2 can use.
    2) Converts a pipeline object from the TA2 layer to a pipeline message format that TA3 can use.
'''


class MessageConverter(object):
    """
    Main entry point so we can test calling the translator with test data
    """

    def __init__(self, resolver=None):
        self.resolver = resolver
        self.full_pipeline = False


    def main(self, argv):
        # 1. Test converting a pipeline object to a pipeline message
        if len(argv) > 1:
            test_pipeline = argv[1]
        else:
            test_pipeline = "test_pipeline2.yaml"
        with open(test_pipeline) as file:
            if test_pipeline.endswith(".yaml"):
                pipeline_description = Pipeline.from_yaml(file)
            else:
                pipeline_description = Pipeline.from_json(file)
        message_object = self.pipeline_description_message(pipeline_description)

        # 2. Test converting a pipeline message to a pipeline object
#        pipeline_message = self.create_sample_pipeline_message()
        pipeline_object = self.message_to_pipeline(message_object)
        print(pipeline_object.to_json(indent=4))


    '''
    Given a pipeline message, build and return a corresponding pipeline object for handoff to TA2
    '''
    def message_to_pipeline(self, pipeline_message=None):
        try:
            id, created, source, name, description = self._m2p_headers(pipeline_message)
            # Pass parameters directly into the constructor
            pipeline = Pipeline(pipeline_id=id, created=created,
                                source=source, name=name, description=description)

            pipeline.users   = [ self._m2p_field(um, 'id', 'reason', 'rationale')
                                for um in pipeline_message.users ]
            pipeline.inputs  = [ self._m2p_field(im, 'name')
                                for im in pipeline_message.inputs ]
            pipeline.outputs = [ self._m2p_field(om, 'name', 'data')
                                for om in pipeline_message.outputs ]
            pipeline.steps   = [ self._m2p_step(sm)
                                for sm in pipeline_message.steps ]
            return self.check_pipeline(pipeline)
        except Exception as e:
            print('Not valid template: ', e)
            return None

    def check_pipeline(self, pipeline):
        if len(pipeline.steps) == 0:
            return None
        return pipeline

    def _m2p_headers(self, pipeline_message):
        # PipelineDescription: id
        id = pipeline_message.id

        # PipelineDescription: source
        source = {
            'name': pipeline_message.source.name,
            # 'contact': pipeline_message.source.contact,
            'conteact': 'dummy@email.com',
            'pipelines': list(pipeline_message.source.pipelines)
        }

        # PipelineDescription: created
        # TA2: Timestamp when created. Templates do not have this timestamp.
        # TA3 might provide it for a fully specified pipeline.
        created = pipeline_message.created
        self.full_pipeline = created != Timestamp
        # Needed to be Datetime and when conversion timezone is missing
        created = created.ToDatetime()
        created = created.replace(tzinfo=pytz.UTC)

        # PipelineDescription: name
        name = pipeline_message.name

        # PipelineDescription: description
        description = pipeline_message.description

        return (id, created, source, name, description)



    def _m2p_field(self, msg, *fields):
        return dict((f, getattr(msg, f)) for f in fields if hasattr(msg, f))


    def _m2p_step(self, steps_message):
        # print('primitive_step', '-'*70)
        if steps_message.HasField('primitive'):
            return self._m2p_primitive_step(steps_message.primitive)
        elif steps_message.HasField('pipeline'):
            return self._m2p_subpipeline_step(steps_message.pipeline)
        elif steps_message.HasField('placeholder'):
            self.full_pipeline = False
            return self._m2p_placeholder_step(steps_message.placeholder)
        else:
            _logger.error("Error - Invalid PipelineDescriptionStep")


    def _m2p_primitive_step(self, primdescr):
        prim = primdescr.primitive
        primitive = primitive = d3m.index.get_primitive(prim.python_path)
        step = PrimitiveStep(
            primitive_description=primitive.metadata.query(),
            resolver=self.resolver
        )
        # step = PrimitiveStep(
        #     primitive_description={
        #         'id': prim.id,
        #         'version': prim.version,
        #         'python_path': prim.python_path,
        #         'name': prim.name,
        #         'digest': prim.digest
        #     },
        #     resolver=self.resolver
        # )
        step.outputs = [ om.id for om in primdescr.outputs ]
        hps = primdescr.hyperparams
        for hp in hps:
            step.add_hyperparameter(name=hp, **self._m2p_hyperparameter(hps[hp]))
        args = primdescr.arguments
        step.arguments = dict(
            (arg, self._m2p_argument(args[arg])) for arg in args
        )
        step.users = [
            self._m2p_field(um, 'id', 'reason', 'rationale') for um in primdescr.users
        ]
        return step


    def _m2p_hyperparameter(self, val):
        if val.HasField('container'):
            return dict(data=val.container.data, argument_type=ArgumentType.CONTAINER)
        elif val.HasField('data'):
            return dict(data=val.data.data, argument_type=ArgumentType.DATA)
        elif val.HasField('primitive'):
            return dict(data=val.primitive.data, argument_type=ArgumentType.PRIMITIVE)
        elif val.HasField('value'):
            return dict(data=self._m2p_hyperparam(val.value.data), argument_type=ArgumentType.VALUE)
        elif val.HasField('data_set'):
            return dict(data=[d for d in val.data_set.data], argument_type=ArgumentType.DATA)
        elif val.HasField('primitives_set'):
            return dict(data=[p for p in val.primitives_set.data], argument_type=ArgumentType.PRIMITIVE)
        else:
            _logger.error("ERROR: unrecognized hyperparameter type")
            return None

    def _m2p_value(self, val):
        if val.HasField('error'):
            return val.error.message
        elif val.HasField('dataset_uri'):
            return val.dataset_uri
        elif val.HasField('csv_uri'):
            return val.csv_uri
        elif val.HasField('pickle_uri'):
            return val.pickle_uri
        elif val.HasField('pickle_blob'):
            return val.pickle_blob
        elif val.HasField('plasma_id'):
            return val.plasma_id
        elif val.HasField('raw'):
            return self._m2p_value_raw(val.raw)
        else:
            _logger.error("ERROR: unrecognized hyperparameter type")

    def _m2p_value_raw(self, val):
        if val.HasField('null'):
            return None
        elif val.HasField('double'):
            return val.double
        elif val.HasField('int64'):
            return val.int64
        elif val.HasField('bool'):
            return val.bool
        elif val.HasField('string'):
            return val.string
        elif val.HasField('bytes'):
            return val.bytes
        elif val.HasField('list'):
            raw_list = []
            for raw in val.list.items:
                raw_list.append(self._m2p_value_raw(raw))
            return raw_list
        elif val.HasField('dict'):
            raw_dict = {}
            for key, raw in val.dict.items:
                raw_dict[key] = self._m2p_value_raw(raw)
            return raw_dict
        else:
            _logger.error("ERROR: unrecognized hyperparameter type")


    def _m2p_hyperparam(self, val):
        return self._m2p_value(val)

    def _m2p_argument(self, val):
        if val.HasField('container'):
            return dict(data=val.container.data, type=ArgumentType.CONTAINER)
        elif val.HasField('data'):
            return dict(data=val.data.data, type=ArgumentType.DATA)
        else:
            _logger.error("ERROR: unrecognized hyperparameter type")
            return None


    def _m2p_subpipeline_step(self, ppln):
        step = SubpipelineStep(pipeline_id = ppln.pipeline.id, resolver=self.resolver)
        step.inputs = [ i.data for i in ppln.inputs ]
        step.outputs = [ o.id for o in ppln.outputs ]
        return step


    def _m2p_placeholder_step(self, phldr):
        step = PlaceholderStep(resolver=self.resolver)
        step.inputs = [ i.data for i in phldr.inputs ]
        step.outputs = [ o.id for o in phldr.outputs ]
        return step


    '''
    Given a pipeline object, build and return a corresponding pipeline message for handoff to TA3
    '''
    def pipeline_description_message(self, pipeline_description):
        id, source, created, context, name, description = self._p2m_headers(pipeline_description)
        message = PipelineDescription(
            id=id,
            source=source,
            created=created,
            context=context,
            name=name,
            description=description
        )
        for user in pipeline_description.users:
            obj = message.users.add()
            self._p2m_fields(obj, user, 'id', 'reason', 'rationale')
        for inp in pipeline_description.inputs:
            obj = message.inputs.add()
            self._p2m_fields(obj, inp, 'name')
        for output in pipeline_description.outputs:
            obj = message.outputs.add()
            self._p2m_fields(obj, output, 'name', 'data')
        for step in pipeline_description.steps:
            obj = message.steps.add()
            self._p2m_step(obj, step)
        return message


    def _p2m_headers(self, pipeline_description):
        # PipelineDescription: id
        id = pipeline_description.id

        # PipelineDescription source
        sdesc = pipeline_description.source
        source = PipelineSource()
        self._p2m_fields(source, sdesc, 'name', 'contact', 'pipelines')

        # PipelineDescription: created
        # Parsing time to protobuf Timestamp()
        pipeline_created_time = pipeline_description.created.replace(tzinfo=None)
        created = Timestamp()
        created.FromDatetime(pipeline_created_time)

        # PipelineDescription: context
        context = PipelineContext.Value(
            pipeline_description.context.name
        )

        # PipelineDescription: name
        name = pipeline_description.name
        # PipelineDescription description
        description = pipeline_description.description

        return (id, source, created, context, name, description)


    def _p2m_fields(self, obj, tab, *fields):
        if tab is None:
            return
        for f in fields:
            if f in tab:
                setattr(obj, f, tab[f])


    def _p2m_step(self, mstep, step):
        # PipelineDescriptionStep: PrimitivePipelineDescriptionStep
        if isinstance(step, PrimitiveStep):
            self._p2m_primitive_step(mstep.primitive, step)
        elif isinstance(step, SubpipelineStep):
            self._p2m_subpipeline_step(mstep.pipeline, step)
        elif isinstance(step, PlaceholderStep):
            self._p2m_placeholder_step(mstep.placeholder, step)
        else:
            _logger.error("ERROR: unrecognized pipeline step")


    def _p2m_primitive_step(self, primitive, step):
        primitive_params = step.__dict__
        primitive_metadata = step.primitive.metadata.query()

        # PrimitivePipelineDescriptionStep: primitive
        self._p2m_fields(primitive.primitive, primitive_metadata,
                         'id', 'version', 'python_path', 'name', 'digest')

        # PrimitivePipelineDescriptionStep: primitive_arguments (map)
        if 'arguments' in primitive_params:
            for key, value in primitive_params['arguments'].items():
                self._p2m_argument(primitive.arguments[key], value)

        if 'outputs' in primitive_params:
            for output in primitive_params['outputs']:
                primitive.outputs.add().id = output

        if 'hyperparams' in primitive_params:
            for key, value in primitive_params['hyperparams'].items():
                self._p2m_hyperparam(primitive.hyperparams[key], value)

        if 'users' in primitive_params:
            for user in primitive_params['users']:
                obj = primitive.users.add()
                self._p2m_fields(obj, user, 'id', 'reason', 'rationale')


    def _p2m_subpipeline_step(self, msg_ppln, step):
        msg_ppln.pipeline.id = step.pipeline_id
        for i in step.inputs:
            inp = msg_ppln.inputs.add()
            inp.data = i
        for o in step.outputs:
            out = msg_ppln.outputs.add()
            out.id = o


    def _p2m_placeholder_step(self, msg_phldr, step):
        for i in step.inputs:
            inp = msg_phldr.inputs.add()
            inp.data = i
        for o in step.outputs:
            out = msg_phldr.outputs.add()
            out.id = o



    def _p2m_argument(self, arg, value):
        if value['type'] == ArgumentType.CONTAINER:
            arg.container.data = value['data']
        else:
            arg.data.data = value['data']


    def _p2m_hyperparam(self, hp, value):
        data = value['data']
        if value['type'] == ArgumentType.CONTAINER:
            hp.container.data = data
        elif value['type'] == ArgumentType.DATA:
            if type(data) is list:
                hp.data_set.data = data
            else:
                hp.data.data = data
        elif value['type'] == ArgumentType.PRIMITIVE:
            if type(data) is list:
                hp.primitives_set.data = data
            else:
                hp.primitive.data = data
        elif value['type'] == ArgumentType.VALUE:
            self._p2m_set_value(hp.value.data, data)


    def _p2m_set_value(self, vobj, data):
        dtype = type(data)
        if dtype is tuple:
            data = list(data)
            dtype = type(data)
        self._set_raw_value(vobj.raw, data)

    def _set_raw_value(self, vobj, data):
        dtype = type(data)
        if data is None:
            vobj.null = True
        elif dtype is float:
            vobj.double = data
        elif dtype is int:
            vobj.int64 = data
        elif dtype is bool:
            vobj.bool = data
        elif dtype is str:
            vobj.string = data
        elif dtype is bytes:
            vobj.bytes = data
        elif dtype is list:
            raw_list = []
            for elem in data:
                raw = ValueRaw()
                self._set_raw_value(raw, elem)
                raw_list.append(raw)
            vobj.list.items.extend(raw_list)
        elif dtype is dict:
            for key, value in data.items():
                raw = ValueRaw()
                self._set_raw_value(raw, value)
                vobj.dict.items[key] = raw
        else:
            raise NotImplementedError("Can't convert type %s" % dtype)


    def step_description_message(self, pipeline_description):
        steps = []
        for step in pipeline_description.steps:
            # StepDescription: primitive
            if isinstance(step, PrimitiveStep):
                primitive_params = step.__dict__
                primitive_hyperparams = {}
                if 'hyperparams' in primitive_params:
                    for key, value in primitive_params['hyperparams'].items():
                        value_obj = Value()
                        self._p2m_set_value(value_obj, value['data'])
                        primitive_hyperparams[key] = value_obj
                    primitive_hyperparams = PrimitiveStepDescription(
                        hyperparams=primitive_hyperparams
                    )
                steps.append(
                    StepDescription(
                        primitive=primitive_hyperparams
                    )
                )
            # StepDescription: pipeline
            if isinstance(step, SubpipelineStep):
                steps.append(
                    StepDescription(
                        pipeline=self.step_description_message(step.pipeline)
                    )
                )
        return steps

    def describe_solution(self, pipeline_description):
        # DescribeSolutionResponse: pipeline
        pipeline = self.pipeline_description_message(pipeline_description)

        # DescribeSolutionResponse: steps
        steps = self.step_description_message(pipeline_description)

        describe_solution_response = DescribeSolutionResponse(
            pipeline=pipeline,
            steps=steps
        )
        return describe_solution_response

    def solution_uri_to_describe_solution(self, solution_uri):
        pipeline_description = pipeline_utils.load_pipeline_description(solution_uri)
        # with open(solution_uri) as file:
        #     pipeline_description = Pipeline.from_json(file)

        describe_solution_response = self.describe_solution(pipeline_description)
        return describe_solution_response

    def _get_specific_keys_dict(self, keys, dict_to_trim):
        new_dict = {}
        for key in keys:
            if key in dict_to_trim:
                new_dict[key] = dict_to_trim[key]
        return new_dict

    '''
    Convenience method for building  a sample pipeline message
    '''

    def create_sample_pipeline_message(self):
        createdTime = Timestamp()
        createdTime.GetCurrentTime()
        pipeline_message = PipelineDescription(
            id="2b50a7db-c5e2-434c-b02d-9e595bd56788",
            source=PipelineSource(
                name="Test author",
                contact="mailto:test@example.com",
                pipelines=[
                    "sample pipeline1",
                    "sample pipeline2"
                ]
            ),
            created=createdTime,
            context=PipelineContext.Value('EVALUATION'),
            name="pipeline name",
            description="pipeline description",
            users=[PipelineDescriptionUser(
                id="sample id1",
                reason="sample reason1",
                rationale="sample rationale1"
            ),
                PipelineDescriptionUser(
                    id="sample id2",
                    reason="sample reason2",
                    rationale="sample rationale2"
                )
            ],
            inputs=[PipelineDescriptionInput(
                name="sample name1"
            ),
                PipelineDescriptionInput(
                    name="sample name2"
                )
            ],
            outputs=[PipelineDescriptionOutput(
                name="sample name1",
                data="sample data1"
            ),
                PipelineDescriptionOutput(
                    name="sample name2",
                    data="sample data2"
                )
            ],
            steps=[PipelineDescriptionStep(
                primitive=PrimitivePipelineDescriptionStep(
                    primitive=Primitive(
                        id="sample id1",
                        version="sample version 1",
                        python_path="sample python path 1",
                        name="sample name 1",
                        digest="sample digest"
                    ),
                    arguments={
                        'arg1': PrimitiveStepArgument(
                            container=ContainerArgument(data=' sample data')
                        ),
                        'arg2': PrimitiveStepArgument(
                            container=ContainerArgument(data=' sample data')
                        )
                    },
                    outputs=[StepOutput(
                        id="sample id1"
                    ),
                        StepOutput(
                            id="sample id1"
                        )
                    ],
                    hyperparams={
                        'param1': PrimitiveStepHyperparameter(
                            container=ContainerArgument(data='sample data')
                        )
                    },
                    users=[
                        PipelineDescriptionUser(
                            id="sample id3",
                            reason="sample reason3",
                            rationale="sample rationale3"
                        ),
                        PipelineDescriptionUser(
                            id="sample id3",
                            reason="sample reason3",
                            rationale="sample rationale3"
                        )
                    ]
                )
            ),
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="sample id1",
                            version="sample version 1",
                            python_path="sample python path 1",
                            name="sample name 1",
                            digest="sample digest"
                        )
                    )
                )
            ]
        )
        return pipeline_message


'''
Entry point - required to make python happy
'''
if __name__ == "__main__":
    MessageConverter(resolver=NoResolver()).main(sys.argv)