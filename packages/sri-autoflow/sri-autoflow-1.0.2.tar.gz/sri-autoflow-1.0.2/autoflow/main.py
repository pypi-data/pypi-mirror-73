import sys
import logging

# init logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
# root_logger = logging.getLogger()
# root_logger.setLevel(logging.INFO)
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s -- %(message)s'))
# stdout_handler.setLevel(logging.INFO)
# root_logger.addHandler(stdout_handler)

# https://stackoverflow.com/questions/43728431/relative-imports-modulenotfounderror-no-module-named-x
# This main script is seen as the __main__ modules so it does not know anything about belonging to a package. The
# addition of the running directory to the sys path helps the system find the autoflow package
import os
sys.path.append(os.path.dirname("."))

from autoflow.autoflowconfig import AutoflowConfig

_logger = logging.getLogger(__name__)


'''
Main entry point for the SRI TA2 command line search command
'''
def main():
    problem = sys.argv[1]
    config_file = sys.argv[2]
    statefile = None
    statefile_index = 3
    target = None
    if problem.endswith(".csv"):
        statefile_index = 4
        target = sys.argv[3]

    if len(sys.argv) > statefile_index:
        statefile = sys.argv[statefile_index]

    _logger.info("Config path %s", config_file)

    config = AutoflowConfig(problem=problem, config_file=config_file, target=target)
    optimizer = config.select_optimizer()

    if statefile is not None:
        _logger.info("Reloading state at %s" % statefile)
        optimizer.reload_state(statefile)

    _logger.info("Running SRI TA2 Search (Version 2020.05.18) on problem: %s",
                 optimizer.config.problem_id)
    optimizer.fit()
    optimizer.checkpoint()
    _logger.info("Completed Search phase for problem: %s", optimizer.config.problem_id)

    # To inform NIST/datamachines evaluation system that we have completed.
    sys.exit(0)


'''
Entry point - required to make python happy
NOTE: We cannot use the plac library here as it is not compatible with a pip installed end points
'''
if __name__ == "__main__":
    main()