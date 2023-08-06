from .base import AutoflowPipelineFragment, SUGGESTED_TARGET_TYPE, PRIMARY_KEY_TYPE, ATTRIBUTE_TYPE, TRUE_TARGET_TYPE, SCALAR_TYPES

from d3m.primitives.data_transformation.denormalize import Common as Denormalize
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes

import os
# When we are running outside of docker dont try to import problematic (difficult to install) primitives
if os.getenv('AUTOFLOW_WITH_NO_DOCKER') is None:
    from d3m.primitives.operator.dataset_map import DataFrameCommon as DatasetMap
    from d3m.primitives.data_transformation.to_numeric import DSBOX as ToNumeric
    from d3m.primitives.schema_discovery.profiler import DSBOX as Profiler
    from d3m.primitives.data_cleaning.cleaning_featurizer import DSBOX as CleaningFeaturizer
    from d3m.primitives.data_preprocessing.encoder import DSBOX as Encoder
    from d3m.primitives.data_preprocessing.mean_imputation import DSBOX as MeanImputation
    from d3m.primitives.normalization.iqr_scaler import DSBOX as IQRScaler

# TODO: Put this back in when the DFS is merged in (Jan 16 2020)
# from d3m.primitives.feature_construction.deep_feature_synthesis import SingleTableFeaturization as DeepFeatureSynthesis
# from d3m.primitives.data_cleaning.imputer import SKlearn as Imputer
from d3m.primitives.data_transformation.simple_column_parser import DataFrameCommon as SimpleColumnParser

__all__ = ('VideoClassificationFragment',)

class VideoClassificationFragment(AutoflowPipelineFragment):

    name = "Video Classification Preamble, SRI"
    description = "Common pipeline prefix for Video Classification problems"
    label = "video_classification_sri"

    def generate_dataset_steps(self):
        hyperparams = DatasetMap.metadata.get_hyperparams()
        dataset_map_0 = DatasetMap(hyperparams=hyperparams.defaults().replace({
                'primitive': SimpleColumnParser(
                    hyperparams=SimpleColumnParser.metadata.get_hyperparams().defaults(),
                ),
                'resources': 'all',
                'fit_primitive': 'no',
            }),)
        node = self.add_af_step(dataset_map_0, "inputs.0")
        return node

    def generate_dataframe_steps(self, node):
        denormalize_1 = Denormalize(hyperparams=dict(starting_resource='learningData'))

        dataset_to_data_frame_2 = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))

        extract_target_3 = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(SUGGESTED_TARGET_TYPE,)))

        simple_column_parser_4 = SimpleColumnParser(hyperparams={})

        column_parser_5 = SimpleColumnParser(hyperparams=dict(parse_semantic_types=tuple(SCALAR_TYPES)))

        extract_attributes_6 = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(ATTRIBUTE_TYPE,)))

        # TODO: Put this back in when the DFS is merged in (Jan 16 2020)
        # deep_feature_synthesis_7 = DeepFeatureSynthesis(hyperparams={})

        # TODO: Experiment with adding some of these primitives back in - They create bad pipelines (cannot convert "brushing hair" to float)
        # hyperparams = Imputer.metadata.get_hyperparams()
        # imputer = Imputer(hyperparams=hyperparams.defaults().replace({
        #         'return_result': 'replace',
        #         'use_semantic_types': True,
        #     }),)
        # hyperparams = RobustScaler.metadata.get_hyperparams()
        # robust_scaler = RobustScaler(hyperparams=hyperparams.defaults().replace({
        #         'return_result': 'replace',
        #         'use_semantic_types': True,
        #     }),)
        # hyperparams = LightGBM.metadata.get_hyperparams()
        # light_gbm = LightGBM(hyperparams=hyperparams.defaults().replace({
        #         'return_result': 'replace',
        #         'use_outputs_columns': [0],
        #     }),)

        # get dataframe
        node = self.add_af_step(denormalize_1, node)
        node = self.add_af_step(dataset_to_data_frame_2, node)

        # get target
        tnode = self.add_af_step(extract_target_3, node)
        rtnode = tnode
        tnode = self.add_af_step(simple_column_parser_4, tnode)

        # get attributes
        node = self.add_af_step(column_parser_5, node)
        node = self.add_af_step(extract_attributes_6, node)

        # TODO: Put this back in when the DFS is merged in (Jan 16 2020)
        # node = self.add_af_step(deep_feature_synthesis_7, node)
        # node = self.add_af_step(imputer, node)
        # node = self.add_af_step(robust_scaler, node)
        # node = self.add_af_step(light_gbm, node, outputs=tnode)

        return node, tnode, rtnode

# DSBox Video pipeline - would not convert file names to values and it was absent metadata. Also - one of their primitives (corextext) is not in the base image?
#     def generate_dataframe_steps(self, node):
#         dataset_to_data_frame = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))
#
#         extract_target = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/SuggestedTarget",)))
#         to_numeric = ToNumeric(hyperparams=dict(drop_non_numeric_columns=False))
#
#         column_parser = SimpleColumnParser(hyperparams=dict(parse_semantic_types=tuple(SCALAR_TYPES)))
#         extract_attributes = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=("https://metadata.datadrivendiscovery.org/types/Attribute",)))
#
#         profiler = Profiler(hyperparams={})
#         cleaning_featurizer = CleaningFeaturizer(hyperparams={})
#         # corex_text = CorexText(hyperparams=dict(n_hidden=10, threshold=0, n_grams=5, max_df=0.9, min_df=0.02))
#         encoder = Encoder(hyperparams={})
#         mean_imputation = MeanImputation(hyperparams={})
#         iqr_scaler = IQRScaler(hyperparams=dict(with_centering=True, with_scaling=True, quantile_range_lowerbound=25.0,
#                                                 quantile_range_upperbound=75.0))
#
#         # get dataframe
#         node = self.add_af_step(dataset_to_data_frame, node)
#
#         # get target
#         tnode = self.add_af_step(extract_target, node)
#         rtnode = tnode
#
#         # get attributes
#         node = self.add_af_step(column_parser, node)
#         node = self.add_af_step(extract_attributes, node)
#
#         # apply
#         node = self.add_af_step(to_numeric, node)
#         node = self.add_af_step(profiler, node)
#         node = self.add_af_step(cleaning_featurizer, node)
#         # node = self.add_af_step(corex_text, node)
#         node = self.add_af_step(encoder, node)
#         node = self.add_af_step(mean_imputation, node)
#         node = self.add_af_step(iqr_scaler, node)
#
#
#         return node, tnode, rtnode