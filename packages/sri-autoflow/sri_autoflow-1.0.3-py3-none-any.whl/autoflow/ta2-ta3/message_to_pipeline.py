import logging
import sys
import pytz
import inspect
import frozendict

from d3m.metadata.pipeline import Pipeline, PrimitiveStep, SubpipelineStep, PlaceholderStep
from d3m.metadata.base import ArgumentType

import pipeline_pb2
from pipeline_pb2 import PipelineDescription
from pipeline_pb2 import PipelineSource
from pipeline_pb2 import PipelineDescriptionUser
from pipeline_pb2 import PipelineDescriptionInput
from pipeline_pb2 import PipelineDescriptionOutput
from pipeline_pb2 import PipelineDescriptionStep
from pipeline_pb2 import PrimitivePipelineDescriptionStep
from pipeline_pb2 import SubpipelinePipelineDescriptionStep
from pipeline_pb2 import PlaceholderPipelineDescriptionStep
from pipeline_pb2 import ContainerArgument
from pipeline_pb2 import StepOutput
from pipeline_pb2 import StepInput
from pipeline_pb2 import PrimitiveStepHyperparameter
from pipeline_pb2 import PrimitiveStepArgument
from primitive_pb2 import Primitive
from pipeline_pb2 import DataArgument
from pipeline_pb2 import PrimitiveArguments
from pipeline_pb2 import ValueArgument
from core_pb2 import DescribeSolutionResponse
from core_pb2 import PrimitiveStepDescription
from core_pb2 import SubpipelineStepDescription
from core_pb2 import StepDescription
from google.protobuf.timestamp_pb2 import Timestamp

from pprint import pprint

# init logger
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)

'''
Converts a pipeline message format from the TA3 layer to a pipeline object that TA2 can use
'''


