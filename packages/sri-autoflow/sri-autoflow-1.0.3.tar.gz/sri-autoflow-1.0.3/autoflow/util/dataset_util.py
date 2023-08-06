import uuid
import numpy
import pandas as pd
from d3m.container import pandas as container_pandas
from d3m.container.dataset import Dataset
from d3m.metadata import base as metadata_base
from d3m.metadata.problem import Problem
from d3m.metadata.problem import TaskKeyword, PerformanceMetric


REGRESSION_METRICS = [
    {'metric': PerformanceMetric.MEAN_ABSOLUTE_ERROR, 'params': {}},
    {'metric': PerformanceMetric.MEAN_SQUARED_ERROR, 'params': {}},
    {'metric': PerformanceMetric.ROOT_MEAN_SQUARED_ERROR, 'params': {}},
    {'metric': PerformanceMetric.R_SQUARED, 'params': {}},
]

BINARY_CLASSIFICATION_METRICS = [
    {'metric': PerformanceMetric.ACCURACY, 'params': {}},
]

PROBLEM_DEFINITION = {
    'binary_classification': {
        'performance_metrics': BINARY_CLASSIFICATION_METRICS,
        'task_keywords': [TaskKeyword.CLASSIFICATION, TaskKeyword.BINARY]
    },
    'regression': {
        'performance_metrics': REGRESSION_METRICS,
        'task_keywords': [TaskKeyword.UNIVARIATE, TaskKeyword.REGRESSION]
    }

}


def get_dataset(input_data, target_index=-2, index_column=-1, semantic_types=None, parse=False):
    """
    A function that has as input a dataframe, and generates a D3M dataset.

    Parameters
    ----------
    input_data : pd.DataFrame
        The dataframe to be converted to d3m Dataset.
    target_index : int
        The index of the target, if index is not present, it will be ignored.
    index_column : int
        The index of the index target, if not provided it will look for d3m index, if not generate one.
    semantic_types : Sequence[Sequence[str]]
        A list of semantic types to be applied. The sequence must be of the same length of
        the dataframe columns.
    parse :
        A flag to determine if the dataset will contain parsed columns. By default is set to fault
        to make it compatible with most of D3M current infrastructure.

    Returns
    -------
    A D3M dataset.
    """
    data = make_unique_columns(input_data.copy(deep=True))
    if semantic_types is None:
        semantic_types = [[] for i in range(len(data.columns))]
        for i, _type in enumerate(input_data.dtypes):
            if _type == float:
                semantic_types[i].append('http://schema.org/Float')
            elif _type == int:
                semantic_types[i].append('http://schema.org/Integer')

    resources = {}

    if 'd3mIndex' not in data.columns:
        # We do not update digest with new data generated here. This is OK because this data is determined by
        # original data so original digest still applies. When saving a new digest has to be computed anyway
        # because this data will have to be converted to string.
        data.insert(0, 'd3mIndex', range(len(data)))
        d3m_index_generated = True
    else:
        d3m_index_generated = False

    data = container_pandas.DataFrame(data)

    # remove this
    if not parse:
        data = data.astype(str)
    metadata = metadata_base.DataMetadata()

    resources['learningData'] = data

    metadata = metadata.update(('learningData',), {
        'structural_type': type(data),
        'semantic_types': [
            'https://metadata.datadrivendiscovery.org/types/Table',
            'https://metadata.datadrivendiscovery.org/types/DatasetEntryPoint',
        ],
        'dimension': {
            'name': 'rows',
            'semantic_types': ['https://metadata.datadrivendiscovery.org/types/TabularRow'],
            'length': len(data),
        },
    })

    metadata = metadata.update(('learningData', metadata_base.ALL_ELEMENTS), {
        'dimension': {
            'name': 'columns',
            'semantic_types': ['https://metadata.datadrivendiscovery.org/types/TabularColumn'],
            'length': len(data.columns),
        },
    })

    for i, column_name in enumerate(data.columns):
        if i == index_column:
            metadata = metadata.update(('learningData', metadata_base.ALL_ELEMENTS, i), {
                'name': column_name,
                'structural_type': numpy.int64,
                'semantic_types': [
                    'http://schema.org/Integer',
                    'https://metadata.datadrivendiscovery.org/types/PrimaryKey',
                ],
            })
        else:
            _structural_type = str
            if semantic_types[i]:
                _semantic_types = semantic_types[i]
                if 'http://schema.org/Float' in _semantic_types:
                    _structural_type = numpy.float64
                elif 'http://schema.org/Integer' in _semantic_types:
                    _structural_type = numpy.int64
            else:
                _semantic_types = ['https://metadata.datadrivendiscovery.org/types/UnknownType']

            if not parse:
                _structural_type = str
            if i == target_index:
                _semantic_types += ['https://metadata.datadrivendiscovery.org/types/SuggestedTarget']
                _semantic_types += ['https://metadata.datadrivendiscovery.org/types/TrueTarget']
            else:
                _semantic_types += ['https://metadata.datadrivendiscovery.org/types/Attribute']

            metadata = metadata.update(('learningData', metadata_base.ALL_ELEMENTS, i), {
                'name': column_name,
                'structural_type': _structural_type,
                'semantic_types': _semantic_types
            })

    dataset_id = str(uuid.uuid4())
    dataset_metadata = {
        'schema': metadata_base.CONTAINER_SCHEMA_VERSION,
        'structural_type': Dataset,
        'id': dataset_id,
        'name': dataset_id,
        'digest': 'asd',
        'dimension': {
            'name': 'resources',
            'semantic_types': ['https://metadata.datadrivendiscovery.org/types/DatasetResource'],
            'length': len(resources),
        },
    }

    metadata = metadata.update((), dataset_metadata)

    dataset = Dataset(resources, metadata)
    return dataset


