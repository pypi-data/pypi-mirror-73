from .base import AutoflowPipelineFragment

from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes
from d3m.primitives.data_transformation.remove_columns import Common as RemoveColumns
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame

from d3m.primitives.data_transformation.conditioner import Conditioner
from common_primitives import utils

__all__ = ('SingleTableLUPIFragment',)

class SingleTableLUPIFragment(AutoflowPipelineFragment):

    name = "Single Table Preamble, SRI (LUPI)"
    description = "Common pipeline prefix for LUPI single-table problems, with SRI Conditioner"
    label = "single_table_lupi"
    configuration = dict(max_tokenized_expansion=(6, 'maximum_expansion'),
                         lupi_columns=(0, 'columns')
    )

    def study_dataset(self, dataset):
        ptype = 'https://metadata.datadrivendiscovery.org/types/SuggestedPrivilegedData'
        columns = utils.list_columns_with_semantic_types(dataset.metadata, [ptype])
        self.configure(lupi_columns=columns)
        

    @classmethod
    def generate(cls, force=False):
        todf = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
        rc = RemoveColumns(hyperparams={})
        scp = SimpleColumnParser(hyperparams={})
        cp = SimpleColumnParser(hyperparams={})
        ext_attr = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/Attribute",)))
        cond = Conditioner(hyperparams=dict(ensure_numeric=True, maximum_expansion=30))
        # ctt = CastToType(hyperparams=dict(type_to_cast='str'))
        # le = LabelEncoder(hyperparams={})

        ext_targ = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/SuggestedTarget",)))
#        hpdefaults = SKImputer.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams'].defaults()
#        imputer = SKImputer(hyperparams=hpdefaults)

        pipeline = cls.scratch_pipeline(cls.name, cls.description)

        # Get data frame
        node = pipeline.add_af_step(rc, "inputs.0")
        node = pipeline.add_af_step(todf, node)

        # Get target
        tnode = pipeline.add_af_step(ext_targ, node)
        tnode = pipeline.add_af_step(scp, tnode)
        # tnode = pipeline.add_af_step(ctt, tnode)
        # tnode = pipeline.add_af_step(le, tnode)

        # Get features
        node = pipeline.add_af_step(cp, node)
        node = pipeline.add_af_step(ext_attr, node)
        node = pipeline.add_af_step(cond, node)
#        node = pipeline.add_af_step(ctt, node)
#        node = pipeline.add_af_step(imputer, node)
        pipeline.add_output(data_reference=node)
        pipeline.add_output(data_reference=tnode)
        return pipeline

