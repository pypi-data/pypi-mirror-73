import sys
import logging
from d3m.container import Dataset
import pandas as pd
import numpy
import json

# init logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')

# https://stackoverflow.com/questions/43728431/relative-imports-modulenotfounderror-no-module-named-x
# This main script is seen as the __main__ modules so it does not know anything about belonging to a package. The
# addition of the running directory to the sys path helps the system find the autoflow package
import os
sys.path.append(os.path.dirname("."))
_logger = logging.getLogger(__name__)

import autoflow.util.dataset_util as dataset_util

'''
Main entry point for the SRI TA2 command line fit-produce command

This is the type of command we are trying to duplicate:
python -m d3m runtime fit-produce -i data/output/train/datasetDoc.json -t data/output/test/datasetDoc.json -p data/558d6adc-1fec-49f2-86b2-949cacd62dfb.json -o output.txt

'''
def main():
    pipeline = sys.argv[1]
    train_csv_file = sys.argv[2]
    test_csv_file = sys.argv[3]
    target_column = sys.argv[4]

    train_d3m_dataset = generate_d3m_dataset(train_csv_file, target_column, "train")
    test_d3m_dataset = generate_d3m_dataset(test_csv_file, target_column, "test")

    from d3m.metadata import base as metadata_base, hyperparams as hyperparams_module, pipeline as pipeline_module, problem
    from d3m.runtime import Runtime

    # Loading pipeline description file.
    with open(pipeline, 'r') as file:
        pipeline_description = pipeline_module.Pipeline.from_json(string_or_file=file)

    # Creating an instance of the reference runtime with a pipeline description
    runtime = Runtime(pipeline=pipeline_description, context=metadata_base.Context.TESTING)

    # Fitting pipeline on input dataset.
    fit_results = runtime.fit(inputs=[train_d3m_dataset])
    fit_results.check_success()

    score_results = runtime.produce(inputs=[test_d3m_dataset])
    score_results.check_success()

    column_count = len(score_results.values['outputs.0'].columns)

    for column_index in range(column_count):
        column = score_results.values['outputs.0'].columns[column_index]
        if column_index + 1 == column_count:
            print('%s' % column)
        else:
            print('%s,' % column, end = '')

    value_count = len(score_results.values['outputs.0'].values)
    for value_index in range(value_count):
        value = score_results.values['outputs.0'].values[value_index]
        for column_index in range(column_count):
            if column_index + 1 == column_count:
                print('%s' % value[column_index])
            else:
                print('%s,' % value[column_index], end='')


def generate_d3m_dataset(csv_file, target_column, dataset_type):
    # Load the CSV into a Dataset object
    dataset = Dataset.load("file://%s" % csv_file)
    # Convert the dataset into a DataFrame
    dataframe = pd.DataFrame(dataset['learningData'], None, dataset['learningData'].columns)
    # Get the target column index from the column name
    index = int(numpy.where(dataset['learningData'].columns == target_column)[0][0])
    # Convert the DataFrame into a D3M Dataset
    d3mdataset = dataset_util.get_dataset(dataframe, target_index=index, index_column=0)
    # No need to write it out unless we want to debug by running on the command line - keep d3m artifacts in memory
    # d3mdataset.save("file://localhost/output/%s/datasetDoc.json" % dataset_type)
    return d3mdataset


'''
Entry point - required to make python happy
NOTE: We cannot use the plac library here as it is not compatible with a pip installed end points
'''
if __name__ == "__main__":
    main()
