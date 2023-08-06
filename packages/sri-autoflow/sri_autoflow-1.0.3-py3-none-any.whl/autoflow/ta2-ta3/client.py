import grpc
import sys

import numpy

import core_pb2
import core_pb2_grpc as cpg
import logging

import problem_pb2
import value_pb2
from core_pb2 import HelloRequest, GetFitSolutionResultsRequest
from core_pb2 import SearchSolutionsRequest
from core_pb2 import GetSearchSolutionsResultsRequest
from core_pb2 import ScoreSolutionRequest
from core_pb2 import GetScoreSolutionResultsRequest
from core_pb2 import SolutionRunUser
from core_pb2 import EndSearchSolutionsRequest
from core_pb2 import ListPrimitivesRequest
from core_pb2 import SolutionExportRequest
from primitive_pb2 import Primitive

from value_pb2 import Value
from value_pb2 import ValueType

from pipeline_pb2 import PipelineDescription, PipelineSource, PipelineContext, PipelineDescriptionUser, \
    PrimitivePipelineDescriptionStep, PrimitiveStepHyperparameter, ContainerArgument, ValueArgument, \
    PlaceholderPipelineDescriptionStep, StepInput, StepOutput, PrimitiveStepArgument

from problem_pb2 import ProblemDescription
from problem_pb2 import ProblemPerformanceMetric
from problem_pb2 import PerformanceMetric
from problem_pb2 import Problem
from problem_pb2 import TaskType
from problem_pb2 import TaskSubtype
from problem_pb2 import ProblemInput
from problem_pb2 import ProblemTarget

from pipeline_pb2 import PipelineDescriptionUser
from pipeline_pb2 import PipelineDescriptionInput
from pipeline_pb2 import PipelineDescriptionOutput
from pipeline_pb2 import PipelineDescriptionStep

import time
from google.protobuf.timestamp_pb2 import Timestamp


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)

