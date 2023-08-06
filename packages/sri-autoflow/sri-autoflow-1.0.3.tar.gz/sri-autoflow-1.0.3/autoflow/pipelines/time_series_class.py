from .base import AutoflowPipelineFragment, SUGGESTED_TARGET_TYPE, TRUE_TARGET_TYPE

from d3m.primitives.schema_discovery.profiler import Common as SimpleProfiler
from d3m.primitives.data_transformation.denormalize import Common as Denormalize
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes

import os
# When we are running outside of docker dont try to import problematic (difficult to install) primitives
if os.getenv('AUTOFLOW_WITH_NO_DOCKER') is None:
    from d3m.primitives.data_preprocessing.time_series_to_list import DSBOX as TimeSeriesToList
    from d3m.primitives.feature_extraction.random_projection_timeseries_featurization import DSBOX as TimeSeriesRandomProjection

__all__ = ('TimeSeriesClassificationFragment',)

class TimeSeriesClassificationFragment(AutoflowPipelineFragment):

    name = "Time Series Classification Preamble, SRI"
    description = "Common pipeline prefix for Time Series classification problems"
    label = "time_series_class_sri"

    def generate_dataset_steps(self):
        dn = Denormalize(hyperparams={})
        node = self.add_af_step(dn, "inputs.0")
        return node

    def generate_dataframe_steps(self, node):
        todf = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
        sp = SimpleProfiler(hyperparams={})
        ext_targ = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=[SUGGESTED_TARGET_TYPE,
                                                                                  TRUE_TARGET_TYPE]))
        scp = SimpleColumnParser(hyperparams={})
        tstl = TimeSeriesToList(hyperparams={})
        tsrp = TimeSeriesRandomProjection(hyperparams={})

        node = self.add_af_step(todf, node)
        node = self.add_af_step(sp, node)
        tnode = self.add_af_step(ext_targ, node)
        rtnode = tnode
        tnode = self.add_af_step(scp, tnode)
        node = self.add_af_step(tstl, node)
        node = self.add_af_step(tsrp, node)

        return node, tnode, rtnode
