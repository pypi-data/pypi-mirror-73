import sys
import logging
from d3m.container import Dataset
import pandas as pd
import numpy
import json
import shutil

from d3m.metadata import base as metadata_base, hyperparams as hyperparams_module, pipeline as pipeline_module, problem
from d3m.runtime import Runtime
from d3m.runtime import score

# init logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s -- %(message)s')

# https://stackoverflow.com/questions/43728431/relative-imports-modulenotfounderror-no-module-named-x
# This main script is seen as the __main__ modules so it does not know anything about belonging to a package. The
# addition of the running directory to the sys path helps the system find the autoflow package
import os
sys.path.append(os.path.dirname("."))
_logger = logging.getLogger(__name__)

import autoflow.util.dataset_util as dataset_util

temporary_folder = "tmp"

'''
Main entry point for the SRI TA2 command line fit-score command

This is the type of command we are trying to duplicate in memory:
python -m d3m runtime fit-score 
    -r data/inputs/185_baseball_MIN_METADATA/185_baseball_MIN_METADATA_problem/problemDoc.json 
    -i data/inputs/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/datasetDoc.json 
    -t data/inputs/185_baseball_MIN_METADATA/TEST/dataset_TEST/datasetDoc.json 
    -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json 
    -p data/558d6adc-1fec-49f2-86b2-949cacd62dfb.json 
    -e ACCURACY
'''
def main():
    pipeline = sys.argv[1]
    train_csv_file = sys.argv[2]
    test_csv_file = sys.argv[3]
    score_csv_file = sys.argv[4]
    target_column = sys.argv[5]
    config_file = sys.argv[6]

    # The metric is (currently) used to determine the optimizer & task to use
    configData = json.load(open(config_file))
    metric = configData["metric"]
    if metric == "mean_squared_error":
        metric = "meanSquaredError"

    if not os.path.exists(temporary_folder):
        os.makedirs(temporary_folder)

    # Clean up any existing files in the tmp folder before starting:
    for the_file in os.listdir(temporary_folder):
        file_path = os.path.join(temporary_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            _logger.warning(e)

    train_d3m_dataset, dataset_id = generate_d3m_dataset(train_csv_file, target_column, "train")
    generate_d3m_dataset(test_csv_file, target_column, "test", dataset_id)
    generate_d3m_dataset(score_csv_file, target_column, "score", dataset_id)

    problem = dataset_util.generate_problem_description(train_d3m_dataset,
                                                        performance_metrics=metric)

    # Now write the problemDoc.json in the expected format
    json_data = json.dumps(problem)
    problem_dir = "%s/problem" % temporary_folder
    if not os.path.exists(problem_dir):
        os.makedirs(problem_dir)
    with open("%s/problem/problemDoc.json" % temporary_folder, "w") as outfile:
        outfile.write(json_data)

    command = "python -m d3m runtime fit-score -i tmp/train/datasetDoc.json -t tmp/test/datasetDoc.json " \
              "-a tmp/score/datasetDoc.json -p %s " \
              "-r tmp/problem/problemDoc.json" % pipeline

    # Absent a way to do this in memory lets run it on the bloody command line.
    os.system(command)


def generate_d3m_dataset(csv_file, target_column, dataset_type, dataset_id=None):
    # Load the CSV into a Dataset object
    dataset = Dataset.load("file://%s" % csv_file)
    # Convert the dataset into a DataFrame
    dataframe = pd.DataFrame(dataset['learningData'], None, dataset['learningData'].columns)
    # Get the target column index from the column name
    index = int(numpy.where(dataset['learningData'].columns == target_column)[0][0])
    # Convert the DataFrame into a D3M Dataset
    d3mdataset = dataset_util.get_dataset(dataframe, target_index=index, index_column=0)
    if dataset_id is not None:
        # Make sure all the datasetDoc.json files have the same datasetID, eyeroll
        d3mdataset.metadata._current_metadata.metadata._dict['id'] = dataset_id
    current_dataset_id = d3mdataset.metadata._current_metadata.metadata._dict['id']
    target_dir = "%s/%s/%s" % (os.getcwd(), temporary_folder, dataset_type)
    # No need to write it out unless we want to debug by running on the command line - keep d3m artifacts in memory
    d3mdataset.save("file://localhost/%s/datasetDoc.json" % target_dir)
    return d3mdataset, current_dataset_id


'''
Entry point - required to make python happy
NOTE: We cannot use the plac library here as it is not compatible with a pip installed end points
'''
if __name__ == "__main__":
    main()


# Old attempts to try to do this in memeory below, sigh

# Now run this:
# python -m d3m runtime fit-score -i data/output/train/datasetDoc.json -t data/output/test/datasetDoc.json -a data/output/score/datasetDoc.json -p data/output/558d6adc-1fec-49f2-86b2-949cacd62dfb.json -r data/output/problem/problemDoc.json

# Loading pipeline description file.
# with open(pipeline, 'r') as file:
#     pipeline_description = pipeline_module.Pipeline.from_json(string_or_file=file)

# Loading problem description.
# problem_description = problem.parse_problem_description('/inputs/185_baseball_MIN_METADATA/185_baseball_MIN_METADATA_problem/problemDoc.json')

# problem_description['id'] = train_d3m_dataset.metadata._current_metadata.metadata['id']
# problem_description.get('inputs', [])[0]['dataset_id'] = train_d3m_dataset.metadata._current_metadata.metadata['id']

# Creating an instance of the reference runtime with a pipeline description
# runtime = Runtime(pipeline=pipeline_description, problem_description=problem_description,
#                   context=metadata_base.Context.TESTING)

# Fitting pipeline on input dataset.
# fit_results = runtime.fit(inputs=[train_d3m_dataset])
# fit_results.check_success()

# Producing results using the fitted pipeline.
# predictions, produce_results = runtime.produce(inputs=[train_d3m_dataset])
# produce_results.check_success()

# score_results = score(predictions, metrics="ACCURACY")
# score_results.check_success()