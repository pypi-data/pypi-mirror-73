from .base import AutoflowPipelineFragment
from .base import TRUE_TARGET_TYPE, SCALAR_TYPES, ATTRIBUTE_TYPE, PRIMARY_KEY_TYPE, GROUPING_KEY_TYPE, CATEGORICAL_TYPE

from d3m.primitives.schema_discovery.profiler import Common as SimpleProfiler
from d3m.primitives.data_transformation.denormalize import Common as Denormalize
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes
from d3m.primitives.data_transformation.grouping_field_compose import Common as GroupingFieldCompose
# TODO: Put this back in when the VAR is merged in (Jan 16 2020)
# from d3m.primitives.time_series_forecasting.vector_autoregression import VAR as VectorAutoRegression

__all__ = ('TimeSeriesForecastingFragment',)

class TimeSeriesForecastingFragment(AutoflowPipelineFragment):

    name = "Time Series Forecasting Preamble, SRI"
    description = "Common pipeline prefix for Time Series forecasting problems"
    label = "time_series_forecast_sri"

    def generate_dataset_steps(self):
        denormalize = Denormalize(hyperparams={})
        node = self.add_af_step(denormalize, "inputs.0")
        return node

    def generate_dataframe_steps(self, node):
        todf = DatasetToDataFrame(hyperparams=dict(dataframe_resource='learningData'))
        sp = SimpleProfiler(hyperparams={})

        target_ext_targ = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=[TRUE_TARGET_TYPE]))
        # target_step_2_scp = SimpleColumnParser(hyperparams={})
        target_scp = SimpleColumnParser(hyperparams={})

        # The default grouping_field_type is Text so we need to set it to Categorical to address issue #44
        # (https://gitlab.com/daraghhartnett/tpot-ta2/-/issues/44)
        gfc = GroupingFieldCompose(hyperparams=dict(grouping_field_type=CATEGORICAL_TYPE))
        extr_attr = ExtractColumnsBySemanticTypes(
            hyperparams=dict(semantic_types=[ATTRIBUTE_TYPE, PRIMARY_KEY_TYPE, GROUPING_KEY_TYPE])
        )
        cp = SimpleColumnParser(hyperparams=dict(parse_semantic_types=tuple(SCALAR_TYPES)))

#        defaults = VectorAutoRegression.metadata.get_hyperparams().defaults()
#        step_4_var = VectorAutoRegression(hyperparams=defaults)
#        step_2_var = VectorAutoRegression(hyperparams=defaults.replace({
#            'n_periods': 21,
#            'seasonal_differencing': 11,
#        }),)

        node = self.add_af_step(todf, node)
        node = self.add_af_step(sp, node)

        tnode = self.add_af_step(target_ext_targ, node)
        rtnode = tnode
        tnode = self.add_af_step(target_scp, tnode)

        node = self.add_af_step(gfc, node)
        node = self.add_af_step(extr_attr, node)
        node = self.add_af_step(cp, node)
#        node = self.add_af_step(step_4_var, node, outputs=node)

        return node, tnode, rtnode
