import types
import logging
import sys
import os
import json
import d3m
from collections import defaultdict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
sys.path.append(os.path.abspath('config'))
from d3m_grid import grid as d3mgrid
TUNING_PARAMETER = 'https://metadata.datadrivendiscovery.org/types/TuningParameter'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)


class GenerateConfig(object):
    '''
    This class offers methods for parsing the d3m primitives available in the environment (docker file ususally),
    getting ranges of their hyperparameters and noting those that do not comply with the basic expected behavior. See
    triage_d3m_primitives.py for entry point details
    '''

    def __init__(self, **args):
        self._add_attrs(args)


    def _add_attrs(self, args, *attrs):
        for attr in attrs:
            if attr in args:
                setattr(self, attr, args[attr])


    def write_config(self, config, config_file):
        # import dill as pickle
        _logger.info("Writing primitive data to config file %s" % config_file)
        with open(config_file, 'w') as file_handle:
            json.dump(config, file_handle, indent=4)


    def get_primitive_categories(self):
        d3m_primitives, d3m_primitive_strings = self.load_d3m_primitives()
        return self.parse_primitive_families(d3m_primitives)


    def parse_primitive_families(self, primitives):
        primitive_families = defaultdict(lambda: defaultdict(list))

        for primitive in primitives:
            package_parts = primitive.split('.')
            if len(package_parts) < 5:
                #TODO: Write this to the blacklist
                _logger.info("Rejecting primitive due to form: %s" % primitive)
                continue
            family = package_parts[2]
            sub_type = package_parts[3]
            name = package_parts[4]
            primitive_families[family][sub_type + "." + name].append(primitive)

        return primitive_families


    def load_d3m_primitives(self, blacklist_file):
        primitives_info_strings = defaultdict(lambda: defaultdict(list))
        primitives_info = defaultdict(lambda: defaultdict(list))
        primitives = d3m.index.search()
        blacklist = set()
        for primitive in primitives:
            _logger.info("Getting hyperparameter values for Primitive %s" % primitive)
            # Use this to catch specific primitives for debugging purposes
            # if primitive == 'd3m.primitives.classification.bagging.SKlearn':
            #     _logger.info("Found d3m.primitives.classification.bagging.SKlearn! Creating pipeline...")
            try:
                primitive_obj = d3m.index.get_primitive(primitive)
            except:
                continue
            mdata = primitive_obj.metadata.query()
            if hasattr(primitive_obj, 'metadata'):
                hyperparams_metadata = primitive_obj.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
                hyperparams_with_defaults = hyperparams_metadata.defaults()

                hyperparams = primitive_obj.metadata.query()['primitive_code']['hyperparams']
                for hyperparam in hyperparams:
                    if hyperparam not in hyperparams_with_defaults:
                        continue

                    # Start by adding the hyperparam with its default value - later we will generate value ranges
                    value = primitive_obj.metadata.query()['primitive_code']['hyperparams'][hyperparam]['default']

                    hpsclass = mdata['primitive_code']['class_type_arguments']['Hyperparams']
                    hpclass = hpsclass.configuration[hyperparam]

                    # Validate the hyper param value and dump out the bad ones
                    try:
                        hyperparams_metadata.configuration[hyperparam].validate(value)
                    except (d3m.exceptions.InvalidArgumentTypeError, d3m.exceptions.InvalidArgumentValueError):
                        print('Throwing out {}.{}={}'.format(primitive, hyperparam, value))
                        blacklist.add(primitive)
                        continue

                    values = list()
                    # Don't search control parameters
                    if TUNING_PARAMETER not in hpclass.semantic_types:
                        # When a hyperparam is a tuning parameter, just add its default value so that the initialization
                        # of the primitive does not fail immediately
                        values.append(
                            primitive_obj.metadata.query()['primitive_code']['hyperparams'][hyperparam]['default'])
                    else:
                        try:
                            values = d3mgrid(hpclass)
                        except Exception as e:
                            # Since we ran into difficulty generating a range of values we will just use the default.
                            values.append(primitive_obj.metadata.query()['primitive_code']['hyperparams'][hyperparam]['default'])

                    for value in values:
                        # Validate the hyper param value and dump out the bad ones
                        try:
                            hyperparams_metadata.configuration[hyperparam].validate(value)
                        except Exception as e:
                            continue
                            # logging.info("Caught exception while generating hyperparameter values for primitive %s hyperparam %s" % (primitive, hyperparam))

                        # Get the class data for validation
                        primitives_info[primitive][hyperparam].append(value)

                        # Stringify the classes for export to json
                        # if isinstance(value, (type, types.ClassType)) or type(value) is d3m.primitives.classification.gradient_boosting.SKlearn:
                        #     value = str(value)

                        # _logger.info("Writing %s, %s, %s" % (primitive, hyperparam, value))
                        primitives_info_strings[primitive][str(hyperparam)].append(str(value))

        blacklist_file_handle = open(blacklist_file, "a+")

        for prim in blacklist:
            blacklist_file_handle.write("%s\t%s\n" % (prim, "failed hyperparameter validation"))
            if (primitives_info.__contains__(prim)):
                primitives_info.pop(prim)
                primitives_info_strings.pop(prim)

        blacklist_file_handle.close()
        return primitives_info, primitives_info_strings


'''
Entry point - required to make python happy
'''
if __name__ == "__main__":
    # Grab the command line parameters
    GenerateConfig().main()