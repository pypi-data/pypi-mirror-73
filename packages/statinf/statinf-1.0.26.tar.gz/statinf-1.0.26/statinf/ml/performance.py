import warnings
import pandas as pd
import numpy as np


class BinaryPerformance:
    def __init__(self, y_true, y_pred):
        """Gives detailed perfomance metrics for binary calssification models.

        :param y_true: Array of true targets.
        :type y_true: :obj:`numpy.array`
        :param y_pred: Array of predicted targets.
        :type y_pred: :obj:`numpy.array`
        """
        warnings.filterwarnings('ignore')
        # Format y_true
        if type(y_true) in [pd.Series, pd.DataFrame]:
            true = list(y_true.values)
        elif type(y_true) == list:
            true = y_true
        elif type(y_true) == np.ndarray:
            if y_true.shape == (len(y_true), 1):
                true = [x[0] for x in np.asarray(y_true)]
            elif y_true.shape == (len(y_true),):
                true = list(y_true)
            else:
                raise TypeError('Cannot properly read shape for y_true.')
        else:
            raise TypeError('Type for y_true is not valid.')
        # Format y_pred
        if type(y_pred) in [pd.Series, pd.DataFrame]:
            pred = list(y_pred.values)
        elif type(y_pred) == list:
            pred = y_pred
        elif type(y_pred) == np.ndarray:
            if y_pred.shape == (len(y_pred), 1):
                pred = [x[0] for x in np.asarray(y_pred)]
            elif y_pred.shape == (len(y_pred),):
                pred = list(y_pred)
            else:
                raise TypeError('Cannot properly read shape for y_pred.')
        else:
            raise TypeError('Type for y_pred is not valid.')

        # Put data to a DF
        for_conf = pd.DataFrame({'true': true,
            'pred': pred,
            'perf': ''})

        # Compute True and False positives/negatives
        for_conf['perf'][(for_conf.true == 1) & (for_conf.pred == 1)] = 'true_positive'
        for_conf['perf'][(for_conf.true == 0) & (for_conf.pred == 0)] = 'true_negative'
        for_conf['perf'][(for_conf.true == 1) & (for_conf.pred == 0)] = 'false_negative'
        for_conf['perf'][(for_conf.true == 0) & (for_conf.pred == 1)] = 'false_positive'
        # Number of True and False positives/negatives
        self.tp = len(for_conf[(for_conf.perf == 'true_positive')])
        self.tn = len(for_conf[(for_conf.perf == 'true_negative')])
        self.fn = len(for_conf[(for_conf.perf == 'false_negative')])
        self.fp = len(for_conf[(for_conf.perf == 'false_positive')])
        self.m = len(y_pred)
        # Confusion matrix
        self.conf = pd.DataFrame({'True 0': [0., 0.], 'True 1': [0., 0.]}, index=['Predicted 0', 'Predicted 1'])
        # Fill confusion matrix
        self.conf['True 0']['Predicted 0'] = self.tn/self.m
        self.conf['True 0']['Predicted 1'] = self.fp/self.m
        self.conf['True 1']['Predicted 0'] = self.fn/self.m
        self.conf['True 1']['Predicted 1'] = self.tp/self.m
        warnings.filterwarnings('default')

    def accuracy(self):
        """Binary accuracy of the model. Percentage of equal values between :obj:`y_true` and :obj:`y_pred`.

        :formula: .. math:: accuracy = \\dfrac{TP + TN}{n}

        :return: Accuracy
        :rtype: :obj:`float`
        """
        return((self.tp + self.tn)/self.m)

    def confusion(self):
        """Confusion matrix

        :return: Confusion matrix

            +-----------------+------------+------------+
            |                 | **True 0** | **True 0** |
            +=================+============+============+
            | **Predicted 0** | :math:`TN` | :math:`TN` |
            +-----------------+------------+------------+
            | **Predicted 1** | :math:`FP` | :math:`TP` |
            +-----------------+------------+------------+

        :rtype: :obj:`pandas.DataFrame`
        """
        return(self.conf * 100)

    def precision(self):
        """Precision metric, proportion of actual 1 values amongst the ones predicted.

        :formula: .. math:: precision = \\dfrac{TP}{TP + FP}

        :return: Precision
        :rtype: :obj:`float`
        """
        return(self.tp / (self.tp + self.fp))

    def recall(self):
        """  Recall metric, proportion of values we predicted as one from the actuals ones.

        :formula: .. math:: recall = \\dfrac{TP}{TP + FN}

        :return: Recall
        :rtype: :obj:`float`
        """
        return(self.tp / (self.tp + self.fn))

    def F1_score(self):
        """F1-score

        :formula: .. math:: F_{1} = 2 \\cdot \\dfrac{precision \\times recall}{precision + recall}

        :return: F1-score
        :rtype: :obj:`float`
        """
        return(2 * (self.precision() * self.recall()) / (self.precision() + self.recall()))
