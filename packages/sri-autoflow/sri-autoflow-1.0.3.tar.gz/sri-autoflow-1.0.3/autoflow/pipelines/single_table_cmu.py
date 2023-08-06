from .base import AutoflowPipelineFragment, SCALAR_TYPES, ATTRIBUTE_TYPE, SUGGESTED_TARGET_TYPE

from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes

from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.data_transformation.conditioner import Conditioner
#TODO: This was causing an import error so we excluded it temporarily since this fragment is currently not used (Jan 16 2020)
# from d3m.primitives.data_cleaning.imputer import SKlearn as SKImputer
#from d3m.primitives.data_preprocessing.dataset_text_reader import DatasetTextReader
#TODO: Re-enable the AutoRPI primitive if RPIU resubmits it for 20200109 AND if we use this fragment again (currently are not)
# from d3m.primitives.feature_selection.joint_mutual_information import AutoRPI as MIFeatureSelector
#from d3m.primitives.data_transformation.one_hot_encoder import SKlearn as OneHotEncoder

__all__ = ('SingleTableSRIFragmentCMU',)

class SingleTableSRIFragmentCMU(AutoflowPipelineFragment):

    name = "Single Table Preamble, SRI"
    description = "Common pipeline prefix for single-table problems"
    label = "single_table_sri_2"
#    configuration = dict(max_tokenized_expansion=(6, 'maximum_expansion'))

    def generate_dataset_steps(self):
        return "inputs.0"

    def generate_dataframe_steps(self, node):
        todf = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
        scp = SimpleColumnParser(hyperparams={})
        cp = SimpleColumnParser(hyperparams=dict(parse_semantic_types=tuple(SCALAR_TYPES)))
        ext_attr = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(ATTRIBUTE_TYPE,)))
        # TODO: This was causing an import error so we excluded it temporarily since this fragment is currently not used (Jan 16 2020)
        # imp_defaults = dict(SKImputer.metadata.get_hyperparams().defaults())
        # imp = SKImputer(hyperparams=imp_defaults)
#        cond = Conditioner(hyperparams=dict(ensure_numeric=True, maximum_expansion=30))
#         fs_defaults = dict(MIFeatureSelector.metadata.get_hyperparams().defaults())
#         fs_defaults['method'] = 'pseudoBayesian'
#         fs_defaults['nbins'] = 2
#         fs = MIFeatureSelector(hyperparams=fs_defaults)
#        ohehp = dict(OneHotEncoder.metadata.get_hyperparams().defaults())
#        ohehp['use_semantic_types'] = True
#        ohehp['handle_unknown'] = 'ignore'
#        ohe = OneHotEncoder(hyperparams=ohehp)
        ext_targ = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(SUGGESTED_TARGET_TYPE,)))

        # Get a dataframe
        node = self.add_af_step(todf, node)

        # Extract target
        tnode = self.add_af_step(ext_targ, node)
        rtnode = tnode
        tnode = self.add_af_step(scp, tnode)

        # Extract features
        node = self.add_af_step(cp, node)
        node = self.add_af_step(ext_attr, node)
        # node = self.add_af_step(fs, node, outputs=tnode)
        # TODO: This was causing an import error so we excluded it temporarily since this fragment is currently not used (Jan 16 2020)
        # node = self.add_af_step(imp, node)
#        node = self.add_af_step(ohe, node)

        return node, tnode, rtnode

