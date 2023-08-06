from .base import AutoflowPipelineFragment, SUGGESTED_TARGET_TYPE, ATTRIBUTE_TYPE

from d3m.primitives.data_transformation.denormalize import Common as Denormalize
from d3m.primitives.data_transformation.dataset_to_dataframe import Common as DatasetToDataFrame
from d3m.primitives.data_transformation.extract_columns_by_semantic_types import Common as ExtractColumnsBySemanticTypes

import os
# When we are running outside of docker dont try to import problematic (difficult to install) primitives
if os.getenv('AUTOFLOW_WITH_NO_DOCKER') is None:
    from d3m.primitives.data_preprocessing.dataframe_to_tensor import DSBOX as DataFrameToTensor
    from d3m.primitives.feature_extraction.resnet50_image_feature import DSBOX as Resnet50ImageFeature
    from d3m.primitives.classification.xgboost_gbtree import Common as XGBoostGBTree

__all__ = ('ImageRecognitionFragment',)

class ImageRecognitionFragment(AutoflowPipelineFragment):

    name = "Image Recognition Preamble, SRI"
    description = "Common pipeline prefix for Image Recognition classification problems"
    label = "image_recognition_sri"

    def generate_dataset_steps(self):
        denormalize_0 = Denormalize(hyperparams={})
        node = self.add_af_step(denormalize_0, "inputs.0")
        return node

    def generate_dataframe_steps(self, node):
        dataset_to_dataframe_1 = DatasetToDataFrame(hyperparams=dict(dataframe_resource=None))

        extract_target_2 = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=[SUGGESTED_TARGET_TYPE]))

        hyperparams = DataFrameToTensor.metadata.get_hyperparams()
        data_frame_to_tensor_3 = DataFrameToTensor(hyperparams=hyperparams.defaults())

        hyperparams = Resnet50ImageFeature.metadata.get_hyperparams()
        resnet50_image_feature_4 = Resnet50ImageFeature(hyperparams=hyperparams.defaults().replace({
                'generate_metadata': True,
            }),)

        #TODO: If removing the XGBoost does not work for the other image issues lets try bring back LDA since that is
        # what works for CMU on the 124_188_usps problem
        #
        # extract_attributes_5 = ExtractColumnsBySemanticTypes(hyperparams=dict(semantic_types=(ATTRIBUTE_TYPE,)))

        # hyperparams = LinearDiscriminantAnalysis.metadata.get_hyperparams()
        # linearDiscriminantAnalysis_6 = LinearDiscriminantAnalysis(hyperparams=hyperparams.defaults())

        hyperparams = XGBoostGBTree.metadata.get_hyperparams()
        xg_boost_gb_tree_5 = XGBoostGBTree(hyperparams=hyperparams.defaults().replace({
                'n_jobs': -1,
                'return_result': 'new',
                'add_index_columns': True,
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 3,
                'gamma': 0.0,
                'min_child_weight': 1,
            }),)

        # Get a dataframe
        node = self.add_af_step(dataset_to_dataframe_1, node)
        original_node = node

        # Extract target
        tnode = self.add_af_step(extract_target_2, node)
        rtnode = tnode

        # Extract features
        node = self.add_af_step(data_frame_to_tensor_3, node)
        node = self.add_af_step(resnet50_image_feature_4, node)
        # node = self.add_af_step(extract_attributes_5, node)
        # node = self.add_af_step(linearDiscriminantAnalysis_6, node, outputs=tnode)
        node = self.add_af_step(xg_boost_gb_tree_5, node, outputs=original_node)

        return node, tnode, rtnode
