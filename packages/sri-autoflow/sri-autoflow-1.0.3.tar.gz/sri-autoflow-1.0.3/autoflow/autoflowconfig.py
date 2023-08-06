import os
import json
from autoflow.optimizer import TPOTClassificationOptimizer
from autoflow.optimizer import TPOTRegressionOptimizer
from autoflow.optimizer import GamaClassificationOptimizer
from autoflow.optimizer import GamaRegressionOptimizer
from autoflow.optimizer import VertexClassificationJHUOptimizer
from autoflow.optimizer import CommunityDetectionJHUOptimizer
from autoflow.optimizer import GraphMatchingJHUOptimizer
from autoflow.optimizer import LinkPredictionJHUOptimizer
from autoflow.optimizer import ObjectDetectionOptimizer
from autoflow.optimizer import GamaTimeSeriesForecastingOptimizer
from autoflow.optimizer import GamaTimeSeriesClassificationOptimizer
import logging
import stat

from gama.postprocessing import BestFitPostProcessing, EnsemblePostProcessing

# init logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')
_logger = logging.getLogger(__name__)

DATAMARTS = {
    'NYU': 'https://datamart.d3m.vida-nyu.org',
    'ISI': "http://dsbox02.isi.edu:9001/blazegraph/namespace/datamart4/sparql"
}

