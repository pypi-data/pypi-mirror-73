import grpc
import argparse
import operator
import os
import logging
import math
import time
import json
import signal

from ta3ta2_api import core_pb2, core_pb2_grpc, value_pb2, problem_pb2, utils
from d3m.metadata import problem as problem_module

logger = logging.getLogger(__name__)

ALLOWED_VALUE_TYPES = ['RAW']
PORT = '45042'
USER_AGENT = "test_agent"
CONNECT_TIMEOUT = 300  # seconds
CLEANUP_TIME = 60  # seconds


def signal_handler(signum, frame):
    raise TimeoutError("Timed out!")


def stop_search_signal_handler(stub, search_id):
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(CLEANUP_TIME)

    try:
        logger.warning('SearchSolution soft TIMEOUT! Stopping search {search_id}'.format(search_id=search_id))
        stub.StopSearchSolutions(stop_search_solution_request(search_id))
    except Exception:
        logger.exception('Exception stopping search, ignoring')


def hello_request():
    request = core_pb2.HelloRequest()
    return request


def search_solutions_request(problem, dataset_path, time_bound_search, rank_solutions_limit):
    version = core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]

    priority = 10

    problem_description = utils.encode_problem_description(problem)

    inputs = [
        value_pb2.Value(
            dataset_uri='file://{dataset_path}'.format(dataset_path=dataset_path)
        )
    ]

    request = core_pb2.SearchSolutionsRequest(
        user_agent=USER_AGENT,
        version=version,
        time_bound_search=time_bound_search,
        priority=priority,
        allowed_value_types=ALLOWED_VALUE_TYPES,
        problem=problem_description,
        inputs=inputs,
        rank_solutions_limit=rank_solutions_limit,
    )
    return request


def get_search_solution_results_request(search_id):
    request = core_pb2.GetSearchSolutionsResultsRequest(search_id=search_id)
    return request


def solution_export_request(solution_id, rank):
    request = core_pb2.SolutionExportRequest(
        solution_id=solution_id,
        rank=rank
    )
    return request


def describe_solution_request(solution_id):
    request = core_pb2.DescribeSolutionRequest(
        solution_id=solution_id
    )
    return request


def stop_search_solution_request(search_id):
    request = core_pb2.StopSearchSolutionsRequest(
        search_id=search_id
    )
    return request


def end_search_solution_request(search_id):
    request = core_pb2.EndSearchSolutionsRequest(
        search_id=search_id
    )
    return request


def wait_for_ta2(host_address):
    channel = None
    stub = None

    # Check if TA2 is up, try for CONNECT_TIMEOUT min
    start = time.monotonic()
    while True:
        try:
            # We create a channel every time so that GRPC back-off logic does not apply.
            channel = grpc.insecure_channel(host_address + ':' + PORT)
            stub = core_pb2_grpc.CoreStub(channel)

            logger.info('Sending Hello Message')
            stub.Hello(hello_request())
            logger.info('Hello Message Received')
            break
        except grpc.RpcError as error:
            logger.warning('Hello failed: %(error)s', {'error': error})

            # We cleanup channel for the current attempt.
            if channel is not None:
                channel.close()
                channel = None
            stub = None

            if time.monotonic() - start > CONNECT_TIMEOUT:
                raise TimeoutError('Cannot connect to {host}'.format(host=host_address + ':' + PORT)) from None

            time.sleep(1)

    assert stub

    return stub


