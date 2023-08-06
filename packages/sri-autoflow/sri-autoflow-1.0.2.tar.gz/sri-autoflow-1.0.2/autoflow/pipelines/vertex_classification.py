from .base import AutoflowPipelineFragment

from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes
from d3m.primitives.data_transformation.remove_columns import Common as RemoveColumns
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
# Disabled by Eriq due to changed graph formats. 20200617
# from d3m.primitives.vertex_nomination.parser import SRI as VertexClassificationParser
# from d3m.primitives.vertex_classification.model import SRI as VertexClassification

__all__ = ('VertextClassificationPipeline',)

class VertexClassificationPipeline(AutoflowPipelineFragment):

    name = "SRI Vertex Classification"
    description = "PSL-based pipeline for handling vertex classification problems"
    label = "vertex_classification"
    configuration = {}

    @classmethod
    def generate(cls, force=False):
        # vnp = VertexClassificationParser(hyperparams={})
        # vn = VertexClassification(hyperparams={})
        pipeline = cls.scratch_pipeline(cls.name, cls.description)
        # node = pipeline.add_af_step(vnp, "inputs.0")
        # node = pipeline.add_af_step(vn, node)
        # pipeline.add_output(data_reference=node)
        return pipeline

