import setuptools

from autoflow.common import config

setuptools.setup(
    name = config.PACKAGE_NAME,
    version = config.VERSION,

    description = 'Autoflow is a tool that explores available primitives and assembles them into pipelines that discover'
                  ' a solution to various problem types',
    long_description = 'Autoflow is a tool that explores available primitives and assembles them into pipelines that '
                       'discover a solution to various problem types. This was developed by SRI under funding from '
                       'DARPA on the D3M Project. GAMA is the Genetic algorithm that explores the pipeline '
                       'configuration. Autoflow is also configurable to use a TPOT backend instead of GAMA.',
    keywords = ['Auto Machine Learning Tool', 'GAMA', 'TPOT', 'pipeline optimization', 'hyperparameter optimization',
                'data science', 'machine learning', 'genetic programming', 'evolutionary computation'],

    maintainer_email = config.EMAIL,
    maintainer = config.MAINTAINER,

    # The project's main homepage.
    url = config.REPOSITORY,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Programming Language :: Python :: 3.6',
    ],

    # packages = setuptools.find_packages(exclude = ['contrib', 'docs', 'tests']),
    packages = [
        'autoflow',
        'autoflow.common',
        'autoflow.util',
        'autoflow.config',
        'autoflow.pipelines',
        'autoflow.pipelines',
        'autoflow.ta2-ta3',
        'autoflow.ta2-ta3.autoflow',
    ],

    include_package_data = True,

    package_data = {
        # If any package contains *.json files, include them:
        "": ["*.json"],
    },

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = [
        'sri_tpot==1.3.0',
        'psutil>=5.6.1',
        'plac==1.0.0',
        'google-auth==1.16.1',
        'google-auth-oauthlib==0.4.1',
        'google-pasta==0.2.0',
        'protobuf==3.12.2',
        'pathos==0.2.5',
        'sri_d3m==1.9.1',
        'scikit-image==0.16.1',
        'scikit-learn==0.22.2.post1',
    ],

    python_requires = '>=3.6',

    entry_points = {
        'console_scripts': ['autoflow-search=autoflow.main:main',
                            'autoflow-fit-produce=autoflow.fit_produce:main',
                            'autoflow-fit-score=autoflow.fit_score:main'],
    }

)
