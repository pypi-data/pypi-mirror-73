import numpy as np

from d3m.primitives.regression.extra_trees import SKlearn as SKExtraTreesRegressor
from d3m.primitives.regression.gradient_boosting import SKlearn as SKGradientBoostingRegressor
from d3m.primitives.regression.decision_tree import SKlearn as SKDecisionTreeRegressor
from d3m.primitives.regression.k_neighbors import SKlearn as SKKNeighborsRegressor
from d3m.primitives.regression.linear_svr import SKlearn as SKLinearSVR
from d3m.primitives.regression.random_forest import SKlearn as SKRandomForestRegressor

from d3m.primitives.data_transformation.fast_ica import SKlearn as SKFastICA
from d3m.primitives.data_preprocessing.feature_agglomeration import SKlearn as SKFeatureAgglomeration
from d3m.primitives.data_preprocessing.min_max_scaler import SKlearn as SKMinMaxScaler
from d3m.primitives.data_preprocessing.nystroem import SKlearn as SKNystroem
from d3m.primitives.feature_extraction.pca import SKlearn as SKPCA
from d3m.primitives.data_preprocessing.polynomial_features import SKlearn as SKPolynomialFeatures
from d3m.primitives.data_preprocessing.rbf_sampler import SKlearn as SKRBFSampler
from d3m.primitives.data_preprocessing.standard_scaler import SKlearn as SKStandardScaler
from d3m.primitives.data_transformation.one_hot_encoder import SKlearn as SKOneHotEncoder
from d3m.primitives.feature_selection.select_percentile import SKlearn as SKSelectPercentile


tsf_config_dict = {

   SKFastICA: {
        'tol': np.arange(0.0, 1.01, 0.05)
    },

    SKFeatureAgglomeration: {
        'linkage': ['ward', 'complete', 'average'],
        'affinity': ['euclidean', 'l1', 'l2', 'manhattan', 'cosine', 'precomputed']
    },

    SKMinMaxScaler: {
    },

    SKNystroem: {
        'kernel': ['rbf', 'cosine', 'chi2', 'laplacian', 'polynomial', 'poly', 'linear', 'additive_chi2', 'sigmoid'],
        'gamma': np.arange(0.0, 1.01, 0.05),
        'n_components': range(1, 11)
    },


    SKPCA: {
        'svd_solver': ['randomized'],
        'iterated_power': range(1, 11)
    },

    SKPolynomialFeatures: {
        'degree': [2],
        'include_bias': [False],
        'interaction_only': [False]
    },

    SKRBFSampler: {
        'gamma': np.arange(0.0, 1.01, 0.05)
    },

    SKStandardScaler: {
    },

    #ZeroCount: {
    #},

    SKOneHotEncoder: {
        'minimum_fraction': [0.05, 0.1, 0.15, 0.2, 0.25],
        'sparse': [False],
        'handle_unknown': ['ignore']
    },

    SKSelectPercentile: {
        'percentile': range(1, 100),
        'score_func': ['f_regression']
    },

    SKExtraTreesRegressor: {
        'n_estimators': [100],
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'bootstrap': [True, False]
    },

    SKGradientBoostingRegressor: {
        'n_estimators': [100],
        'loss': ["ls", "lad", "huber", "quantile"],
        'learning_rate': [1e-3, 1e-2, 1e-1, 0.5, 1.],
        'max_depth': range(1, 11),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'subsample': np.arange(0.05, 1.01, 0.05),
        'max_features': np.arange(0.05, 1.01, 0.05),
        'alpha': [0.75, 0.8, 0.85, 0.9, 0.95, 0.99]
    },

    # SKAdaBoostRegressor: {
    #    'n_estimators': [100],
    #    'learning_rate': [1e-3, 1e-2, 1e-1, 0.5, 1.],
    #    'loss': ["linear", "square", "exponential"],
    #    'max_depth': range(1, 11)
    # },

    SKDecisionTreeRegressor: {
        'max_depth': range(1, 11),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21)
    },

    # SKKNeighborsRegressor: {
    #    'n_neighbors': range(1, 101),
    #    'weights': ["uniform", "distance"],
    #    'p': [1, 2]
    # },

    SKLinearSVR: {
        'loss': ["epsilon_insensitive", "squared_epsilon_insensitive"],
        'dual': [True, False],
        'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1],
        'C': [1e-4, 1e-3, 1e-2, 1e-1, 0.5, 1., 5., 10., 15., 20., 25.],
        'epsilon': [1e-4, 1e-3, 1e-2, 1e-1, 1.]
    },

    SKRandomForestRegressor: {
        'n_estimators': [100],
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'bootstrap': [True, False]
    },

    #    DeepAutoRegression: {
        #'epochs' : [2],
#        'learning_rate' : [0.0001, 0.001, 0.005, 0.01, 0.1],
#        'dropout_rate' : [ 0.05, 0.1, 0.2, 0.3, 0.5 ],
#        'window_size' : [ 10, 20, 50, 100, 500 ]
#    }
}

tsf_config_dict_pure = {

   SKFastICA: {
        'tol': np.arange(0.0, 1.01, 0.05)
    },

    SKFeatureAgglomeration: {
        'linkage': ['ward', 'complete', 'average'],
        'affinity': ['euclidean', 'l1', 'l2', 'manhattan', 'cosine', 'precomputed']
    },

    SKMinMaxScaler: {
    },

    SKNystroem: {
        'kernel': ['rbf', 'cosine', 'chi2', 'laplacian', 'polynomial', 'poly', 'linear', 'additive_chi2', 'sigmoid'],
        'gamma': np.arange(0.0, 1.01, 0.05),
        'n_components': range(1, 11)
    },


    SKPCA: {
        'svd_solver': ['randomized'],
        'iterated_power': range(1, 11)
    },

    SKPolynomialFeatures: {
        'degree': [2],
        'include_bias': [False],
        'interaction_only': [False]
    },

    SKRBFSampler: {
        'gamma': np.arange(0.0, 1.01, 0.05)
    },

    SKStandardScaler: {
    },

    #ZeroCount: {
    #},

    SKOneHotEncoder: {
        'minimum_fraction': [0.05, 0.1, 0.15, 0.2, 0.25],
        'sparse': [False],
        'handle_unknown': ['ignore']
    },

    SKSelectPercentile: {
        'percentile': range(1, 100),
        'score_func': ['f_regression']
    },

}