'''
This script is a dummy TA3 client the submits a bunch of messages to drive the TA2 pipeline creation process
'''
class Client(object):

    """
    Main entry point for the SRI TA2 test client
    """
    def main(self, argv):
        _logger.info("Running TA2/TA3 Interface version v2019.12.4")

        # Standardized TA2-TA3 port is 45042
        address = 'localhost:45042'
        channel = grpc.insecure_channel(address)

        # Create the stub to be used in each message call
        stub = cpg.CoreStub(channel)

        # Make a set of calls that follow the basic pipeline search
        self.basicPipelineSearch(stub)

        # See if we can retrieve the primitives from TA2
        # self.list_primitives(stub)

        # Make a call that submits a fully specified pipeline for execution
        #self.run_fully_specified_pipeline(stub)

        # Make a call that submits a place holder pipeline along with the search request
        #self.placeholder_pipeline_search(stub)


    '''
    Follow the example on the TA2-TA3 API documentation that follows the basic pipeline 
    search interation diagram. 
    '''
    def basicPipelineSearch(self, stub):
        # 1. Say Hello
        _logger.info("(1)> Calling Hello...")
        self.Hello(stub)

        # 2. Initiate Solution Search
        _logger.info("(2)> Calling SearchSolutions...")

        searchSolutionsRequest = SearchSolutionsRequest(
                user_agent="SRI Test Client",
                version="2019.12.4",
                time_bound_search=10, # minutes
                time_bound_run=10, # TODO: Use these values
                priority=0,
                allowed_value_types=[value_pb2.RAW],
                problem=ProblemDescription(problem=Problem(
                    # task_type=problem_pb2.REGRESSION,
                    task_type=problem_pb2.CLASSIFICATION,
                    task_subtype=problem_pb2.NONE,
                    performance_metrics=[
                        ProblemPerformanceMetric(
                            # metric=problem_pb2.MEAN_SQUARED_ERROR,
                            metric=problem_pb2.ACCURACY,
                            k=0,
                            pos_label="None"
                        )]
                    ),
                    inputs=[ProblemInput(
                        dataset_id="185_bl_dataset_TRAIN", # d_185_bl_dataset_TRAIN for uncharted since they create their own version of the metadata
                        targets=[
                            ProblemTarget(
                                # target_index=4,
                                target_index=17,
                                resource_id="0",
                                # column_index=4,
                                column_index=17,
                                # column_name="At_bats"
                                column_name="Hall_of_Fame"
                            )
                        ])]
                ),
            template = self.get_placeholder(),

            # inputs=[Value(dataset_uri="file:///datasets/4245637346336387598/datasetDoc.json")] # Search Solutions
            inputs=[Value(dataset_uri="file:///datasets/seed_datasets_current/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json")]
            # inputs=[Value(dataset_uri="file:///inputs/TRAIN/dataset_TRAIN/datasetDoc.json")]
        )

        search_id = self.SearchSolutions(stub, searchSolutionsRequest)
        self.results_ready = False
        _logger.info("(2)< SearchSolutions returned search_id: %s" % search_id)

        # 3. Ask for the current solutions
        solution_id = None
        _logger.info("(3)> Calling GetSearchSolutionsResults with search_id: %s" % search_id)
        while not self.results_ready:
            solution_id = self.GetSearchSolutionsResults(stub, search_id)
            if self.results_ready:
                _logger.info("(3)< GetSearchSolutionsResults returned solution_id: %s" % solution_id)
            time.sleep(5)

        # 4. Score the first of the solutions.
        _logger.info("(4)> Calling ScoreSolution with solution_id: %s" % solution_id)
        request_id = self.ScoreSolution(stub, solution_id)
        _logger.info("(4)< ScoreSolution returned request_id: %s" % request_id)

        # 5. Get Score Solution Results
        _logger.info("(5)> Calling GetScoreSolutionResults with request_id: %s" % request_id)
        self.GetScoreSolutionResults(stub, request_id)
        _logger.info("(5)< GetScoreSolutionResults returned nothing and that is ok")

        # Is this something we want to do?
        # 6. Iterate over the score solution responses
        # i = 0
        #TODO: Strangely, having iterated over this structure in the getScoreSolutionResults method the
        # scoreSolutionResults shows as empty, hmmm
        # for scoreSolutionResultsResponse in scoreSolutionResults:
        #     _logger.info("State of solution for run %s is %s" % (str(i), str(scoreSolutionResultsResponse.progress.state)))
        #     i += 1

        # 7. Call FitSolution
        _logger.info("(7)> Calling FitSolution with solution_id: %s" % solution_id)
        request_id = self.FitSolution(stub, solution_id)
        _logger.info("(7)< FitSolution returned request_id: %s" % request_id)

        # 8. Call GetFitSolutionResults
        _logger.info("(8)> Calling GetFitSolutionResults with request_id: %s" % request_id)
        fitted_solution_id = self.GetFitSolutionResults(stub, request_id)
        _logger.info("(8)< GetFitSolutionResults returned fitted_solution_id: %s" % fitted_solution_id)

        # 9. Call ProduceSolution
        _logger.info("(9)> Calling ProduceSolution with fitted_solution_id: %s" % fitted_solution_id)
        request_id = self.ProduceSolution(stub, fitted_solution_id)
        _logger.info("(9)< ProduceSolution returned request_id: %s" % request_id)

        # 10. Call GetProduceSolutionResults
        _logger.info("(10)> Calling GetProduceSolutionResults with request_id: %s" % request_id)
        self.GetProduceSolutionResults(stub, request_id)
        _logger.info("(10)< GetProduceSolutionResults returned nothing and that ok")

        # 11. Call GetProduceSolutionResults
        _logger.info("(10)> Calling SolutionExport with request_id: %s" % request_id)
        rank = 1
        self.SolutionExport(stub, solution_id, rank)
        _logger.info("(10)< SolutionExport returned nothing and that ok")

        # 12. Now that we have some results lets can the Search Solutions request
        _logger.info("(12)> Calling EndSearchSolutions with search_id: %s" % search_id)
        self.EndSearchSolutions(stub, search_id)
        _logger.info("(12)> EndSearchSolutions returned nothing and that ok")


    def placeholder_pipeline_search(self, stub):
        # 1. Say Hello
        _logger.info("(1)> Calling Hello...")
        self.Hello(stub)

        # 2. Initiate Solution Search
        _logger.info("(2)> Calling SearchSolutions with Template only...")

        searchSolutionsRequest = SearchSolutionsRequest(
            version="2018.2.27",
            allowed_value_types=[value_pb2.RAW],
            template=self.get_placeholder(),
            #            inputs=[Value(dataset_uri="file:///Users/freitag/project/d3m/stage/tpot-ta2/data/input/185_baseball/185_baseball_dataset/datasetDoc.json")]

            inputs=[Value(dataset_uri="file:///datasets/seed_datasets_current/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json")]  # Search Solutions
            # inputs=[Value(dataset_uri="file:///inputs/TRAIN/dataset_TRAIN/datasetDoc.json")]  # Search Solutions
            # inputs=[Value(dataset_uri="file:///datasets/4245637346336387598/datasetDoc.json")]  # Search Solutions
            # inputs=[Value(dataset_uri="file:///datasets/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json")]
        )

        search_id = self.SearchSolutions(stub, searchSolutionsRequest)
        self.results_ready = False
        _logger.info("(2)< SearchSolutions returned search_id: %s" % search_id)

        # 3. Ask for the current solutions
        solution_id = None
        _logger.info("(3)> Calling GetSearchSolutionsResults with search_id: %s" % search_id)
        while not self.results_ready:
            solution_id = self.GetSearchSolutionsResults(stub, search_id)
            if self.results_ready:
                _logger.info("(3)< GetSearchSolutionsResults returned solution_id: %s" % solution_id)
            time.sleep(5)

        # 4. Score the first of the solutions.
        _logger.info("(4)> Calling ScoreSolution with solution_id: %s" % solution_id)
        request_id = self.ScoreSolution(stub, solution_id)
        _logger.info("(4)< ScoreSolution returned request_id: %s" % request_id)

        # 5. Get Score Solution Results
        _logger.info("(5)> Calling GetScoreSolutionResults with request_id: %s" % request_id)
        self.GetScoreSolutionResults(stub, request_id)
        _logger.info("(5)< GetScoreSolutionResults returned nothing and that is ok")

        # Is this something we want to do?
        # 6. Iterate over the score solution responses
        # i = 0 # TODO: Strangely, having iterated over this structure in the getScoreSolutionResults method the
        # scoreSolutionResults shows as empty, hmmm
        # for scoreSolutionResultsResponse in scoreSolutionResults:
        #     _logger.info("State of solution for run %s is %s" % (str(i), str(scoreSolutionResultsResponse.progress.state)))
        #     i += 1

        # 7. Call FitSolution
        _logger.info("(7)> Calling FitSolution with solution_id: %s" % solution_id)
        request_id = self.FitSolution(stub, solution_id)
        _logger.info("(7)< FitSolution returned request_id: %s" % request_id)

        # 8. Call GetFitSolutionResults
        _logger.info("(8)> Calling GetFitSolutionResults with request_id: %s" % request_id)
        fitted_solution_id = self.GetFitSolutionResults(stub, request_id)
        _logger.info("(8)< GetFitSolutionResults returned fitted_solution_id: %s" % fitted_solution_id)

        # 9. Call ProduceSolution
        _logger.info("(9)> Calling ProduceSolution with fitted_solution_id: %s" % fitted_solution_id)
        request_id = self.ProduceSolution(stub, fitted_solution_id)
        _logger.info("(9)< ProduceSolution returned request_id: %s" % request_id)

        # 10. Call GetProduceSolutionResults
        _logger.info("(10)> Calling GetProduceSolutionResults with request_id: %s" % request_id)
        self.GetProduceSolutionResults(stub, request_id)
        _logger.info("(10)< GetProduceSolutionResults returned nothing and that ok")

        # 11. Now that we have some results lets can the Search Solutions request
        _logger.info("(11)> Calling EndSearchSolutions with search_id: %s" % search_id)
        self.EndSearchSolutions(stub, search_id)
        _logger.info("(11)> EndSearchSolutions returned nothing and that ok")


    '''
    TA3 gives us a pipeline to run, we simply pass it in, run it and give back the results.
    '''
    def run_fully_specified_pipeline(self, stub):
        # 1. Say Hello
        _logger.info("(1)> Calling Hello...")
        self.Hello(stub)

        # 2. Initiate Solution Search
        _logger.info("(2)> Calling SearchSolutions...")
        created = Timestamp()
        searchSolutionRequest = SearchSolutionsRequest(
            user_agent="SRI Test Client",
            version="2019.12.4",
            time_bound_search=10,  # minutes
            allowed_value_types=[value_pb2.RAW],
            template=self.get_fully_specified_pipeline_template(created),
            inputs=[Value(dataset_uri="file:///data/185_baseball/TRAIN/dataset_TRAIN/tables/learningData.csv")]
        )
        search_id = self.SearchSolutions(stub, searchSolutionRequest)
        self.results_ready = False
        _logger.info("(2)< SearchSolutions returned search_id: %s" % search_id)

        # 3. Ask for the current solutions
        solution_id = None
        _logger.info("(3)> Calling GetSearchSolutionsResults with search_id: %s" % search_id)
        while not self.results_ready:
            solution_id = self.GetSearchSolutionsResults(stub, search_id)
            if self.results_ready:
                _logger.info("(3)< GetSearchSolutionsResults returned solution_id: %s" % solution_id)
            time.sleep(5)

        # 4. Call FitSolution
        _logger.info("(4)> Calling FitSolution with solution_id: %s" % solution_id)
        request_id = self.FitSolution(stub, solution_id)
        _logger.info("(4)< FitSolution returned request_id: %s" % request_id)

        # 5. Call GetFitSolutionResults
        _logger.info("(5)> Calling GetFitSolutionResults with request_id: %s" % request_id)
        fitted_solution_id = self.GetFitSolutionResults(stub, request_id)
        _logger.info("(5)< GetFitSolutionResults returned fitted_solution_id: %s" % fitted_solution_id)

        # 6. Call ProduceSolution
        _logger.info("(6)> Calling ProduceSolution with fitted_solution_id: %s" % fitted_solution_id)
        request_id = self.ProduceSolution(stub, fitted_solution_id)
        _logger.info("(6)< ProduceSolution returned request_id: %s" % request_id)

        # 7. Call GetProduceSolutionResults
        _logger.info("(7)> Calling GetProduceSolutionResults with request_id: %s" % request_id)
        self.GetProduceSolutionResults(stub, request_id)
        _logger.info("(7)< GetProduceSolutionResults returned nothing and that ok")

        # 8. Now that we have some results lets can the Search Solutions request
        _logger.info("(8)> Calling EndSearchSolutions with search_id: %s" % search_id)
        self.EndSearchSolutions(stub, search_id)
        _logger.info("(8)> EndSearchSolutions returned nothing and that ok")


    def get_fully_specified_pipeline_template(self, created):
        return PipelineDescription(
            id="1b6184c1-49ba-44f8-b02d-90fb41e65e1a",
            created=created,
            inputs=[
                PipelineDescriptionInput(
                    name="dataframe"
                )],
            outputs=[
                PipelineDescriptionOutput(
                    data="steps.2.produce"
                )],
            steps=[
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="d7e14b12-abeb-42d8-942f-bdb077b4fd37",
                            version="0.1.0",
                            python_path="d3m.primitives.data_transformation.add_semantic_types.Common",
                            name="Add semantic types to columns",
                        ),
                        arguments={
                            'inputs': PrimitiveStepArgument(
                                container=ContainerArgument(data='inputs.0')
                            )
                        },
                        outputs=[StepOutput(
                            id="produce"
                        )],
                        hyperparams={
                            'columns': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    int64=0
                                                )]
                                            )
                                        )
                                    )
                                )
                            ),
                            'semantic_types': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string="http://schema.org/Integer"
                                                )]
                                            )
                                        )
                                    )
                                )
                            )
                        }
                    ),
                ),
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="d510cb7a-1782-4f51-b44c-58f0236e47c7",
                            version="0.5.0",
                            python_path="d3m.primitives.data_transformation.column_parser.Common",
                            name="Parses strings into their types",
                        ),
                        arguments={
                            'inputs': PrimitiveStepArgument(
                                container=ContainerArgument(data='steps.0.produce')
                            )
                        },
                        outputs=[StepOutput(
                            id="produce"
                        )]
                    )
                ),
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="5c9d5acf-7754-420f-a49f-90f4d9d0d694",
                            version="0.1.0",
                            python_path="d3m.primitives.operator.increment.Test",
                            name="Increment Values",
                        ),
                        arguments={
                            'inputs': PrimitiveStepArgument(
                                container=ContainerArgument(data='steps.1.produce')
                            )
                        },
                        outputs=[StepOutput(
                            id="produce"
                        )]
                    )
                )
            ]
        )

    '''
    Invoke Hello call
    '''
    def Hello(self, stub):
        reply = stub.Hello(HelloRequest())
        log_msg(reply)


    '''
    Invoke Search Solutions
    Non streaming call
    '''
    def SearchSolutions(self, stub, searchSolutionRequest):
        reply = stub.SearchSolutions(searchSolutionRequest)
        log_msg(reply)
        return reply.search_id


    '''
    Request and process the SearchSolutionsResponses
    Handles streaming reply from TA2
    '''
    def GetSearchSolutionsResults(self, stub, search_id):
        reply = stub.GetSearchSolutionsResults(GetSearchSolutionsResultsRequest(
            search_id=search_id
        ))

        for searchSolutionsResultsResponse in reply:
            log_msg(searchSolutionsResultsResponse)
            if searchSolutionsResultsResponse.progress.state == core_pb2.COMPLETED:
                self.results_ready = True
                return searchSolutionsResultsResponse.solution_id
            # Add some logging here to see what path is being followed
        return None


    '''
    For the provided Search Solution Results solution_id get the Score Solution Results Response
    Non streaming call
    '''
    def ScoreSolution(self, stub, solution_id):

        reply = stub.ScoreSolution(ScoreSolutionRequest(
            solution_id=solution_id,
            inputs=[Value(
                dataset_uri="file:///datasets/seed_datasets_current/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json"
                # dataset_uri="file:///inputs/TRAIN/dataset_TRAIN/datasetDoc.json"
                # dataset_uri="file:///datasets/5791557309150150657/datasetDoc.json"
            )],
            performance_metrics=[ProblemPerformanceMetric(
                # metric=problem_pb2.MEAN_SQUARED_ERROR
                metric=problem_pb2.F1_MICRO
            )],
            configuration=core_pb2.ScoringConfiguration(
                method=core_pb2.HOLDOUT,
                # Add in the train test split ratio to satisfy https://jira.sri.com/browse/D3M-109
                train_test_ratio=0.8
            )
        # inputs = [Value(
        #     dataset_uri="file:///datasets/5791557309150150657/datasetDoc.json")]  # Score Solutions, Produce Solution,

        ))
        return reply.request_id


    '''
    For the provided Score Solution Results Response request_id score it against some data
    Handles streaming reply from TA2
    '''
    def GetScoreSolutionResults(self, stub, request_id):

        reply = stub.GetScoreSolutionResults(GetScoreSolutionResultsRequest(
            request_id=request_id
        ))

        # Iterating here seems to kill the list - not sure why
        for scoreSolutionResultsResponse in reply:
            log_msg(scoreSolutionResultsResponse)

        return


    def FitSolution(self, stub, solution_id):
        reply = stub.FitSolution(core_pb2.FitSolutionRequest(
            solution_id=solution_id
        ))

        request_id = reply.request_id

        log_msg(reply)
        return request_id


    def GetFitSolutionResults(self, stub, request_id):
        reply = stub.GetFitSolutionResults(GetFitSolutionResultsRequest(
            request_id=request_id
        ))

        reply_list = list(reply)

        for fitSolutionResultsResponse in reply_list:
            log_msg(fitSolutionResultsResponse)

        return reply_list[0].fitted_solution_id


    def ProduceSolution(self, stub, fitted_solution_id):

        reply = stub.ProduceSolution(core_pb2.ProduceSolutionRequest(
            fitted_solution_id = fitted_solution_id,
            inputs = [
                Value(dataset_uri = "file:///datasets/seed_datasets_current/185_baseball/TRAIN/dataset_TRAIN/datasetDoc.json")
                # Value(dataset_uri = "file:///inputs/TRAIN/dataset_TRAIN/datasetDoc.json")
                # Value(dataset_uri = "file:///datasets/5791557309150150657/datasetDoc.json")
                # Value(dataset_uri = "file:///datasets/5791557309150150657/datasetDoc.json") # this path would have /d3m/data at the start when running against uncharted.
            ]
        ))

        return reply.request_id


    def GetProduceSolutionResults(self, stub, request_id):
        reply = stub.GetProduceSolutionResults(core_pb2.GetProduceSolutionResultsRequest(
            request_id = request_id
        ))
        for getProduceSolutionResultsResponse in reply:
            log_msg(getProduceSolutionResultsResponse)
            log_msg(getProduceSolutionResultsResponse.exposed_outputs)


    def EndSearchSolutions(self, stub, search_id):
        stub.EndSearchSolutions(EndSearchSolutionsRequest(
            search_id=search_id
        ))


    def SolutionExport(self, stub, solution_id, rank):
        reply = stub.SolutionExport(core_pb2.SolutionExportRequest(
            solution_id = solution_id,
            rank = rank
        ))


    def StopSearchSolutions(self):
        pass


    def UpdateProblem(self):
        pass


    def DescribeSolution(self):
        pass


    def ListPrimitives(self, stub=None):
        primitives = stub.ListPrimitives(ListPrimitivesRequest())

        for primitive in primitives.primitives:
            _logger.info(primitive)

    def get_standalone_template(self):
        timestamp = Timestamp()
        start = timestamp

        placeholder = PipelineDescription(
            name="says",
            outputs=[PipelineDescriptionOutput(
                data="steps.1.produce"
            )],
            steps=[PipelineDescriptionStep(
                primitive=PrimitivePipelineDescriptionStep(
                    primitive=Primitive(
                        id="4b42ce1e-9b98-4a25-b68e-fad13311eb65",
                        version="0.3.0",
                        python_path="d3m.primitives.datasets.DatasetToDataFrame",
                        name="Dataset to DataFrame converter",
                        digest="85b946aa6123354fe51a288c3be56aaca82e76d4071c1edc13be6f9e0e100144"
                    ),
                    arguments={
                        'inputs': PrimitiveStepArgument(
                            container=ContainerArgument(data='inputs.0')
                        )
                    },
                    outputs=[StepOutput(
                        id="produce"
                    )],
                )
            ),
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="d2fa8df2-6517-3c26-bafc-87b701c4043a",
                            version="1.1.1",
                            python_path="d3m.primitives.distil.simon",
                            name="simon",
                            digest = "0673d166f157944d3b6fdfa451f31fdfdbead7315ede3d6d9edb20f3f220b836"
                        ),
                        arguments={
                            'inputs': PrimitiveStepArgument(
                                container=ContainerArgument(data='steps.0.produce')
                            )
                        },
                        outputs=[StepOutput(
                            id="produce"
                        )],
                    )
                )
            ]
        )

        return placeholder

    def get_placeholder(self):
        timestamp = Timestamp()
        start = timestamp

        placeholder = PipelineDescription(
            # id = "08508cc5-13df-4a53-befe-7bac2e8dc880",
            # source = PipelineSource(),
            # created = start.GetCurrentTime(),
            # context = PipelineContext(),
            name = "preprocessing-d_185_bl_dataset_TRAIN-08508cc5-13df-4a53-befe-7bac2e8dc880",
            description = "Preprocessing pipeline capturing user feature selection and type information. Dataset: `d_185_bl_dataset_TRAIN` ID: `08508cc5-13df-4a53-befe-7bac2e8dc880`",
            # users = PipelineDescriptionUser(),
            # inputs = PipelineDescriptionInput(),
            outputs = [PipelineDescriptionOutput(
                data = "steps.5.produce"
            )],
            steps = [PipelineDescriptionStep(
                primitive = PrimitivePipelineDescriptionStep(
                    primitive = Primitive(
                        id = "2eeff053-395a-497d-88db-7374c27812e6",
                        version = "0.2.0",
                        python_path ="d3m.primitives.data.RemoveColumns",
                        name = "Column remover"
                    ),
                    arguments = {
                        'inputs': PrimitiveStepArgument(
                            container = ContainerArgument(data='inputs.0')
                        )
                    },
                    outputs = [StepOutput(
                        id = "produce"
                    )],
                    hyperparams = {
                        'columns': PrimitiveStepHyperparameter(
                            value = ValueArgument(
                                data = Value(
                                    raw=value_pb2.ValueRaw(
                                        list=value_pb2.ValueList(
                                            items = [value_pb2.ValueRaw(
                                                int64=1
                                            )]
                                        )))
                            )
                        ),
                        'resource_id': PrimitiveStepHyperparameter(
                            value = ValueArgument(
                                data = Value(
                                    raw=value_pb2.ValueRaw(
                                    string = "0"
                                    ))
                            )
                        )
                    }
                )
            ),
                # ab number 1
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="98c79128-555a-4a6b-85fb-d4f4064c94ab",
                            version="0.2.0",
                            python_path="d3m.primitives.data.UpdateSemanticTypes",
                            name="Semantic type updater"
                        ),
                        arguments={
                            'inputs': PrimitiveStepArgument(
                                container=ContainerArgument(data = 'steps.0.produce')
                            )
                        },
                        outputs=[StepOutput(
                            id="produce"
                        )],
                        hyperparams={
                            'add_indices': PrimitiveStepHyperparameter(
                                value= ValueArgument(
                                data = Value(
                                    raw=value_pb2.ValueRaw(
                                        list=value_pb2.ValueList(
                                            items=[value_pb2.ValueRaw(
                                                int64=1
                                            )]
                                        )))
                            )),
                            'add_types': PrimitiveStepHyperparameter(
                                value = ValueArgument(
                                data = Value(
                                    raw=value_pb2.ValueRaw(
                                        list=value_pb2.ValueList(
                                            items = [value_pb2.ValueRaw(
                                                string=""
                                            )]
                                        )))
                            )),
                            'remove_indices': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    int64=2
                                                ),
                                                    value_pb2.ValueRaw(
                                                        int64=12
                                                    )
                                                ]
                                            )))
                                )
                            ),
                            'remove_types': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string="http://schema.org/Integer"
                                                )]
                                            )))
                            )),
                            'resource_id': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data = Value(
                                        raw=value_pb2.ValueRaw(
                                            string = "0"
                                            ))
                            ))
                        }
                    )
                ),
                # ab number 2
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="98c79128-555a-4a6b-85fb-d4f4064c94ab",
                            version="0.2.0",
                            python_path="d3m.primitives.data.UpdateSemanticTypes",
                            name="Semantic type updater"
                        ),
                        arguments={
                            'inputs': PrimitiveStepArgument(
                                container=ContainerArgument(data='steps.1.produce')
                            )
                        },
                        outputs=[StepOutput(
                            id="produce"
                        )],
                        hyperparams={
                            'add_indices': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    int64 = 12
                                                )]
                                            )))
                                )),
                            'add_types': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string="http://schema.org/Float"
                                                )]
                                            )))
                                        )
                                ),
                            'remove_indices': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    int64=1
                                                )]
                                            )))
                                    )
                                ),
                            'remove_types': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string=""
                                                )]
                                            )))
                                    )
                                ),
                            'resource_id': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string="0"
                                                )]
                                            )))
                                ))
                        }
                    )
                ),
                # ab number 3
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="98c79128-555a-4a6b-85fb-d4f4064c94ab",
                            version="0.2.0",
                            python_path="d3m.primitives.data.UpdateSemanticTypes",
                            name="Semantic type updater"
                        ),
                        arguments={
                            'inputs': PrimitiveStepArgument(
                                container=ContainerArgument(data='steps.2.produce')
                            )
                        },
                        outputs=[StepOutput(
                            id="produce"
                        )],
                        hyperparams={
                            'add_indices': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    int64=1
                                                )]
                                            )))
                                    )
                                ),
                            'add_types': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string="http://schema.org/Text"
                                                )]
                                            )))
                                )),
                            'remove_indices': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    int64 = 12
                                                )]
                                            ))
                                    )
                                )),
                            'remove_types': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string=""
                                                )]
                                            )))
                                )),
                            'resource_id': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            string = "0"
                                            ))
                                ))
                        }
                    )
                ),
                # ab number 4
                PipelineDescriptionStep(
                    primitive=PrimitivePipelineDescriptionStep(
                        primitive=Primitive(
                            id="98c79128-555a-4a6b-85fb-d4f4064c94ab",
                            version="0.2.0",
                            python_path="d3m.primitives.data.UpdateSemanticTypes",
                            name="Semantic type updater"
                        ),
                        arguments={
                            'inputs': PrimitiveStepArgument(
                                container=ContainerArgument(data='steps.3.produce')
                            )
                        },
                        outputs=[StepOutput(
                            id="produce"
                        )],
                        hyperparams={
                            'add_indices': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    int64=2
                                                )]
                                            )))
                                )),
                            'add_types': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string="https://metadata.datadrivendiscovery.org/types/CategoricalData"
                                                )]
                                            )))
                                )),
                            'remove_indices': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    int64=1
                                                )]
                                            )))
                                )),
                            'remove_types': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            list=value_pb2.ValueList(
                                                items=[value_pb2.ValueRaw(
                                                    string="https://metadata.datadrivendiscovery.org/types/CategoricalData"
                                                )]
                                            )))
                                )),
                            'resource_id': PrimitiveStepHyperparameter(
                                value=ValueArgument(
                                    data=Value(
                                        raw=value_pb2.ValueRaw(
                                            string = "0"
                                            ))
                                ))
                        }
                    )
                ),
                PipelineDescriptionStep(
                    placeholder = PlaceholderPipelineDescriptionStep(
                        inputs = [StepInput(
                            data = "steps.4.produce"
                        )],
                        outputs = [StepOutput(
                            id = "produce"
                        )]
                    )
                )
             ]
        )
        return placeholder


'''
Handy method for generating pipeline trace logs
'''
def log_msg(msg):
    msg = str(msg)
    for line in msg.splitlines():
        _logger.info("    | %s" % line)
    _logger.info("    \\_____________")


'''
Entry point - required to make python happy
'''
if __name__ == "__main__":
    Client().main(sys.argv)

