from .base import AutoflowPipelineFragment

from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes

from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.data_transformation.conditioner import Conditioner
from d3m.primitives.data_preprocessing.dataset_text_reader import DatasetTextReader

__all__ = ('SemiSupervisedTableSRIFragment',)

class SemiSupervisedTableSRIFragment(AutoflowPipelineFragment):

    name = "Semi Supervised Table Preamble, SRI"
    description = "Common pipeline prefix for semi supervised problems, with SRI Conditioner"
    label = "semi_supervised_sri"
    configuration = dict(max_tokenized_expansion=(6, 'maximum_expansion'))

    @classmethod
    def generate(cls, force=False):
        tr = DatasetTextReader(hyperparams={})
        todf = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
        cp = SimpleColumnParser(hyperparams={})
        ext_attr = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/Attribute",)))
        cond = Conditioner(hyperparams=dict(ensure_numeric=True, maximum_expansion=30))
        ext_targ = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/SuggestedTarget",)))
        pipeline = cls.scratch_pipeline(cls.name, cls.description)

        node = pipeline.add_af_step(tr, "inputs.0")
        node = pipeline.add_af_step(todf, node)

        # Extract target
        tnode = pipeline.add_af_step(ext_targ, node)
        tnode = pipeline.add_af_step(cp, tnode)

        # Extract features
        node = pipeline.add_af_step(cp, node)
        node = pipeline.add_af_step(ext_attr, node)
        node = pipeline.add_af_step(cond, node)
        pipeline.add_output(data_reference=node)
        pipeline.add_output(data_reference=tnode)
        return pipeline

