from .base import AutoflowPipelineFragment, SCALAR_TYPES

import os
# When we are running outside of docker dont try to import problematic (difficult to install) primitives
if os.getenv('AUTOFLOW_WITH_NO_DOCKER') is None:
    from d3m.primitives.link_prediction.data_conversion import JHU as DataConversion
    from d3m.primitives.data_transformation.adjacency_spectral_embedding import JHU as AdjacencySpectralEmbedding
    from d3m.primitives.link_prediction.rank_classification import JHU as RankClassification

__all__ = ('LinkPredictionJHUFragment',)

class LinkPredictionJHUFragment(AutoflowPipelineFragment):

    name = "Link Prediction JHU Preable Pipeline Fragment"
    description = "Adapted from JHU's sample LinkPrediction pipelines"
    label = "link_prediction_jhu"

    def generate_dataset_steps(self):
        hyperparams = DataConversion.metadata.get_hyperparams()
        data_conversion = DataConversion(hyperparams=hyperparams.defaults())
        node = self.add_af_step(data_conversion, "inputs.0")
        return node

    def generate_dataframe_steps(self, node):
        hyperparams = AdjacencySpectralEmbedding.metadata.get_hyperparams()
        adjacency_spectral_embedding = AdjacencySpectralEmbedding(hyperparams=hyperparams.defaults().replace({
            'which_elbow': 1,
            'max_dimension': 2,
            'use_attributes': False,
        }),)

        hyperparams = RankClassification.metadata.get_hyperparams()
        rank_classification = RankClassification(hyperparams=hyperparams.defaults())

        node = self.add_af_step(adjacency_spectral_embedding, node)
        node = self.add_af_step(rank_classification, node)

        return node, node, node

