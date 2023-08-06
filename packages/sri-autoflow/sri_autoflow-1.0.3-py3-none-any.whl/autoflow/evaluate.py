import sys
import sklearn.metrics as metrics
import numpy as np
import logging
import math

class MetricDataException(Exception):
    pass

class MetricCalculator(object):

    _logger = logging.getLogger(__name__)

    def __init__(self, prediction_file, target_file):
        # Make this work for the ta2/ta3 use case
        # self.predictions = prediction_file.tolist()
        self.predictions = prediction_file
        self.targets = target_file
        self.isNumbers = True

        if len(self.predictions) != len(self.targets):
            raise MetricDataException()

    def _sklearn_inputs(self):
        actuals = []
        predictions = []
        for key in self.targets:
            actual = self.targets[key]
            predicted = self.predictions[key]
            if self.is_number(actual) and self.is_number(predicted) and self.isNumbers == True:
                self.isNumbers = True
            else:
                self.isNumbers = False
            actuals.append(actual)
            predictions.append(predicted)
        return (actuals, predictions)

    def accuracy(self):
        act, pred = self._sklearn_inputs()
        return metrics.accuracy_score(act, pred)

    def mean_squared_error(self):
        act, pred = self._sklearn_inputs()
        if self.isNumbers:
            return metrics.mean_squared_error([float(i) for i in act], [float(i) for i in pred])
        else:
            return 0

    def root_mean_squared_error(self):
        mse = self.mean_squared_error()
        return math.sqrt(mse)

    def r_squared(self):
        act, pred = self._sklearn_inputs()
        if self.isNumbers:
            return metrics.r2_score([float(i) for i in act], [float(i) for i in pred])
        else:
            return 0

    def f1(self):
        act, pred = self._sklearn_inputs()
        if self.isNumbers:
            return metrics.f1_score([float(i) for i in act], [float(i) for i in pred])
        else:
            return 0

    def f1_macro(self):
        act, pred = self._sklearn_inputs()

        from sklearn.metrics import f1_score, precision_recall_fscore_support

        p_macro, r_macro, f_macro, support_macro = precision_recall_fscore_support(y_true=act, y_pred=pred, average='macro')

        return f_macro

    def mean_absolute_error(self):
        act, pred = self._sklearn_inputs()
        if self.isNumbers:
            return metrics.mean_absolute_error([float(i) for i in act], [float(i) for i in pred])
        else:
            return 0

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

'''
Main entry point for the SRI TA2 pipeline evaluator
'''
def main(argv):
    print("Comparing Test run results to Targets")

    # Grab the prediction file
    predictionFile = sys.argv[1]
    # Grab the target file
    targetFile = sys.argv[2]
    # evaluation type
    metric = sys.argv[3]

    predictions = _load_file(predictionFile)
    targets = _load_file(targetFile)

    mc = MetricCalculator(predictions, targets)

    if metric == 'accuracy':
        accuracy = mc.accuracy()
        print("Accuracy: %f" % accuracy)
    elif metric == 'mean_squared_error':
        mse = mc.mean_squared_error()
        print("MSE: " + str(mse))
    elif metric == 'root_mean_squared_error':
        rmse = mc.root_mean_squared_error()
        print("RootMSE: " + str(rmse))
    elif metric == 'r_squared':
        r_squared = mc.r_squared()
        print("R2: " + str(r_squared))
    elif metric == 'f1Macro':
        f1_macro = mc.f1_macro()
        print("F1Macro: " + str(f1_macro))
    elif metric == 'f1':
        f1 = mc.f1()
        print("F1: " + str(f1))
    elif metric == 'mean_absolute_error':
        mean_absolute_error = mc.mean_absolute_error()
        print("MeanAbsoluteError: " + str(mean_absolute_error))
    else:
        print("Metric not supported: " + metric)



def _load_file(fname):
    result = {}
    with open(fname, "r") as myfile:
        firstLine = True
        for line in myfile.readlines():
            if firstLine:
                firstLine = False
            else:
                index, value = line.split(",")
                if isinstance(value, float):
                    result[index] = float(value)
                else:
                    result[index] = value
    return result


'''
Entry point - required to make python happy
'''
if __name__ == "__main__":
    main(sys.argv)