def make_unique_columns(data):
    """
    Parameters
    ----------
    data : pd.DataFrame
        A dataframe to fix the column names.

    Returns
    -------
    The original dataframe where the columns are strings and has a unique name/
    """
    seen_columns_name = {}
    column_names = []
    for column in data.columns:
        if column in seen_columns_name:
            column_name = str(column) + '_' + str(seen_columns_name[column])
            seen_columns_name[column] += 1
        else:
            seen_columns_name[column] = 0
            column_name = str(column)
        column_names.append(column_name)
    data.columns = column_names
    return data


def generate_problem_description(dataset, task=None, *, task_keywords=None, performance_metrics=None):
    """
    A function that simplifies the generation of a problem description.

    Parameters
    ----------
    dataset : Dataset
        Dataset to be use for pipeline search.
    task : str
        A string that represent the problem type, currently only supported: ``binary_classification`` and
        ``regression``.
    task_keywords : List[TaskKeyword]
        A list of TaskKeyword.
    performance_metrics: List[PerformanceMetric]
        A list of PerformanceMetric.

    Returns
    -------
    A Problem
    """
    dataset_id = dataset.metadata.query(())['id']
    problem_id = dataset_id + '_problem'
    schema = 'https://metadata.datadrivendiscovery.org/schemas/v0/problem.json'
    version = '4.0.0'

    target_column_index = None

    for i in range(dataset.metadata.query(('learningData', metadata_base.ALL_ELEMENTS,))['dimension']['length']):
        if 'https://metadata.datadrivendiscovery.org/types/SuggestedTarget' in \
                dataset.metadata.query(('learningData', metadata_base.ALL_ELEMENTS, i,))['semantic_types']:
            target_column_index = i
            break

    if target_column_index is None:
        raise ValueError('Input dataframe does not contains targets')

    keywords = None
    if performance_metrics == "accuracy":
        keywords = "CLASSIFICATION", "BINARY"
    else:
        keywords = "UNIVARIATE", "REGRESSION"

    about = {
        "problemID": "problem_id",
        "problemName": "problem_name"
    }

    inputs = {
        'data': [{
            'datasetID': dataset_id,
            'targets': [{
                'colIndex': target_column_index,
                'colName': dataset.metadata.query(('learningData', metadata_base.ALL_ELEMENTS, i,))['name'],
                'resID': 'learningData',
                'targetIndex': 0
            }]
        }],
        'performanceMetrics': [{
            'metric': performance_metrics,
            'taskKeywords': [
                keywords
            ]
        }]
    }

    problem_description = {
        'about' : about,
        'id': problem_id,
        'schema': schema,
        'version': version,
        'inputs': inputs,
    }

    return problem_description
