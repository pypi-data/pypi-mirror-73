from .base import AutoflowPipelineFragment, SCALAR_TYPES

import os
# When we are running outside of docker dont try to import problematic (difficult to install) primitives
if os.getenv('AUTOFLOW_WITH_NO_DOCKER') is None:
    from d3m.primitives.data_transformation.load_graphs import JHU as LoadGraphs
    from d3m.primitives.data_preprocessing.largest_connected_component import JHU as LargestConnectedComponent
    from d3m.primitives.data_transformation.laplacian_spectral_embedding import JHU as LaplacianSpectralEmbedding
    from d3m.primitives.graph_clustering.gaussian_clustering import JHU as GaussianClustering

__all__ = ('CommunityDetectionJHUFragment',)

class CommunityDetectionJHUFragment(AutoflowPipelineFragment):

    name = "Community Detection JHU Preable Pipeline Fragment"
    description = "Adapted from JHU's sample Vertex Classification pipelines"
    label = "community_detection_jhu"

    def generate_dataset_steps(self):
        hyperparams = LoadGraphs.metadata.get_hyperparams()
        load_graphs = LoadGraphs(hyperparams=hyperparams.defaults())
        node = self.add_af_step(load_graphs, "inputs.0")
        return node

    def generate_dataframe_steps(self, node):
        hyperparams = LargestConnectedComponent.metadata.get_hyperparams()
        largest_connected_component = LargestConnectedComponent(hyperparams=hyperparams.defaults())

        hyperparams = LaplacianSpectralEmbedding.metadata.get_hyperparams()
        laplacian_spectral_embedding = LaplacianSpectralEmbedding(hyperparams=hyperparams.defaults().replace({
            'max_dimension': 5,
            'use_attributes': True,
        }),)

        hyperparams = GaussianClustering.metadata.get_hyperparams()
        gaussian_clustering = GaussianClustering(hyperparams=hyperparams.defaults().replace({
            'max_clusters': 10,
        }),)

        node = self.add_af_step(largest_connected_component, node)
        node = self.add_af_step(laplacian_spectral_embedding, node)
        node = self.add_af_step(gaussian_clustering, node)

        return node, node, node

