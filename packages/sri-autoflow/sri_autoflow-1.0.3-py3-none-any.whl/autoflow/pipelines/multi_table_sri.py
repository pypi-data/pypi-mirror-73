from .base import AutoflowPipelineFragment, ENTRY_POINT_TYPE, ATTRIBUTE_TYPE, TRUE_TARGET_TYPE, KEY_TYPES

from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.schema_discovery.profiler import Common as SimpleProfiler

from d3m.primitives.data_transformation.conditioner import Conditioner
from d3m.primitives.data_preprocessing.dataset_text_reader import DatasetTextReader
from d3m.primitives.data_transformation.denormalize import Common as Denormalize

__all__ = ('MultiTableSRIFragment',)

class MultiTableSRIFragment(AutoflowPipelineFragment):

    name = "Multi Table Preamble, SRI"
    description = "Common pipeline prefix for multi-table problems, with SRI Conditioner"
    label = "multi_table_sri"
    configuration = dict(resource_id=(2, 'dataframe_resource'),
                         max_tokenized_expansion=(8, 'maximum_expansion')
    )

    def study_dataset(self, dataset):
        resource_id = None
        for rid in dataset.keys():
            stypes = dataset.metadata.query((rid,)).get('semantic_types', [])
            if ENTRY_POINT_TYPE in stypes:
                resource_id = rid
                break
        if resource_id is None:
            raise ValueError("Cannot find entry resource")
        self.configure(resource_id=resource_id)

    def generate_dataset_steps(self):
        tr = DatasetTextReader(hyperparams={})
        dn = Denormalize(hyperparams={})
        node = "inputs.0"
        node = self.add_af_step(tr, node)
        node = self.add_af_step(dn, node)
        return node

    def generate_dataframe_steps(self, node):
        todf = DatasetToDataFrame(hyperparams={})
        simple_profiler = SimpleProfiler(hyperparams={})
        scp = SimpleColumnParser(hyperparams={})
        cp = SimpleColumnParser(hyperparams={})
        ext_attr = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(ATTRIBUTE_TYPE,)))
        # rm_keys = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=tuple(KEY_TYPES), negate=True))
        cond = Conditioner(hyperparams=dict(ensure_numeric=True, maximum_expansion=30))
        ext_targ = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(TRUE_TARGET_TYPE,)))

        node = self.add_af_step(todf, node)

        # Add primitive to add the metadata back in
        node = self.add_af_step(simple_profiler, node)

        # Extract the target
        tnode = self.add_af_step(ext_targ, node)
        rtnode = tnode
        tnode = self.add_af_step(scp, tnode)

        # Extract features
        node = self.add_af_step(cp, node)
        #TODO: Check with Dayne about this - removing the keys was killing search - could be the new meta data changes
        # has made this step unnecessary?
        # node = self.add_af_step(rm_keys, node)
        node = self.add_af_step(ext_attr, node)
        node = self.add_af_step(cond, node)

        return node, tnode, rtnode

