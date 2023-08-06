import sys
from pipelines import generate_all_yaml

force = False

if len(sys.argv) > 1:
    if sys.argv[1] != '0':
        force = True

generate_all_yaml(force)
