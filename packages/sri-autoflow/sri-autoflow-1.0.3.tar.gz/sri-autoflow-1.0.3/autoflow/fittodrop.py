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
Main entry point for the SRI TA2 command line search command
'''
def main():
    pipeline = sys.argv[1]
    train_csv_file = sys.argv[2]
    test_csv_file = sys.argv[3]
    target_column = sys.argv[4]

    train_d3m_dataset = generate_d3m_dataset(train_csv_file, target_column, "train")
    test_d3m_dataset = generate_d3m_dataset(test_csv_file, target_column, "test")

    # problem = dataset_util.generate_problem_description(train_d3m_dataset,
    #                                                     task="binary_classification",
    #                                                     performance_metrics="ACCURACY")

    # problem_description = problem.to_json_structure(canonical=True)
    # from d3m.metadata.problem import problem_serializer
    # prob_desc = problem_serializer(problem_description)

    from d3m.metadata import base as metadata_base, hyperparams as hyperparams_module, pipeline as pipeline_module, problem
    from d3m.container.dataset import Dataset
    from d3m.runtime import Runtime

    # Loading problem description.
    problem_description = problem.parse_problem_description('../data/inputs/185_baseball_MIN_METADATA/185_baseball_MIN_METADATA_problem/problemDoc.json')

    # Loading dataset.
    # path = 'file://{uri}'.format(uri=os.path.abspath('datasetDoc.json'))
    # dataset = Dataset.load(dataset_uri=path)

    # Loading pipeline description file.
    with open('../data/558d6adc-1fec-49f2-86b2-949cacd62dfb.json', 'r') as file:
        pipeline_description = pipeline_module.Pipeline.from_json(string_or_file=file)

    # Creating an instance on runtime with pipeline description and problem description.
    runtime = Runtime(pipeline=pipeline_description, problem_description=problem_description,
                      context=metadata_base.Context.TESTING)

    # Fitting pipeline on input dataset.
    fit_results = runtime.fit(inputs=[test_d3m_dataset])
    fit_results.check_success()

    # Producing results using the fitted pipeline.
    # produce_results = runtime.produce(inputs=[dataset])
    # produce_results.check_success()

    score_results = runtime.score(inputs=[test_d3m_dataset])
    score_results.check_success()

    print(score_results.values)


    # json_structure = json.dumps(problem_description, indent=2)

    # problem_dir = "/output/problem"
    # if not os.path.exists(problem_dir):
    #     os.makedirs(problem_dir)

    # with open("%s/problemDoc.json" % problem_dir, "w") as outfile:
    #     outfile.write(json_structure)

    # from d3m.metadata.problem import D3MProblemLoader
    # loader = D3MProblemLoader()
    # problem_loaded = loader.load(problem_uri="file://localhost/output/problem/problemDoc.py")



def generate_d3m_dataset(csv_file, target_column, dataset_type):
    # Load the CSV into a Dataset object
    dataset = Dataset.load("file://%s" % csv_file)
    # Convert the dataset into a DataFrame
    dataframe = pd.DataFrame(dataset['learningData'], None, dataset['learningData'].columns)
    # Get the target column index from the column name
    index = int(numpy.where(dataset['learningData'].columns == target_column)[0][0])
    # Convert the DataFrame into a D3M Dataset
    d3mdataset = dataset_util.get_dataset(dataframe, target_index=index, index_column=0)
    # Write the d3m dataset out (?)
    # d3mdataset.save("file://localhost/output/%s/datasetDoc.json" % dataset_type)
    return d3mdataset


'''
Entry point - required to make python happy
NOTE: We cannot use the plac library here as it is not compatible with a pip installed end points
'''
if __name__ == "__main__":
    main()




    # Call the Reference Runtime on the D3M Dataset to complete the fit-score call
    #python3 -m d3m runtime fit-produce -p pipeline.json -r problem/problemDoc.json
    # -i dataset_TRAIN/datasetDoc.json -t dataset_TEST/datasetDoc.json -o results.csv -O pipeline_run.yml

    # From run on Jig:
    # fit-score -p /output/pipelines_ranked/234530ec-6961-4a1f-8f24-cf5e8616964b.json
    #         -r /input/SEMI_1053_jm1_MIN_METADATA_problem/problemDoc.json
    #         -i /input/TRAIN/dataset_TRAIN/datasetDoc.json
    #         -t /input/TEST/dataset_TEST/datasetDoc.json
    #         -a /input/SCORE/dataset_SCORE/datasetDoc.json
    #         -o /output/predictions/234530ec-6961-4a1f-8f24-cf5e8616964b/predictions.csv
    #         -O /output/pipeline_runs/234530ec-6961-4a1f-8f24-cf5e8616964b/pipeline_run.yml
    #         -c /output/scores/234530ec-6961-4a1f-8f24-cf5e8616964b/scores.csv

    # Local pipeline and input data that produces scores:
    # python -m d3m runtime fit-score -p data/output/185_baseball_MIN_METADATA/pipelines_ranked/0af39257-9a9d-48ee-ad1d-3d68811ff575.json -r data/inputs/185_baseball_MIN_METADATA/185_baseball_MIN_METADATA_problem/problemDoc.json -i data/inputs/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/datasetDoc.json -t data/inputs/185_baseball_MIN_METADATA/TEST/dataset_TEST/datasetDoc.json -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json
    # python -m d3m runtime fit-score
    #           -p data/output/185_baseball_MIN_METADATA/pipelines_ranked/0af39257-9a9d-48ee-ad1d-3d68811ff575.json
    #           -r data/inputs/185_baseball_MIN_METADATA/185_baseball_MIN_METADATA_problem/problemDoc.json
    #           -i data/inputs/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/datasetDoc.json
    #           -t data/inputs/185_baseball_MIN_METADATA/TEST/dataset_TEST/datasetDoc.json
    #           -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json

    # Pip installed pipeline and input data that produces scores:
    # python -m d3m runtime fit-score -p ../../test-package/output/learningData/pipelines_ranked/f8429add-9e30-43f8-86ec-82f46f628dae.json  -r data/inputs/185_baseball_MIN_METADATA/185_baseball_MIN_METADATA_problem/problemDoc.json -i data/inputs/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/datasetDoc.json -t data/inputs/185_baseball_MIN_METADATA/TEST/dataset_TEST/datasetDoc.json -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json
    # python -m d3m runtime fit-score
    #           -p ../../test-package/output/learningData/pipelines_ranked/f8429add-9e30-43f8-86ec-82f46f628dae.json
    #           -r data/inputs/185_baseball_MIN_METADATA/185_baseball_MIN_METADATA_problem/problemDoc.json
    #           -i data/inputs/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/datasetDoc.json
    #           -t data/inputs/185_baseball_MIN_METADATA/TEST/dataset_TEST/datasetDoc.json
    #           -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json

    # Pip installed pipeline plus generated train & test datasetDocs - Error in Construct Pred: ValueError: Cannot find an index column in reference data, but index column is required.
    # python -m d3m runtime fit-score -p ../../test-package/output/learningData/pipelines_ranked/f8429add-9e30-43f8-86ec-82f46f628dae.json -i data/output/train/datasetDoc.json -t data/output/test/datasetDoc.json -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json
    # python -m d3m runtime fit-score
    #         -p ../../test-package/output/learningData/pipelines_ranked/f8429add-9e30-43f8-86ec-82f46f628dae.json
    #         -i data/output/train/datasetDoc.json
    #         -t data/output/test/datasetDoc.json
    #         -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json

    # Same as above but with supplied train & test datasetDocs - Error - ValueError: Input data has no columns matching semantic types ('https://metadata.datadrivendiscovery.org/types/TrueTarget',)
    # python -m d3m runtime fit-score -p ../../test-package/output/learningData/pipelines_ranked/f8429add-9e30-43f8-86ec-82f46f628dae.json -i data/inputs/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/datasetDoc.json -t data/inputs/185_baseball_MIN_METADATA/TEST/dataset_TEST/datasetDoc.json -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json
    # python -m d3m runtime fit-score
    #         -p ../../test-package/output/learningData/pipelines_ranked/f8429add-9e30-43f8-86ec-82f46f628dae.json
    #         -i data/inputs/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/datasetDoc.json
    #         -t data/inputs/185_baseball_MIN_METADATA/TEST/dataset_TEST/datasetDoc.json
    #         -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json

    #
    # python -m d3m runtime fit-score -p ../../test-package/output/learningData/pipelines_ranked/f8429add-9e30-43f8-86ec-82f46f628dae.json  -r data/inputs/185_baseball_MIN_METADATA/185_baseball_MIN_METADATA_problem/problemDoc.json -i data/output/train/datasetDoc.json -t data/output/test/datasetDoc.json -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json

    # Ok - this one will produce actual predictions using all pip installed stuff:
    # python -m d3m runtime fit-produce -i data/output/train/datasetDoc.json -t data/output/test/datasetDoc.json -p data/558d6adc-1fec-49f2-86b2-949cacd62dfb.json -o output.txt

    # Next lets see if we can get some scores out of it:
    # All pip stuff except for the score doc - it complains about ValueError: No true target columns.
    # python -m d3m runtime fit-score -i data/output/train/datasetDoc.json -t data/output/test/datasetDoc.json -a data/inputs/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/datasetDoc.json -p data/558d6adc-1fec-49f2-86b2-949cacd62dfb.json -e ACCURACY

