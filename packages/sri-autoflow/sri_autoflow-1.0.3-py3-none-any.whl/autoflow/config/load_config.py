import logging
import sys
import os
import json
from collections import defaultdict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(os.path.abspath('config'))

from sri.d3mglue.d3mwrap import D3MWrapperClassFactory
import d3m
import pkg_resources

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)

class LoadConfig(object):
    '''
    This class offers methods for loading a d3m primitive json config file and also for reconstituting the json data
    to actual primitive classes and hyper parameter values. See triage_d3m_primitives.py for entry point details.
    '''

    def __init__(self, **args):
        self._add_attrs(args)


    def _add_attrs(self, args, *attrs):
        for attr in attrs:
            if attr in args:
                setattr(self, attr, args[attr])


    def load_json(self, file):
        # This is required to make pip installed resource loading work
        my_data = pkg_resources.resource_filename(__name__, "../%s" % file)
        with open(my_data) as json_file:
            data = json.load(json_file)
            return data


    def parse_data(self, json_data, family, primitive_keys):
        new_config = defaultdict(lambda: defaultdict(list))

        for primitive in json_data:
            if primitive in primitive_keys:
                continue
            _logger.info("Parsing %s primitive" % primitive)
            package_parts = primitive.split('.')
            prim_family = package_parts[2]
            if prim_family == family:
                try:
                    primitive_obj = d3m.index.get_primitive(primitive)
                    primitive_key = D3MWrapperClassFactory(primitive_obj, primitive_obj.__name__)

                    for hyperparam in json_data[primitive]:
                        for value in json_data[primitive][hyperparam]:
                            new_config[primitive_key][hyperparam].append(value)
                except:
                    _logger.info("Failed to load primitive %s from white list - this may be due to running locally instead "
                                 "of in docker where all the primitives are available")
                    continue

        return new_config


'''
Entry point - required to make python happy
'''
if __name__ == "__main__":
    # Grab the command line parameters
    LoadConfig().main()