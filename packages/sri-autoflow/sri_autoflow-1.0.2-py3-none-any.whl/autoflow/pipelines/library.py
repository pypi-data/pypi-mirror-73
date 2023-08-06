
class PipelineLibrary(object):
    """
    Class that provides access to a collection of primitive-like preamble pipelines.
    """

    def __init__(self, dataset, autoflowconfig, augmentation_hints=None):
        self.dataset = dataset
        self.config = autoflowconfig
        self.augmentation_hints = augmentation_hints
        self.library = set()
        self.cache = {}

    def available_pipeline_classes(self):
        """
        :return: A list of pipelines available.  These will all be subclasses of AutoflowPipelineFragment.
        """
        return list(self.library)

    def add_pipeline_class(self, cls):
        """
        Adds a class to the library.

        :param cls: A subclass of AutoflowPipelineFragment.
        :return: None.
        """
        if cls not in self.library:
            self.library.add(cls)

    def get_pipeline(self, cls, **hparms):
        """
        Provides access to a parameterized preamble pipeline, an instance of AutoflowPipelineFragment.
        Upon first retrieval of an instantiated pipeline, there may be some non-trivial processing.
        For example, data augmentation, if warranted, will be applied.

        :param cls: The class implementing the pipeline
        :param dataset: The dataset against which the pipeline will be run.
        :param hparms: Hyperparameters of the pipeline.

        """
        key = (cls, tuple(hparms.items()))
        if key in self.cache:
            return self.cache[key]





