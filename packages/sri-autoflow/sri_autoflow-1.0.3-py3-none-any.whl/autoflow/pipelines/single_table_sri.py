from .base import AutoflowPipelineFragment, SCALAR_TYPES

from d3m.primitives.schema_discovery.profiler import Common as SimpleProfiler

from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes

from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.data_transformation.conditioner import Conditioner
from d3m.primitives.data_preprocessing.dataset_text_reader import DatasetTextReader

__all__ = ('SingleTableSRIFragment',)

class SingleTableSRIFragment(AutoflowPipelineFragment):

    name = "Single Table Preamble, SRI"
    description = "Common pipeline prefix for single-table problems, with SRI Conditioner"
    label = "single_table_sri"
    configuration = dict(max_tokenized_expansion=(7, 'maximum_expansion'))

    def generate_dataset_steps(self):
        tr = DatasetTextReader(hyperparams={})
        node = self.add_af_step(tr, "inputs.0")
        return node

    def generate_dataframe_steps(self, node):
        todf = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
        simple_profiler = SimpleProfiler(hyperparams={})
        scp = SimpleColumnParser(hyperparams={})
        cp = SimpleColumnParser(hyperparams=dict(parse_semantic_types=tuple(SCALAR_TYPES)))
        ext_attr = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/Attribute",)))
        cond = Conditioner(hyperparams=dict(ensure_numeric=True, maximum_expansion=30))
        ext_targ = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/TrueTarget",)))

        # Get a dataframe
        node = self.add_af_step(todf, node)

        # Add primitive to add the metadata back in
        node = self.add_af_step(simple_profiler, node)

        # Extract target
        tnode = self.add_af_step(ext_targ, node)
        rtnode = tnode
        tnode = self.add_af_step(scp, tnode)

        # Extract features
        node = self.add_af_step(cp, node)
        node = self.add_af_step(ext_attr, node)
        node = self.add_af_step(cond, node)
#        node = self.add_af_step(fs, node, outputs=tnode)
#        node = self.add_af_step(ohe, node)

        return node, tnode, rtnode

