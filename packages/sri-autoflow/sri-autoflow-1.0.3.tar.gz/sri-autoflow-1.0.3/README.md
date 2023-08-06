## Table of contents

1. [What is in this repository](#what-is-in-this-repository)
2. [Related repositories](#related-repositories)
3. [Installation](#installation)
    - [Pip](#pip)
    - [Docker](#docker)
    - [Kubernetes](#kubernetes)
    - [Conda Development Environment](#conda-development-environment)
    - [Docker Development Environment](#docker-development-environment)



## What is in this repository
This repository is for the Autoflow Pipeline optimization tool. Autoflow explores available primitives and 
constructs pipelines to address various types of problems. The back end that performs the pipeline search
is the Genetic Algorithm called [GAMA](https://github.com/PGijsbers/gama.git). This application was developed during the
DARPA sponsored D3M project. 


## Related repositories
Repo where we keep this code: https://gitlab.com/daraghhartnett/tpot-ta2
Repo where we keep our TA3 ready image for use by anyone: https://gitlab.com/daraghhartnett/autoflow
Repo where we push images to so the evaluation repos can use the core TA2: https://gitlab.datadrivendiscovery.org/j18_TA2Eval/SRI_TPOT


## Installation
There are various ways of using the Autoflow tool. Each is explained below.


### Pip
1. Before starting, it is recommended that you create a conda environment using the following commands. This will allow
you to keep the environment used to support Autoflow separate from your other work:

    ```conda create -n <environment name> python=3.6.9```<br>
    ```conda activate <environment name>```

2. Due to current project state there are some extra, temporary steps that are required to install Autoflow. It is 
expected that each of these will be addressed by projects end which will allow a simple pip install. The first of these 
extra steps is to install dependencies that cannot be captured by the python setup tools. Download the requirements.txt
file located [here](https://gitlab.com/daraghhartnett/tpot-ta2/-/blob/master/requirements.txt) and run the following 
in the conda environment you created in the previous step:

    ```pip install -r requirements.txt```
    
3. Run pip install to get the released version of the sri-autoflow library. Other versions of Autoflow are available on 
[PyPi](https://pypi.org/project/sri-autoflow/):

    ```pip install sri-autoflow==1.0.2```
    
4. Edit the conda installed lib/python3.6/site-packages/d3m/index.py file to remove the reference to pycurl. This has 
been fixed in a later version of d3m core so this step should not be necessary for long. If you are unable to find the 
location of this file, simply run autoflow in the next step and it will print an exception showing the full path to the 
file. Here is what the error looks like:

    ```
    ... 
      File "/Users/user1/miniconda3/envs/test-package/lib/python3.6/site-packages/d3m/index.py", line 21, in <module>
        import pycurl  # type: ignore
    ImportError: pycurl: libcurl link-time ssl backend (openssl) is different from compile-time ssl backend (none/other)
    ``` 

    The line that needs to be commented out is line number 21:

    ```import pycurl  # type: ignore```
    
5. Depending on your version of python and your platform it is possilkle you will see errors related to xgboost which is
required for some of the common primitives. If that occurs, run the following commands to build the binaries manually:
    
    ```
    git clone --recursive https://github.com/dmlc/xgboost
    cd xgboost; cp make/minimum.mk ./config.mk; make -j4
    cd python-package; python setup.py develop --user
    ```
    
6. Set the AUTOFLOW_WITH_NO_DOCKER environment variable to True. This is required so that primitives that are difficult
to install are not imported when running Autoflow. It is likely that as we near the conclusion of the program that the
offending primitives will be easier to install and this step can be skipped but for now it is necessary:
    
    ```export AUTOFLOW_WITH_NO_DOCKER=True```

7. Autoflow is now ready to use! In the following steps we will explain how to search and apply solutions for two common
problem types, binary classification and regression. In order to search for solutions to a problem you will need the following:

    - Single table csv file with column names. An example of this for the baseball dataset, a classification problem, can be viewed 
    [here](https://gitlab.datadrivendiscovery.org/d3m/datasets/blob/master/seed_datasets_current/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/tables/learningData.csv)
      An example of this for the autoMpg dataset, a regression problem, can be viewed [here](https://gitlab.datadrivendiscovery.org/d3m/datasets/blob/master/seed_datasets_current/196_autoMpg_MIN_METADATA/TRAIN/dataset_TRAIN/tables/learningData.csv)
    - Target column name that should be used to train the model. Following the example of the baseball dataset, the 
    'Hall_of_Fame' column is generally used. For the autoMpg problem, the 'class' column is generally used.
    - Configuration file. Sample configuration files can be found viewed in the autoflow repository for [classification](https://gitlab.com/daraghhartnett/tpot-ta2/-/blob/master/config/search_config_binary_classification.json)
      and [regression](https://gitlab.com/daraghhartnett/tpot-ta2/-/blob/master/config/search_config_regression.json)
     This contains parameters to guide Autoflow in its search:
        - Where to write the output of the search
        - Time limit to search for pipelines in minutes 
        - Maximum number of CPU's
        - Maximum RAM allocation 
        - Metric to use when scoring the predictions (Values of mean_squared_error for regression and accuracy for binary classificaiton have been tested)
        - Task Type (classification and regression have been tested)
        - Some other internal parameters dealing with the backend
    
8. Using the example inputs described in the previous step, start by searching for pipelines to solve the problem using
the autoflow-search call. Here is the call format to use:

    ```autoflow-search <training-data-csv> <config-file> <target-column-name>```

   Here are sample calls to autoflow-search for the baseball and autoMpg problems:

    ```autoflow-search /datasets/seed_datasets_current/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/tables/learningData.csv search_config_binary_classification.json Hall_of_Fame```
    ```autoflow-search /datasets/seed_datasets_current/196_autoMpg_MIN_METADATA/TRAIN/dataset_TRAIN/tables/learningData.csv search_config_regression.json class```
    
    This will produce output like the following (output for the classification problem, summarized for clarity):
    
    ```
    2020-07-08 09:37:41,544 [WARNING] d3m.namespace -- While loading primitive 'classification.gaussian_naive_bayes.SKlearn', an error has been detected: (numpy 1.19.0 (/Users/daraghhartnett/miniconda3/envs/test-package/lib/python3.6/site-packages), Requirement.parse('numpy<=1.18.2,>=1.15.4'), {'d3m'})
    2020-07-08 09:37:41,544 [WARNING] d3m.namespace -- Attempting to load primitive 'classification.gaussian_naive_bayes.SKlearn' without checking requirements.
    ...
    2020-07-08 09:37:45,343 [INFO] autoflow.main -- Running SRI TA2 Search (Version 2020.05.18) on problem: learningData.csv
    2020-07-08 09:37:45,344 [INFO] autoflow.optimizer -- optimizer::fit() called
    2020-07-08 09:37:45,344 [INFO] autoflow.optimizer -- 	optimizer::fit() calling prep_data
    ...
    2020-07-08 09:37:49,875 [INFO] gama.genetic_programming.compilers.scikitlearn -- Evaluating individual: Individual d1597029-f5ee-4452-9621-72384b6e1ec0
    Pipeline: AF_SKMultinomialNB(AF_SKSelectPercentile(data, AF_SKSelectPercentile.percentile=34, AF_SKSelectPercentile.score_func='f_classif'), AF_SKMultinomialNB.alpha=100.0, AF_SKMultinomialNB.fit_prior=False)
    Fitness: None
    [0.904]
    2020-07-08 09:37:49,888 [INFO] autoflow.optimizer -- Internal scores for Problem: learningData.csv. Inserted pipeline with score 0.885000 into nbest. Current size: (4)
    2020-07-08 09:37:49,892 - gama.genetic_programming.compilers.scikitlearn - INFO - Evaluating individual: Individual bc7b8ad4-86b6-4060-b16a-94f6720153d0
    Pipeline: AF_SKDecisionTreeClassifier(AF_SKFeatureAgglomeration(data, AF_SKFeatureAgglomeration.affinity='cosine', AF_SKFeatureAgglomeration.linkage='ward'), AF_SKDecisionTreeClassifier.criterion='entropy', AF_SKDecisionTreeClassifier.max_depth=2, AF_SKDecisionTreeClassifier.min_samples_leaf=3, AF_SKDecisionTreeClassifier.min_samples_split=5)
    ...
    2020-07-08 09:43:12,697 [INFO] sri.d3mglue.d3mwrap -- Warning: Suppressing value of False for use_semantic_types of SKAdaBoostClassifier
    2020-07-08 09:43:15,655 [INFO] autoflow.optimizer -- Checkpointed 75 considered pipelines
    2020-07-08 09:43:15,656 [INFO] autoflow.main -- Completed Search phase for problem: learningData.csv
    ```
    
9. Once the search is complete (see final log message in the previous step), look in the folder specified as the output directory
 in the config file. The following file structure should be visible:
 
    ```angular2
    drwxr-xr-x   2 user  staff    64 Jul  7 17:00 additional_inputs
    drwxr-xr-x   2 user  staff    64 Jul  7 17:00 pipeline_runs
    drwxr-xr-x  42 user  staff  1344 Jul  7 17:11 pipelines_ranked
    drwxr-xr-x  74 user  staff  2368 Jul  7 17:11 pipelines_scored
    drwxr-xr-x   2 user  staff    64 Jul  7 17:00 pipelines_searched
    drwxr-xr-x   2 user  staff    64 Jul  7 17:00 subpipelines
    drwxr-xr-x   2 user  staff    64 Jul  7 17:11 temp
    ```
       
    Inside the `pipelines_ranked` directory there will be two files for each of the 20 best pipelines. The files are 
    grouped by the pipline UID which has the following form: `0eaa146d-d569-4ec7-9780-5d7a770b1c62`. The first file is a 
    `.rank` file which as the rank of that pipeline. A rank of `1` is considered the best, a rank of `20` is considered
    the poorest. The `.json` file describes the pipeline in detail. For information on how to interpret this file 
    structure see the [D3M Pipeline documentation](https://docs.datadrivendiscovery.org/v2020.5.18/pipeline.html#pipeline)
    
    The `pipelines_scored` directory contains all the other pipelines that were found during search but were deemed to 
    not be as good as the 20 ranked pipelines.
    
10. Now that pipelines have been discovered, they can be run on hold out data to see how they perform at predicting the 
values in the target column. An example of such test data for the baseball dataset can be found 
[here](https://gitlab.datadrivendiscovery.org/d3m/datasets/blob/master/seed_datasets_current/185_baseball_MIN_METADATA/TEST/dataset_TEST/tables/learningData.csv),
and for the autoMpg dataset, [here](https://gitlab.datadrivendiscovery.org/d3m/datasets/blob/master/seed_datasets_current/196_autoMpg_MIN_METADATA/TEST/dataset_TEST/tables/learningData.csv)    

    To run the pipelines on the test data and produce predictons for the target column, the autoflow library has a 
    command called `autoflow-fit-produce`. This can be invoked as follows:
    
    ```autoflow-fit-produce <pipeline.json> <training-data-csv> <test-data-csv> <target-column-name>```
    
    Here are sample calls to autoflow-fit-produce for the baseball and autoMpg problems:

    ```autoflow-fit-produce output/learningData/pipelines_ranked/f5fafeb8-fe7d-4194-a468-a7b8746e1d9b.json /datasets/seed_datasets_current/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/tables/learningData.csv /datasets/seed_datasets_current/185_baseball_MIN_METADATA/TEST/dataset_TEST/tables/learningData.csv Hall_of_Fame```
    ```autoflow-fit-produce output/learningData/pipelines_ranked/ecdd740c-27de-4c7a-aeed-e5f118a28ea4.json /datasets/seed_datasets_current/196_autoMpg_MIN_METADATA/TRAIN/dataset_TRAIN/tables/learningData.csv /datasets/seed_datasets_current/196_autoMpg_MIN_METADATA/TEST/dataset_TEST/tables/learningData.csv class```
    
    Following is some sample output from the baseball predictions, truncated for clarity.
    
    ```
    d3mIndex,Hall_of_Fame
    2,0
    9,0
    14,0
    15,0
    ...
    ```
    
11. To get an idea of how accurate the predictions are, the **autoflow-fit-score** function can be used. This call 
requires a csv that contains the true values of the target column for the test data, this is called score data. An 
example of such score data for the baseball dataset can be found [here](https://gitlab.datadrivendiscovery.org/d3m/datasets/blob/master/seed_datasets_current/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/tables/learningData.csv),
and for the autoMpg dataset, [here](https://gitlab.datadrivendiscovery.org/d3m/datasets/blob/master/seed_datasets_current/196_autoMpg_MIN_METADATA/SCORE/dataset_SCORE/tables/learningData.csv)
To produce a performance score for the chosen pipeline, the autoflow library has a command called `autoflow-fit-score`. 
This can be invoked as follows:

    ```autoflow-fit-score <pipeline.json> <training-data-csv> <test-data-csv> <score-data-csv> <target-column-name> <config-file>```

Note, use the same config file used in the autoflow-search call. Here are sample calls to autoflow-fit-score for the 
baseball and autoMpg problems:

    ```autoflow-fit-score output/learningData/pipelines_ranked/f5fafeb8-fe7d-4194-a468-a7b8746e1d9b.json /datasets/seed_datasets_current/185_baseball_MIN_METADATA/TRAIN/dataset_TRAIN/tables/learningData.csv /datasets/seed_datasets_current/185_baseball_MIN_METADATA/TEST/dataset_TEST/tables/learningData.csv /datasets/seed_datasets_current/185_baseball_MIN_METADATA/SCORE/dataset_SCORE/tables/learningData.csv Hall_of_Fame search_config_binary_classification.json```
    ```autoflow-fit-score output/learningData/pipelines_ranked/ecdd740c-27de-4c7a-aeed-e5f118a28ea4.json /datasets/seed_datasets_current/196_autoMpg_MIN_METADATA/TRAIN/dataset_TRAIN/tables/learningData.csv /datasets/seed_datasets_current/196_autoMpg_MIN_METADATA/TEST/dataset_TEST/tables/learningData.csv /datasets/seed_datasets_current/196_autoMpg_MIN_METADATA/SCORE/dataset_SCORE/tables/learningData.csv class search_config_regression.json```
     
    Following is some sample output from the baseball predictions, truncated for clarity.
    
    ```
       metric,value,normalized,randomSeed
       ACCURACY,0.9363295880149812,0.9363295880149812,0
    ```
    
 
12. If you ever need to remove your conda environment to start over use the following commands:

    ```conda deactivate```<br>
    ```conda remove -n <environment name> --all```
    
13. Following is a list of the things we need to improve in the short term, please feel free to add a feature request
to the list:

    - Suppress unhelpful logging (warnings about non compliant primitives etc)
    - Implement better file/problem name management (currently all output goes into output/learningData)
    - Support all problem types (currently only classification and regression problems are supported)


### Docker


### Kubernetes


### Conda Development Environment


### Docker Development Environment

