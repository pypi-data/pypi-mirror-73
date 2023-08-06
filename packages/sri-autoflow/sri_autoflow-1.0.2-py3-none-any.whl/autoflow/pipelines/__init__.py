import os.path
import pkgutil
import importlib

from d3m.metadata.pipeline import Pipeline, PrimitiveStep
from d3m.metadata.base import Context as D3MPipelineContext
from d3m.metadata.base import ArgumentType

from .base import AutoflowPipelineFragment

path = os.path.dirname(__file__)
for (module_loader, name, ispkg) in pkgutil.iter_modules([path]):
#    print(name)
    importlib.import_module('.' + name, __package__)

pipeline_classes = [cls for cls in AutoflowPipelineFragment.__subclasses__()]

def generate_all_yaml(force=False):
    for cls in pipeline_classes:
        cls.generate_yaml(force=force)


def find_pipeline_class(*, name=None, label=None):
    if name is not None:
        pipeline_class = next((cls for cls in pipeline_classes if cls.__name__ == name), None)
        if pipeline_class is not None:
            return pipeline_class
    if label is not None:
        pipeline_class = next((cls for cls in pipeline_classes if cls.label == label), None)
        if pipeline_class is not None:
            return pipeline_class
    return None