class MessageToPipeline(object):
    """
    Main entry point so we can test calling the translator on the command line
    """

    def main(self, argv):
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
        # self.translate_message(pipeline_message)

        test_pipline = 'test_pipeline.json'
        with open(test_pipline) as file:
            pipeline_description = Pipeline.from_json(file)
        describe_solution_message = self.describe_solution(pipeline_description)
        pprint(describe_solution_message)

    def translate_message(self, pipeline_message=None):
        # PipelineDescription: id
        id = pipeline_message.id

        # PipelineDescription: source
        source = {
            'name': pipeline_message.source.name,
            'contact': pipeline_message.source.contact,
            'pipelines': pipeline_message.source.pipelines
        }

        # PipelineDescription: created
        # TA2: Timestamp when created. Templates do not have this timestamp.
        # TA3 might provide it for a fully specified pipeline.
        created = pipeline_message.created
        created_flag = created != Timestamp
        # Needed to be Datetime and when conversion timezone is missing
        created = created.ToDatetime()
        created = created.replace(tzinfo=pytz.UTC)

        # PipelineDescription: context
        # An small hack to make it work.
        context = lambda: None
        setattr(context, 'name', PipelineContext.Name(pipeline_message.context))

        # PipelineDescription: name
        name = pipeline_message.name

        # PipelineDescription: description
        description = pipeline_message.description

        # PipelineDescription: users (repeated)
        user_messages = pipeline_message.users
        users = []
        for user_message in user_messages:
            user = {
                'id': user_message.id,
                'reason': user_message.reason,
                'rationale': user_message.rationale,
            }
            users.append(user)

        # PipelineDescription: inputs (repeated)
        inputs_messages = pipeline_message.inputs
        inputs = []
        for input_message in inputs_messages:
            input = {
                'name': input_message.name
            }
            inputs.append(input)

        # PipelineDescription outputs (repeated)
        outputs_messages = pipeline_message.outputs
        outputs = []
        for outputs_message in outputs_messages:
            output = {
                'name': outputs_message.name,
                'data': outputs_message.data
            }
            outputs.append(output)

        # PipelineDescription steps (repeated)
        steps_messages = pipeline_message.steps
        steps = []
        for steps_message in steps_messages:
            step = None
            # TODO: Check to see if the hasattr will catch the different possible subclasses
            if hasattr(steps_message, 'primitive'):
                step = PrimitiveStep(
                    primitive_description={
                        'id': steps_message.primitive.primitive.id,
                        'version': steps_message.primitive.primitive.version,
                        'python_path': steps_message.primitive.primitive.python_path,
                        'name': steps_message.primitive.primitive.name,
                        'digest': steps_message.primitive.primitive.digest
                    }
                )

                # TODO: Look at this in the debugger to see what it looks like
                step.primitive = None

                outputs = []
                for output_message in steps_message.outputs:
                    output = output_message.id
                    outputs.append(output)
                step.outputs = outputs

                hyperparams = {}
                for hyperparams_message in steps_message.hyperparams:
                    hyperparam_argument = hyperparams_message.argument
                    # TODO: Inspect this for container, data, primitive etc attribute also?


            elif hasattr(steps_message, 'pipeline'):
                # step = SubpipelineStep()
                pass
            elif hasattr(steps_message, 'placeholder'):
                step = PlaceholderStep()
            else:
                _logger.error("Error - PipelineDescriptionStep had invalid attribute")
            steps.append(step)

        # Pass parameters directly into the constructor
        pipeline = Pipeline(pipeline_id=id, context=context, created=created,
                            source=source, name=name, description=description)

        # Set the attributes after object creation
        pipeline.users = users
        pipeline.inputs = inputs
        pipeline.outputs = outputs
        pipeline.steps = steps

        # pprint.pprint(pipeline.to_json_structure())
        return pipeline

    def pipeline_description_message(self, pipeline_description):
        # PipelineDescription: id
        id = pipeline_description.id
        # PipelineDescription source
        source = pipeline_description.source

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

        # PipelineDescription: users
        users = []
        for user in pipeline_description.users:
            users.append(PipelineDescriptionUser(**user))

        # PipelineDescription: inputs (repeated)
        inputs = []
        for input in pipeline_description.inputs:
            inputs.append(PipelineDescriptionInput(**input))

        # PipelineDescription: outputs (repeated)
        outputs = []
        for output in pipeline_description.outputs:
            outputs.append(PipelineDescriptionOutput(**output))

        # PipelineDescription: : steps (repeated)
        steps = []
        for step in pipeline_description.steps:

            # PipelineDescriptionStep: PrimitivePipelineDescriptionStep
            if isinstance(step, PrimitiveStep):
                primitive_params = step.__dict__
                primitive_metadata = step.primitive.metadata.query()
                # PrimitivePipelineDescriptionStep: primitive
                primitive = Primitive(
                    **self._get_specific_keys_dict(
                        ['id', 'version', 'python_path', 'name', 'digest'],
                        primitive_metadata)
                )
                # PrimitivePipelineDescriptionStep: primitive_arguments (map)
                primitive_arguments = {}

                if 'arguments' in primitive_params:
                    for key, value in primitive_params['arguments'].items():
                        data = {'data': value['data']}
                        if value['type'] == ArgumentType.CONTAINER:
                            primive_step_argument = PrimitiveStepArgument(
                                container=ContainerArgument(**data))
                        else:
                            primive_step_argument = PrimitiveStepArgument(
                                data=DataArgument(**data))

                        primitive_arguments[key] = primive_step_argument

                # PrimitivePipelineDescriptionStep: outputs (repeated)
                primitive_outputs = []
                if 'outputs' in primitive_params:
                    for output in primitive_params['outputs']:
                        primitive_outputs.append(StepOutput(id=output))

                # PrimitivePipelineDescriptionStep: hyperparams (map)
                # TODO ADD MORE HYPERPARAMS TYPES (DATASET, PRIMITIVESET)
                primitive_hyperparams = {}
                if 'hyperparams' in primitive_params:
                    for key, value in primitive_params['hyperparams'].items():
                        # ArgumentType.CONTAINER
                        if value['type'] == ArgumentType.CONTAINER:
                            primive_step_hyperparameter = PrimitiveStepHyperparameter(
                                container=ContainerArgument(
                                    data=value['data']))
                        # ArgumentType.DATA
                        if value['type'] == ArgumentType.DATA:
                            primive_step_hyperparameter = PrimitiveStepHyperparameter(
                                data=DataArgument(
                                    data=value['data']))

                        # ArgumentType.PRIMITIVE
                        if value['type'] == ArgumentType.PRIMITIVE:
                            primive_step_hyperparameter = PrimitiveStepHyperparameter(
                                primitive=PrimitiveArguments(
                                    data=value['data']))

                        # ArgumentType.DATA
                        if value['type'] == ArgumentType.VALUE:
                            primive_step_hyperparameter = ValueArgument(
                                value=ContainerArgument(
                                    data=value['data']))
                        primitive_hyperparams[key] = primive_step_hyperparameter

                primitive_users = []
                if 'users' in primitive_params:
                    for user in primitive_params['users']:
                        primitive_users.append(PipelineDescriptionUser(**user))

                steps.append(
                    PipelineDescriptionStep(
                        primitive=PrimitivePipelineDescriptionStep(
                            primitive=primitive,
                            arguments=primitive_arguments,
                            outputs=primitive_outputs,
                            hyperparams=primitive_hyperparams,
                            users=primitive_users
                        )
                    )
                )
                continue

            # PipelineDescriptionStep: SubpipelinePipelineDescriptionStep
            if isinstance(step, SubpipelineStep):

                # SubpipelinePipelineDescriptionStep: pipeline
                sub_pipeline = self.pipeline_description_message(step.pipeline)

                # SubpipelinePipelineDescriptionStep: inputs
                sub_pipeline_inputs = []
                for input in step.inputs:
                    sub_pipeline_inputs.append(StepInput(data=input))

                # SubpipelinePipelineDescriptionStep outputs
                sub_pipeline_outputs = []
                for output in step.outputs:
                    sub_pipeline_outputs.append(StepOutput(id=output))

                steps.append(
                    PipelineDescriptionStep(
                        pipeline=SubpipelinePipelineDescriptionStep(
                            pipeline=sub_pipeline,
                            inputs=sub_pipeline_inputs,
                            outputs=sub_pipeline_outputs
                        )
                    )
                )
                continue

            # PipelineDescriptionStep: PlaceholderPipelineDescriptionStep
            if isinstance(step, PlaceholderStep):
                place_holder_inputs = []
                for input in step.inputs:
                    place_holder_inputs.append(StepInput(data=input))

                place_holder_outputs = []
                for output in step.outputs:
                    place_holder_outputs.append(StepOutput(id=output))

                steps.append(
                    PipelineDescriptionStep(
                        placeholder=PlaceholderPipelineDescriptionStep(
                            inputs=place_holder_inputs,
                            outputs=place_holder_outputs
                        )
                    )
                )
                continue

        pipeline_description_message = PipelineDescription(
            id=id,
            source=source,
            created=created,
            context=context,
            name=name,
            description=description,
            users=users,
            inputs=inputs,
            outputs=outputs,
            steps=steps
        )
        return pipeline_description_message

    def step_description_message(self, pipeline_description):
        steps = []
        for step in pipeline_description.steps:
            # StepDescription: primitive
            if isinstance(step, PrimitiveStep):
                primitive_params = step.__dict__
                primitive_hyperparams = {}
                if 'hyperparams' in primitive_params:
                    for key, value in primitive_params['hyperparams'].items():
                        primitive_hyperparams[key] = value['data']
                    primitive_hyperparams = PrimitiveStepDescription(hyperparams=primitive_hyperparams)
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
        # gadgfag
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

    def _get_specific_keys_dict(self, keys, dict_to_trim):
        new_dict = {}
        for key in keys:
            if key in dict_to_trim:
                new_dict[key] = dict_to_trim[key]
        return new_dict


'''
Entry point - required to make python happy
'''
if __name__ == "__main__":
    MessageToPipeline().main(sys.argv)
