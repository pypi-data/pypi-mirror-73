from .base import AutoflowPipelineFragment, SCALAR_TYPES

# from d3m.primitives.graph_matching.seeded_graph_matching import JHU as SeededGraphMatching

__all__ = ('GraphMatchingJHUFragment',)

class GraphMatchingJHUFragment(AutoflowPipelineFragment):

    name = "Graph Matching JHU Preable Pipeline Fragment"
    description = "Adapted from JHU's sample Vertex Classification pipelines"
    label = "graph_matching_jhu"

    def generate_dataset_steps(self):
        # hyperparams = SeededGraphMatching.metadata.get_hyperparams()
        # seeded_graph_matching = SeededGraphMatching(hyperparams=hyperparams.defaults())
        # node = self.add_af_step(seeded_graph_matching, "inputs.0")
        # return node
        return None

    def generate_dataframe_steps(self, node):

        return node, node, node