class AutoflowConfig(object):

    # Mapping from D3M problem types to optimizer classes
    optimizer_class_map = dict(
        classification         = dict(TPOT=TPOTClassificationOptimizer, GAMA=GamaClassificationOptimizer),
        regression             = dict(TPOT=TPOTRegressionOptimizer, GAMA=GamaRegressionOptimizer),
        # clustering           = TODO
        vertexNomination       = dict(TPOT=TPOTClassificationOptimizer, GAMA=GamaClassificationOptimizer),

        #TODO: We currently have a Vertex Classification Optimizer (PSL) but for now lets try the JHU pipeline to see
        # what it can do - choose the better scoring fragment
        # vertexClassification  = VertexClassificationOptimizer,
        vertexClassification   = VertexClassificationJHUOptimizer,

        # This is not a typo - the JHU pipelines claim to use the same pipeline for both graph clustering and community detection problems
        graphClustering        = CommunityDetectionJHUOptimizer,
        graphMatching          = GraphMatchingJHUOptimizer,
        linkPrediction         = LinkPredictionJHUOptimizer,

        # Time Series Forecasting and Time Series Classification have dedicated preamble pipeline fragments
        collaborativeFiltering = dict(TPOT=TPOTClassificationOptimizer, GAMA=GamaClassificationOptimizer),
        objectDetection        = ObjectDetectionOptimizer,
        communityDetection     = CommunityDetectionJHUOptimizer,

        semiSupervisedClassification=dict(TPOT=TPOTClassificationOptimizer, GAMA=GamaClassificationOptimizer),

        timeSeriesForecasting  = dict(GAMA=GamaTimeSeriesForecastingOptimizer),
        timeSeriesClassification = dict(GAMA=GamaTimeSeriesClassificationOptimizer)
    )

    metric_map = dict(
        accuracy="accuracy",
        f1="f1_true",
        f1_true="f1_true",
        f1Micro="f1_micro",
        f1Macro="f1_macro",
        rocAuc="roc_auc",
        rocAucMicro="recall_micro",
        rocAucMacro="recall_macro",
        meanSquaredError="mean_squared_error",
        rootMeanSquaredError="root_mean_squared_error",
        rootMeanSquaredErrorAvg="root_mean_squared_error_average",
        meanAbsoluteError="mean_absolute_error",
        rSquared="r2",
        normalizedMutualInformation="normalized_mutual_info_score",
        jaccardSimilarityScore="jaccard_similarity_score",
        precisionAtTopK=None
    )


    metric_optimizer = dict(
        accuracy = dict(TPOT=TPOTClassificationOptimizer, GAMA=GamaClassificationOptimizer),
        f1 = dict(TPOT=TPOTClassificationOptimizer, GAMA=GamaClassificationOptimizer),
        f1_micro = dict(TPOT=TPOTClassificationOptimizer, GAMA=GamaClassificationOptimizer),
        f1_macro = dict(TPOT=TPOTClassificationOptimizer, GAMA=GamaClassificationOptimizer),
        mean_squared_error = dict(TPOT=TPOTRegressionOptimizer, GAMA=GamaRegressionOptimizer),
        root_mean_squared_error= dict(TPOT=TPOTRegressionOptimizer, GAMA=GamaRegressionOptimizer),
        root_mean_squared_error_average=dict(TPOT=TPOTRegressionOptimizer, GAMA=GamaRegressionOptimizer),
        mean_absolute_error=dict(TPOT=TPOTRegressionOptimizer, GAMA=GamaRegressionOptimizer)
    )

    """
    Here's the env variables currently being proposed for the Phase 2 eval
    (https://datadrivendiscovery.org/wiki/display/work/Evaluation+Workflow)
    D3MRUN - a label what is the setting under which the pod is being run
    D3MINPUTDIR - a location of dataset(s), read - only
    D3MPROBLEM - a location to problem description to use(should be under D3MINPUTDIR), datasets are linked from the problem description using IDs, those datasets should exist inside D3MINPUTDIR
    D3MOUTPUTDIR - a location of output files, shared by TA2 and TA3 pods( and probably data mart)
    D3MLOCALDIR - a local - to - host directory provided; used by memory sharing mechanisms
    D3MSTATICDIR - a path to the volume with primitives' static files
    D3MCPU - available CPU units in Kubernetes specification
    D3MRAM - available memory units in Kubernetes specification
    D3MTIMEOUT
    """

    def __init__(self, problem=None, config_file=None, config_dict=None, target=None):

        # Suppress a bunch of log output clutter
        for namespace in ("d3m.namespace", "d3m.index", "git.cmd", "matplotlib.font_manager", "matplotlib",
                          "rdflib", "gensim.models.doc2vec", "summa.preprocessing.cleaner", "root",
                          "faker.factory", "gensim.models.fasttext"):
            log = logging.getLogger(namespace)
            log.setLevel(logging.CRITICAL)
            log.propagate = True

        if problem.endswith(".csv") and target is not None:
            # When running autoflow on just a .csv with a supplied target
            self.process_csv_and_target(problem, config_file, target)
        elif config_file is not None and "http" not in problem:
            # When called in TA2 standalone mode with D3M seed datasets
            self.process_config_file(problem, config_file)
        elif config_dict is not None:
            # When called in TA2 TA3 Mode and the config information is passed over the api
            self.process_config_dict(config_dict)
        else:
            # This means we are being called with an OpenML Dataset and no additional config will be provided
            self.process_open_ML(problem, config_file)

        logging.info("output_dir recorded as: %s" % self.output_dir)

        # Make sure dirs are there (for local testing)
        self._make_dirs('pipelines_ranked', 'pipelines_scored',
                        'pipelines_searched', 'subpipelines',
                        'pipeline_runs', 'additional_inputs', 'temp')

        self.process_environment_variables()


    '''
    When running in TA3 mode the system wants us to move output directories under a directory names after
    the search_id.
    '''
    def update_paths(self, search_id):
        logging.info("Updating paths under search_id: %s" % search_id)
        logging.info("Base Path is: %s" % self.output_dir)

        search_id_dir = "%s/%s" % (self.output_dir, str(search_id))
        if not os.path.exists(search_id_dir):
            os.makedirs(search_id_dir)
            os.chmod(search_id_dir, stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH |
                               stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                               stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP)
        else:
            logging.warning("WARNING! A Search folder with the ID %s already exists! This should never happen!" % search_id)
        temp_dir = "%s/%s" % (self.output_dir, 'temp')

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            os.chmod(temp_dir, stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH |
                               stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                               stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP)
        setattr(self, 'temp', temp_dir)

        for output_field in ('pipelines_ranked', 'pipelines_scored',
                        'pipelines_searched', 'subpipelines',
                        'pipeline_runs', 'additional_inputs'):
            # Remove original dirs
            if os.path.exists("%s/%s" % (self.output_dir, output_field)):
                try:
                    os.rmdir("%s/%s" % (self.output_dir, output_field))
                except Exception as e:
                    logging.warning("Unable to remove directory: %s/%s" % (self.output_dir, output_field))
            logging.info("Creating updated path: %s/%s/%s" % (self.output_dir, str(search_id), output_field))
            output_field_path = "%s/%s/%s" % (self.output_dir, str(search_id), output_field)
            os.makedirs(output_field_path)
            os.chmod(output_field_path, stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH |
                               stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                               stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP)
            setattr(self, output_field, output_field_path)


    def infer_problem_config(self):
        self.training_data_root = "%s/%s/TRAIN/dataset_TRAIN" % (self.input_root, self.problem)
        self.problem_root = "%s/%s/TRAIN/problem_TRAIN" % (self.input_root, self.problem)
        self.dataset_schema = "%s/datasetDoc.json" % self.training_data_root
        self.problem_schema = "%s/problemDoc.json" % self.problem_root

        for output_field in ('pipelines_ranked', 'pipelines_scored', 'pipelines_searched', 'subpipelines',
                             'pipeline_runs', 'additional_inputs', 'temp'):
            setattr(self, output_field, "%s/%s/%s" % (self.output_root, self.problem, output_field))
        self.output_dir = "%s/%s" % (self.output_root, self.problem)


    def process_config_file(self, problem, config_file):
        # e.g., '185_baseball'
        self.problem = problem
        self.process_config_data(config_file)
        self.infer_problem_config()

        # Read the problem doc (problemSchema)
        problemDoc = self.problemDoc = json.load(open(self.problem_schema))
        self.problem_id = problemDoc["about"]["problemID"]
        # Get the target column name from the problem doc as it is not longer provided in the metadata
        self.target_column_name = problemDoc['inputs']['data'][0]['targets'][0]['colName']
        try:
            self.metric = self.metric_map[problemDoc["inputs"]["performanceMetrics"][0]["metric"]]
        except KeyError:
            self.metric = None
        try:
            self.pos_label = problemDoc["inputs"]["performanceMetrics"][0]["posLabel"]
        except KeyError:
            self.pos_label = None

        # TODO: Bring in clauses to handle forecasting types from parse_datasets in the sri_d3m project
        taskKeyword_taskType_set = {
            "classification",
            "regression",
            "linkPrediction",
            "vertexNomination",
            "vertexClassification",
            "graphClustering",
            "graphMatching",
            "collaborativeFiltering",
            "objectDetection",
            "communityDetection",
            "semiSupervised",
            # Compound problem types such as timeSeries/Classification/Forecasting get special handling below
        }

        taskKeywords = problemDoc["about"]["taskKeywords"]
        taskType = taskKeyword_taskType_set.intersection(taskKeywords)
        if 'timeSeries' in taskKeywords and 'forecasting' in taskKeywords:
            self.taskType = 'timeSeriesForecasting'
        elif 'timeSeries' in taskKeywords and 'classification' in taskKeywords:
            self.taskType = 'timeSeriesClassification'
        elif 'semiSupervised' in taskKeywords and 'classification' in taskKeywords:
            self.taskType = 'semiSupervisedClassification'
        elif len(taskType) == 1:
            self.taskType = taskType.pop()
        elif len(taskType) == 0:
            _logger.warning("Supported Task Type is not found in taskKeywords: %s from problemDoc" % taskKeywords)
            self.taskType = None
        elif len(taskType) > 1:
            _logger.warning("More than one Supported Task Type Task Type found in taskKeywords: %s from problemDoc."
                            " Continuing with the first one detected" % taskKeywords)
            self.taskType = taskType.pop()

        _logger.info("Task Type selected is: %s" % self.taskType)

        self.outputFileName = problemDoc["expectedOutputs"]["predictionsFile"]

        # Read the dataset description
        self.dataDoc = json.load(open(self.dataset_schema))
        self.privileged_columns = self._get_privileged_columns()
        self.base_directory = os.getcwd()

        # See if there is data augmentation info in the problem description
        try:
            self.data_augmentation = problemDoc['dataAugmentation']
        except KeyError:
            self.data_augmentation = None

    def process_config_data(self, config_file):
        configData = self.configData = json.load(open(config_file))
        # Note - metric is only expected to be present when running with openml or .csv data
        self._get_attrs(configData, 'input_root', 'output_root',
                        'timeout', 'cpus', 'ram', 'optimizer_args', 'fit_args',
                        'preamble_args', 'maximum_rows', 'max_generation_time_mins',
                        'cr_backend', 'grammar_file_name', 'grammar_rule_name', 'pipeline_caching',
                        'datamart_provider', 'ensemble_n', 'metric', 'task_type'
                        )

    def process_config_dict(self, config_dict):
        # Populate the values that we got from TA3 when they started the session
        self.problem_id = config_dict.get("problemId")
        self.metric = config_dict.get("metric")
        self.taskType = config_dict.get("taskType")
        self.dataset_schema = config_dict.get("datasetSchema")
        self.timeout = config_dict.get("timeout")
        # Use 2/3rds of the time budget for search so we have enough time for fitting
        # self.timeout *= 0.66
        logging.info("Search time: %s minutes" % self.timeout)
        self.cpus = config_dict.get("cpus")
        self.cr_backend = config_dict.get("cr_backend")

        try:
            self.pos_label = config_dict.get("pos_label")
        except KeyError:
            self.pos_label = None

        # TODO: Do not add this to the deployed code! This is for super fast testing
        #self.optimizer_args = dict(population_size = 10)

        # Read the k8s output env variable if it is there
        self.output_dir = "/output/%s" % self.problem_id
        if 'D3MOUTPUTDIR' in os.environ:
            self.output_dir = os.environ['D3MOUTPUTDIR']
            logging.info("Overriding output_dir from env variable: %s" % self.output_dir)

        # Get the target column name from the problem doc data as it is not longer provided in the metadata
        self.target_column_name = config_dict.get("targetName")

        # These directories are specified in the evaluation workflow schema:
        self.pipelines_ranked = '%s/pipelines_ranked' % self.output_dir
        self.pipelines_scored = '%s/pipelines_scored' % self.output_dir
        self.pipelines_searched = '%s/pipelines_searched' % self.output_dir
        self.subpipelines = '%s/subpipelines' % self.output_dir
        self.pipeline_runs = '%s/pipeline_runs' % self.output_dir
        self.additional_inputs = '%s/additional_inputs' % self.output_dir
        self.temp = '%s/temp' % self.output_dir
        self.predictions_dir = '%s/predictions' % self.output_dir

        # Read the dataset description
        self.dataDoc = json.load(open(config_dict.get("datasetSchema")))
        self.privileged_columns = self._get_privileged_columns()
        self.base_directory = os.getcwd()

        # NOTE: This was commented out as the latest version of gama (d3m branch) does not recognize this parameter
        # Set the fit args for GAMA for the TA2TA3 mode since we no longer have a config file
        # values = {'auto_ensemble_n': 1}
        # setattr(self, 'fit_args', values)

        # Get data augmentation info into the format expected by our TA2
        try:
            problem = config_dict.get("problem")
            augmentation_struct = list(problem.data_augmentation)

            if len(augmentation_struct) == 0:
                logging.info("No Data Augmentation data provided by TA3")
                self.data_augmentation = None
            else:
                logging.info("Data Augmentation data provided by TA3 for processing")
                augmentation_list = []
                augmentation_categories = dict()
                augmentation_list.append(augmentation_categories)
                domain = []
                for domain_entry in augmentation_struct[0].domain:
                    domain.append(domain_entry)
                augmentation_categories['domain'] = domain

                keywords = []
                for keyword_entry in augmentation_struct[0].keywords:
                    keywords.append(keyword_entry)
                augmentation_categories['keywords'] = keywords

                self.data_augmentation = augmentation_list
        except KeyError:
            logging.info("No Data Augmentation data provided by TA3")
            self.data_augmentation = None



    def process_csv_and_target(self, csv_file, config_file, target):
        logging.info("CSV File detected: %s" % csv_file)

        # Load and process the config variables in the config file (timeout cpu ram etc)
        self.process_config_data(config_file)

        # The problem is the path to the CSV File
        self.dataset_schema = csv_file

        # Extract the problem id
        parts = csv_file.split('/')
        csv_file = parts[len(parts) - 1]
        self.problem_id = csv_file.replace(".csv", "")
        self.output_dir = "%s/%s" % (self.output_root, self.problem_id)

        # These directories are specified in the evaluation workflow schema:
        self.pipelines_ranked = '%s/pipelines_ranked' % self.output_dir
        self.pipelines_scored = '%s/pipelines_scored' % self.output_dir
        self.pipelines_searched = '%s/pipelines_searched' % self.output_dir
        self.subpipelines = '%s/subpipelines' % self.output_dir
        self.pipeline_runs = '%s/pipeline_runs' % self.output_dir
        self.additional_inputs = '%s/additional_inputs' % self.output_dir
        self.predictions_dir = '%s/predictions' % self.output_dir
        self.temp = '%s/temp' % self.output_dir

        # What is this for? Something we should try populate from Open ML dataset?
        self.pos_label = None

        self.target_column_name = target


    def process_open_ML(self, problem, config_file):
        logging.info("Open ML dataset detected: %s" % problem)

        # Load and process the config variables in the config file (timeout cpu ram etc)
        self.process_config_data(config_file)

        # The problem is the path to the OpenML Dataset URL
        self.dataset_schema = problem

        # Extract the problem id
        parts = problem.split('/')
        self.problem_id = parts[len(parts) - 1]
        self.output_dir = "%s/%s" % (self.output_root, self.problem_id)

        # These directories are specified in the evaluation workflow schema:
        self.pipelines_ranked = '%s/pipelines_ranked' % self.output_dir
        self.pipelines_scored = '%s/pipelines_scored' % self.output_dir
        self.pipelines_searched = '%s/pipelines_searched' % self.output_dir
        self.subpipelines = '%s/subpipelines' % self.output_dir
        self.pipeline_runs = '%s/pipeline_runs' % self.output_dir
        self.additional_inputs = '%s/additional_inputs' % self.output_dir
        self.predictions_dir = '%s/predictions' % self.output_dir
        self.temp = '%s/temp' % self.output_dir

        # What is this for? Something we should try populate from Open ML dataset?
        self.pos_label = None


    def process_environment_variables(self):
        if 'D3MCPU' in os.environ:
            self.cpus = int(os.environ['D3MCPU'])
            logging.info("Overriding cpu from env variable: %s" % self.cpus)
        if 'D3MRAM' in os.environ:
            self.ram = os.environ['D3MRAM']
            logging.info("Overriding ram from env variable: %s" % self.ram)
        if 'D3MTIMEOUT' in os.environ:
            timeout_seconds = int(os.environ['D3MTIMEOUT'])
            self.timeout = timeout_seconds / 60
            _logger.info("Overriding timeout from env variable: %s (in seconds), converted to minutes: %s " %
                         (timeout_seconds, self.timeout))
        # Default to True
        self.use_whitelist = True
        if 'USEWHITELIST' in os.environ:
            _logger.info("Found 'use whitelist' setting: %s" % os.environ['USEWHITELIST'])
            if os.environ['USEWHITELIST'] == "False":
                self.use_whitelist = False

        # If set, the optimizer will load and prepare the test data. This is used to score the best pipline in GAMA
        # before it converts the pipelines to the D3M format. This is used as a sanity check.
        self.use_test_dataset = False
        if 'USETESTDATASET' in os.environ:
            _logger.info("Using the Test Dataset to expose internal Gama performance")
            self.use_test_dataset = True

        self.datamarts = dict(**DATAMARTS)

        if 'DATAMART_URL_ISI' in os.environ:
            self.datamarts['ISI'] = os.environ['DATAMART_URL_ISI']
            logging.info("Setting DATAMART_URL_ISI to %s", os.environ['DATAMART_URL_ISI'])
        if 'DATAMART_URL_NYU' in os.environ:
            self.datamarts['NYU'] = os.environ['DATAMART_URL_NYU']
            logging.info("Setting DATAMART_URL_NYU to %s", os.environ['DATAMART_URL_NYU'])

        # Use 2/3rds of the time budget for search so we have enough time for fitting
        # original = self.timeout
        # self.timeout *= 0.66
        # logging.info("Overriding search time from %s to %s minutes" %(original, self.timeout))

        self.static_volumes = None
        if 'D3MSTATICDIR' in os.environ:
            self.static_volumes = os.environ['D3MSTATICDIR']
            logging.info("Setting static_volumes to %s", os.environ['D3MSTATICDIR'])


    def _get_attrs(self, table, *attrs):
        for attr in attrs:
            if attr in table:
                setattr(self, attr, table[attr])


    def _make_dirs(self, *attrs):
        for attr in attrs:
            if hasattr(self, attr) and not os.path.exists(getattr(self, attr)):
                os.makedirs(getattr(self, attr), exist_ok=True)


    def _get_privileged_columns(self):

        priv = {}

        try:
            for qual in self.dataDoc['qualities']:
                if qual['qualName'] != 'privilegedFeature':
                    continue
                if qual['qualValue'] != 'True':
                    continue

                try:
                    resto = qual['restrictedTo']
                    resid = resto['resID']
                    col = resto['resComponent']['columnName']

                    try:
                        tab = priv[resid]
                    except KeyError:
                        tab = priv[resid] = set()
                    colindex = self.column_name_to_index(resid, col)

                    tab.add(colindex)

                except KeyError:
                    pass

        except KeyError:
            pass

        return priv


    def column_name_to_index(self, resid, colname):
        for res in self.dataDoc['dataResources']:
            if res['resID'] == resid:
                for col in res['columns']:
                    if col['colName'] == colname:
                        return col['colIndex']
                
                
    def select_optimizer(self):

        if hasattr(self, 'cr_backend') and self.cr_backend is not None:
            self.backend = self.cr_backend
        else:
            self.backend = 'TPOT'

        logging.info("CR Backend set to %s" % self.backend)

        try:
            # TODO: Refactor this (after pip delivery) so the variables gets populated automatically, or not
            # For some problem types we will specify the task type in the config file
            if self.task_type is not None:
                self.taskType = self.task_type
            logging.info("iLooking up task type in sri_tpot: %s" % self.taskType)
            cls = self.optimizer_class_map[self.taskType]
            logging.info("Requesting optimizer class: %s" % cls)
            if type(cls) is dict:
                cls = cls[self.backend]
        except KeyError:
            try:
                cls = self.metric_optimizer[self.metric]
                if type(cls) is dict:
                    cls = cls[self.backend]
            except KeyError:
                 raise NotImplementedError()

        return cls(config=self)


    def data_resource_types(self):
        return [ r['resType'] for r in self.dataDoc['dataResources'] ]

    
    def key_table_indexes(self):
        resources = self.dataDoc['dataResources']
        # This assumes that only a single table can have a target column
        target_tab = next((e for e in resources 
                          if 'columns' in e and 
                              any('suggestedTarget' in c['role'] 
                                  for c in e['columns'])), None)
        table_index = target_tab['resID']
        # This assumes that the table has only a single target
        target_col = next(c for c in target_tab['columns'] 
                          if 'suggestedTarget' in c['role'])
        return (table_index, target_col['colIndex'])


    def column_description_index(self):
        tab, col = self.key_table_indexes()
        return tab


    def target_index(self):
        tab, col = self.key_table_indexes()
        return col


    def column_names_old(self, rename_target=True):
        datasetSchema = self.dataDoc
        tab, col = self.key_table_indexes()
        column_names = [ item['colName'] 
                         for item in datasetSchema['dataResources'][int(tab)]['columns'] ]
        if rename_target:
            column_names[col] = 'target'
        return column_names


    def column_names(self, table_index=None):
        if table_index is None:
            table_index, col = self.key_table_indexes()
        return [ item['colName'] for item in 
                 self.dataDoc['dataResources'][int(table_index)]['columns'] ]


    def get_target_name(self):
        return self.target_column_name


    def d3m_indices(self, dataset):
        """
        Return the D3M indices of the items in the key learning table
        in a D3M dataset as a list.
        """
        tab, col = self.key_table_indexes()
        return dataset[tab]['d3mIndex'].tolist()


    def code_directory(self):
        return "%s" % self.base_directory


    def table_references(self, table_index):
        columns = self.dataDoc['dataResources'][int(table_index)]['columns']
        for col in columns:
            if 'key' in col['role']:
                try:
                    ref = col['refersTo']
                    tabref = ref['resID']
                    colref = ref['resObject']['columnName']
                    yield (tabref, colref)
                except KeyError:
                    pass

    def optimizer_arguments(self):
        if hasattr(self, 'optimizer_args'):
            for k, v in self.optimizer_args.items():
                yield (k, v)

    def preamble_arguments(self):
        if hasattr(self, 'preamble_args'):
            for k, v in self.preamble_args.items():
                yield (k, v)

    def fit_arguments(self):
        if hasattr(self, 'fit_args'):
            for k, v in self.fit_args.items():
                yield (k, v)

    def grammar_rule(self):
        if hasattr(self, 'grammar_file_name'):
            return (self.grammar_file_name, self.grammar_rule_name)
        else:
            return (None, None)

    def enable_pipeline_caching(self):
        if hasattr(self, 'pipeline_caching'):
            return self.pipeline_caching
        else:
            return False

    def augmentation_enabled(self):
        return self.datamart_service() is not None

    def datamart_service(self):
        if hasattr(self, 'datamart_provider'):
            logging.info("Datamart Provider being set to: %s" % self.datamart_provider)
            return self.datamart_provider
        logging.info("Datamart Provider Defaulting to NYU")
        return 'NYU'

    def ensembling_enabled(self):
        return hasattr(self, 'ensemble_n') and self.ensemble_n > 1

    def gama_postprocessor(self):
        if not hasattr(self, 'ensemble_n') or self.ensemble_n == 1:
            return BestFitPostProcessing()
        else:
            return EnsemblePostProcessing(ensemble_size=self.ensemble_n)