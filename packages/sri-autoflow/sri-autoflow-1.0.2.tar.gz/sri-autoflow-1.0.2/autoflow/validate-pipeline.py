import sys
from d3m.metadata.pipeline import Pipeline

def is_pipeline_valid_full_validation(filename):
    try:
        func = getattr(Pipeline, "from_yaml" if filename.endswith(".yml") or filename.endswith(".yaml") else "from_json")
        func(open(filename, "r")).check(allow_placeholders=False)
        return True
    except:
        return False

pfile = sys.argv[1]

passes = is_pipeline_valid_full_validation(pfile)
print("Status=%s" % passes)

