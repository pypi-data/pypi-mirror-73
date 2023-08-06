from .base import AutoflowPipelineFragment

from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes
from d3m.primitives.data_transformation.cast_to_type import Common as CastToType
from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser

from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
#TODO: This was causing an import error so we excluded it temporarily since this fragment is currently not used (Jan 16 2020)
# from d3m.primitives.data_cleaning.imputer import SKlearn as SKImputer

__all__ = ('SingleTableFragment',)

class SingleTableFragment(AutoflowPipelineFragment):

    name = "Single Table Preamble"
    description = "Common pipeline prefix for single-table problems, courtesy of Diego Martinez"
    label = "single_table"
    configuration = {}

    @classmethod
    def generate(cls, force=False):
        todf = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
        cp = SimpleColumnParser(hyperparams={})
        ext_attr = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/Attribute",)))
        ctt = CastToType(hyperparams=dict(type_to_cast='float'))
        ext_targ = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/SuggestedTarget",)))
        # TODO: This was causing an import error so we excluded it temporarily since this fragment is currently not used (Jan 16 2020)
        # hpdefaults = SKImputer.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams'].defaults()
        # imputer = SKImputer(hyperparams=hpdefaults)
        pipeline = cls.scratch_pipeline(cls.name, cls.description)
        node = pipeline.add_af_step(todf, "inputs.0")
        tnode = pipeline.add_af_step(ext_targ, node)
        node = pipeline.add_af_step(cp, node)
        node = pipeline.add_af_step(ext_attr, node)
        node = pipeline.add_af_step(ctt, node)
        # TODO: This was causing an import error so we excluded it temporarily since this fragment is currently not used (Jan 16 2020)
        # node = pipeline.add_af_step(imputer, node)
        pipeline.add_output(data_reference=node)
        pipeline.add_output(data_reference=tnode)
        return pipeline

