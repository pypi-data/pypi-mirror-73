# from ta2_impl import sharedValues, list_primitives, id_generator
import os
import sys
import time
import logging

from concurrent import futures

import grpc
from core_pb2_grpc import add_CoreServicer_to_server
from ta2_servicer import TA2Servicer

# from ta2c.pyclient import RegistrationHelper

# init logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)


'''
Main entry point for the SRI TA2 Server. When invoked, the config file is passed to the Main classes startServer 
method - this initiates the TA2 libraries and goes into a loop to await messages from the TA3 GRPC Client
'''
def main(argv):
    mode = argv[1]
    _logger.info("Running in %s mode" % mode)
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        server = grpc.server(executor)
        add_CoreServicer_to_server(TA2Servicer(mode=mode), server)
        # Standardized TA2-TA3 port is 45042
        server.add_insecure_port("[::]:45042")
        server.start()
        _logger.info("SRI TA2 GRPC Server (TA2-TA3 API Version 2020.6.2) ready for action - awaiting commands.")
        while True:
            time.sleep(60)

'''
Entry point - required to make python happy
'''
if __name__ == "__main__":

    # Start registration with TA2 - Coordination server - Keep! - we may need it again in the future (July 22 2019)
    # ta2c_address = "ta2c:45042"
    # address = os.getenv("ADDRESS", "sri")
    # port = 45042
    # name = "sri_ta2"
    #
    # RegistrationHelper(ta2c_address,
    #                    port,
    #                    worker_address=address,
    #                    worker_name=name)
    
    main(sys.argv)
