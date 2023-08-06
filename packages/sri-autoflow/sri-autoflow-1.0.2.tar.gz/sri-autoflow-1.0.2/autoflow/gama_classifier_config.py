import numpy as np

from d3m.primitives.classification.gaussian_naive_bayes import SKlearn as SKGaussianNB
from d3m.primitives.classification.bernoulli_naive_bayes import SKlearn as SKBernoulliNB
from d3m.primitives.classification.multinomial_naive_bayes import SKlearn as SKMultinomialNB
from d3m.primitives.classification.decision_tree import SKlearn as SKDecisionTreeClassifier
from d3m.primitives.classification.extra_trees import SKlearn as SKExtraTreesClassifier
from d3m.primitives.classification.random_forest import SKlearn as SKRandomForestClassifier
from d3m.primitives.classification.gradient_boosting import SKlearn as SKGradientBoostingClassifier
from d3m.primitives.classification.svc import SKlearn as SKSVC
from d3m.primitives.classification.logistic_regression import SKlearn as SKLogisticRegression
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
# from d3m.primitives.feature_selection.joint_mutual_information import AutoRPI as RPIFeatureSelector


#from d3m.primitives.sri.tpot import ZeroCount
# Check the TPOT documentation for information on the structure of config dicts

classifier_config_dict = {

    # Classifiers
    SKRandomForestClassifier: {
        'n_estimators': [100],
        'criterion': ["gini", "entropy"],
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'bootstrap': [True, False]
    },

    # Classifiers
    SKSVC: {
        'C': [2 ** i for i in range(-5, 6)],
        'kernel': [
            'rbf', 
#            'poly', 
            'sigmoid'],
        'degree': range(1, 6),
        'gamma': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10],
        'coef0': np.arange(-1, 1.01, 0.2),
        'shrinking': [True, False],
        'tol': [1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    },

    SKGradientBoostingClassifier: {
        'n_estimators': [100],
        'criterion': ["friedman_mse", "mae", "mse"],
        'min_weight_fraction_leaf': [0.],
        'min_impurity_decrease': [0.],
        'learning_rate': [1e-3, 1e-2, 1e-1, 0.5, 1.],
        'max_depth': range(1, 11),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'subsample': np.arange(0.05, 1.01, 0.05),
        'max_features': np.arange(0.05, 1.01, 0.05)
    },

    SKGaussianNB: {
    },

    SKBernoulliNB: {
        'alpha': [1e-3, 1e-2, 1e-1, 1., 10., 100.],
        'fit_prior': [True, False]
    },

    SKMultinomialNB: {
        'alpha': [1e-3, 1e-2, 1e-1, 1., 10., 100.],
        'fit_prior': [True, False]
    },

    SKDecisionTreeClassifier: {
        'criterion': ["gini", "entropy"],
        'max_depth': range(1, 11),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21)
    },

    SKExtraTreesClassifier: {
        'n_estimators': [100],
        'criterion': ["gini", "entropy"],
        'max_features': np.arange(0.05, 1.01, 0.05),
        'min_samples_split': range(2, 21),
        'min_samples_leaf': range(1, 21),
        'bootstrap': [True, False]
    },

    #SKKNeighborsClassifier: {
    #    'n_neighbors': range(1, 101),
    #    'weights': ["uniform", "distance"],
    #    'p': [1, 2]
    #},

#    Disabled for testing.  Too slow for debugging!
#    SKLogisticRegression: {
#        'penalty': ["l1", "l2"],
#        'C': [1e-4, 1e-3, 1e-2, 1e-1, 0.5, 1., 5., 10., 15., 20., 25.],
#        'dual': [True, False]
#    },

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

#    SKPCA: {
#        'svd_solver': ['randomized'],
#        'iterated_power': range(1, 11)
#    },

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
        'score_func': ['f_classif']
    },

#    RPIFeatureSelector: {
#        'nbins': range(2, 21),
#        'method': ['counting', 'pseudoBayesian', 'fullBayesian'],
#        'strategy': ['uniform', 'quantile']
#    }

}
