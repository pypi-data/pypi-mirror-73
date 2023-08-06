## Table of contents

1. [What is in this repository](#what-is-in-this-repository)
2. [Related repositories](#related-repositories)
3. [Installation](#installation)
    - [Pip](#pip)
    - [Docker](#docker)
    - [Kubernetes](#kubernetes)
    - [Conda Development Environment](#conda-development-environment)
    - [Docker Development Environment](#docker-development-environment)




## 1. What is in this repository
This repository is for the Autoflow Pipeline optimization tool. Autoflow explores available primitives and 
constructs pipelines to address various types of problems. The back end that performs the pipeline search
is the Genetic Algorithm called [GAMA](https://github.com/PGijsbers/gama.git). This application was developed during the
DARPA sponsored D3M project. 

## 2. Related repositories


## 3. Installation
There are various ways of using the Autoflow tool. Each is explained below.

### 3.1 Pip
1. Before starting, it is recommended that you create a conda environment using the following commands. This will allow
you to keep the environment used to support Autoflow separate from your other work:

    ```conda create -n <environment name> python=3.6.9```<br>
    ```conda activate <environment name>```

     It may be necessary to enter 'y' occasionally to accept the install suggestions.

2. Due to current project state there are some extra, temporary steps that are required to install Autoflow. It is 
expected that each of these will be addressed by projects end which will allow a simple pip install. The first of these 
extra steps is to install dependencies that cannot be captured by the python setup tools. Download the requirements.txt
file located in the base directory of this repository and run the following in the conda environment you created in 
step one:

    ```pip install -r requirements.txt```
    
    It may be necessary to enter 'y' occasionally to accept the install suggestions.
    
3. 

10. If you ever need to remove your conda environment to startover use the following command:

    ```conda remove -n test-package --all```


### 3.2 Docker


### 3.3 Kubernetes


### 3.4 Conda Development Environment


### 3.5 Docker Development Environment


Pip installable instructions:
=============================
- Autoflow is now pip installable. Before starting, it is recommended that you create a conda environment using the
  following commands:

    > conda create -n <environment name> python=3.6.9
    > conda activate <environment name>

- This step will no longer be needed if we upgrade to Python 3.7 or xgboost 1.1.0. XGBoost, which is needed for some
  D3M libraries needs some special installation:

    git clone --recursive https://github.com/dmlc/xgboost
    cd xgboost; cp make/minimum.mk ./config.mk; make -j4
    cd python-package; python setup.py develop --user

- pip install autoflow-1.0.0-py3-none-any.whl

- This is fixed in the post 20200518 release of d3mcore.
  When you run autoflow you will get an error like this:

    (test-package) AIC-CAS0013240-Bering:test-package daraghhartnett$ autoflow
    Traceback (most recent call last):
      File "/Users/daraghhartnett/miniconda3/envs/test-package/bin/autoflow", line 5, in <module>
        from autoflow.main import main
      File "/Users/daraghhartnett/miniconda3/envs/test-package/lib/python3.6/site-packages/autoflow/main.py", line 15, in <module>
        from .autoflowconfig import AutoflowConfig
      File "/Users/daraghhartnett/miniconda3/envs/test-package/lib/python3.6/site-packages/autoflow/autoflowconfig.py", line 3, in <module>
        from .optimizer import TPOTClassificationOptimizer
      File "/Users/daraghhartnett/miniconda3/envs/test-package/lib/python3.6/site-packages/autoflow/optimizer.py", line 31, in <module>
        from d3m.metadata.pipeline import PlaceholderStep
      File "/Users/daraghhartnett/miniconda3/envs/test-package/lib/python3.6/site-packages/d3m/metadata/pipeline.py", line 18, in <module>
        from d3m import container, deprecate, environment_variables, exceptions, index, utils
      File "/Users/daraghhartnett/miniconda3/envs/test-package/lib/python3.6/site-packages/d3m/index.py", line 21, in <module>
        import pycurl  # type: ignore

  Edit index.py mentioned in the last file in the exception and comment out the 'import pycurl' line

- SKLearn also has a problem with the install - we cant seem to specify a source git clone in the setup.py so you need to run this
  manually:

    pip install -e git+https://gitlab.com/datadrivendiscovery/sklearn-wrap.git@dist#egg=sklearn_wrap



Docker repos:
=============
Repo where we keep this code: https://gitlab.com/daraghhartnett/tpot-ta2
Repo where we keep our TA3 ready image for use by anyone: https://gitlab.com/daraghhartnett/autoflow
Repo where we push images to so the evaluation repos can use the core TA2: https://gitlab.datadrivendiscovery.org/j18_TA2Eval/SRI_TPOT


<a name="Related-Repositories"/>

## Related Repositories