def run(problem, dataset_path, host_address, time_bound_search, rank_solutions_limit):
    """
    A function to test the basic functionality of a TA2 though the TA3-TA2 API.

    Parameters
    ----------
    problem : dict
        A problem description to use.
    dataset_path : str
        A path to the dataset specified in the problem, dataset's ``datasetDoc.json``.
    host_address : str
        A address where the host is located.
    time_bound_search : int
        Desired upper limit of time for solution search, expressed in seconds.
    rank_solutions_limit : int
        Number of ranked solutions requested.
    """

    logger.info('Host {host}'.format(host=host_address))

    stub = wait_for_ta2(host_address)

    # List to keep track of the solutions.
    known_solutions_id = set()

    # A dictionary to keep track of solutions with ranks.
    solutions_id_rank = {}

    # Search id
    search_id = None

    # Start counting time.
    signal.signal(signal.SIGALRM, lambda signum, frame: stop_search_signal_handler(stub, search_id))
    signal.alarm(time_bound_search)
    try:
        logger.info('Sending SearchSolution Message')
        search_solutions_r = stub.SearchSolutions(
            search_solutions_request(problem, dataset_path, time_bound_search / 60, rank_solutions_limit),
        )
        search_id = search_solutions_r.search_id

        logger.info('Getting SearchSolutionsResults for {search_id}'.format(search_id=search_id))
        for get_search_solution_r in stub.GetSearchSolutionsResults(get_search_solution_results_request(search_id)):
            if get_search_solution_r.solution_id:
                solution_id = get_search_solution_r.solution_id

                if solution_id not in known_solutions_id:
                    known_solutions_id.add(solution_id)
                    logger.info('Solution found {solution_id}'.format(solution_id=solution_id))

                if solution_id not in solutions_id_rank:
                    for search_score in get_search_solution_r.scores:
                        for score in search_score.scores:
                            if score.metric and score.metric.metric and score.metric.metric == 'RANK':
                                try:
                                    rank = utils.decode_value(score.value)['value']
                                except Exception:
                                    logger.exception("Could not decode rank value.")
                                    continue

                                solutions_id_rank[solution_id] = rank

                                logger.info('Rank for {solution_id}: {rank}'.format(
                                    solution_id=solution_id, rank=rank)
                                )

                                if math.isfinite(get_search_solution_r.internal_score):
                                    logger.info('Internal score {solution_id}: {internal_score}'.format(
                                        solution_id=solution_id, internal_score=get_search_solution_r.internal_score)
                                    )

                                break

                        if solution_id in solutions_id_rank:
                            break

        # Clear alarm
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
    except TimeoutError:
        logger.warning('SearchSolution hard TIMEOUT! Exporting any ranked solutions until now')

    for solution_id in known_solutions_id:
        if solution_id not in solutions_id_rank:
            logger.warning('Solution {solution_id} is missing rank'.format(solution_id=solution_id))

    if len(solutions_id_rank) > rank_solutions_limit:
        logger.warning('TA2 returned more solutions than the limit, ignoring extra ones')

    # A set to keep track of repeated ranks
    ranks = set()

    # A dictionary that contains solutions that have the same rank.
    repeated_solutions_rank = {}

    exported_solutions_count = 0
    # We sort to make sure we export the best solutions (if more than limit of them were returned).
    for solution_id, rank in sorted(solutions_id_rank.items(), key=operator.itemgetter(1)):
        if rank in ranks:
            repeated_solutions_rank[solution_id] = rank
            continue

        ranks.add(rank)

        # There might be more solutions returned than the limit. We do not export extra ones.
        if exported_solutions_count < rank_solutions_limit:
            logger.info('Sending SolutionExport {solution_id}'.format(solution_id=solution_id))
            stub.SolutionExport(solution_export_request(solution_id, rank))
            stub.DescribeSolution(describe_solution_request(solution_id))
            exported_solutions_count += 1

    for solution_id, rank in repeated_solutions_rank.items():
        logger.warning('Solution={solution_id}, repeated rank={rank}'.format(solution_id=solution_id, rank=rank))

    try:
        logger.info('Ending search {search_id}'.format(search_id=search_id))
        stub.EndSearchSolutions(end_search_solution_request(search_id))
    except Exception:
        logger.exception('Exception ending search, ignoring')


def check_positive(value):
    _value = int(value)
    if _value <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return _value


def configure_parser(parser, *, skip_arguments=()):
    if 'problem_path' not in skip_arguments:
        parser.add_argument(
            '-p', '--problem-path', type=str, help="Path of a problemDoc.json to use."
        )

    if 'datasets_dir' not in skip_arguments:
        parser.add_argument(
            '-d', '--datasets-dir', type=str, help="Path to a directory with D3M datasets."
        )

    if 'host_address' not in skip_arguments:
        parser.add_argument(
            '-e', '--host-address', type=str, default="localhost", help="Host address. Default localhost."
        )

    if 'time_bound_search' not in skip_arguments:
        parser.add_argument(
            '-t', '--time-bound-search', type=check_positive, default=300,
            help="Desired upper limit of time for solution search, expressed in seconds."
        )

    if 'rank_solutions_limit' not in skip_arguments:
        parser.add_argument(
            '-n', '--rank-solutions-limit', type=check_positive, default=20,
            help="Number of ranked solutions requested."
        )


def main(arguments):
    # Maximum number of ranked solutions
    rank_solutions_limit = arguments.rank_solutions_limit

    # Getting time bound search on seconds
    time_bound_search = arguments.time_bound_search

    # Get host address
    host_address = arguments.host_address

    # Datasets path
    # datasets_dir = os.path.abspath(arguments.datasets_dir)

    # Problem Path
    problem = problem_module.get_problem(arguments.problem_path)

    # if len(problem['inputs']) != 1:
    #     raise RuntimeError('Expected number of datasets is 1 got {n_datasets}'.format(n_datasets=len(problem['inputs'])))
    # else:
    #     dataset_id = problem['inputs'][-1]['dataset_id']
    #
    # for dirpath, dirnames, filenames in os.walk(datasets_dir, followlinks=True):
    #     if 'datasetDoc.json' in filenames:
    #         # Do not traverse further (to not parse "datasetDoc.json" or "problemDoc.json" if they
    #         # exists in raw data filename).
    #         dirnames[:] = []
    #         dataset_path = os.path.join(os.path.abspath(dirpath), 'datasetDoc.json')
    #
    #         try:
    #             with open(dataset_path, 'r', encoding='utf8') as dataset_file:
    #                 dataset_doc = json.load(dataset_file)
    #
    #             if dataset_id == dataset_doc['about']['datasetID']:
    #                 break
    #
    #         except (ValueError, KeyError):
    #             logger.exception(
    #                 "Unable to read dataset '%(dataset)s'.", {
    #                     'dataset': dataset_path,
    #                 },
    #             )
    # else:
    #     raise ValueError('Dataset {dataset} not found'.format(dataset=dataset_id))

    logger.info('Starting TA2 run')
    run(problem=problem, dataset_path=arguments.datasets_dir, host_address=host_address,
        time_bound_search=time_bound_search, rank_solutions_limit=rank_solutions_limit)
    logger.info('Finished TA2 run')


if __name__ == '__main__':
    # Configuring logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

    # Creating parser
    parser = argparse.ArgumentParser(description="Call SRI TA2 with the SRI TA3")
    configure_parser(parser)
    arguments = parser.parse_args()

    main(arguments)
