"""
Class description

Date:
Authors:
"""

# imports
import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.base import clone
from tabulate import tabulate
from tqdm import tqdm
from scipy.stats import rankdata

class Evaluator():
    def __init__(self, datasets, protocol=(1, 5, None)):
        self.datasets = datasets
        self.protocol = protocol

    def process(self, clfs, verbose=False):
        """
        This function is used to process declared evaluation protocol
        through all given datasets and classifiers.
        It results with stored predictions and corresponding labels.

        Input atguments description:
        clfs: dictonary that contains estimators names and objects
              ["name"] : obj
        """
        self.clfs = clfs

        # Establish protocol
        m, k, random_state = self.protocol

        skf = RepeatedStratifiedKFold(n_splits=k, n_repeats=m,
                                      random_state=random_state)
        self.predictions = np.zeros([len(self.datasets), len(self.clfs),
                                     m*k], dtype=object)
        self.true_values = np.zeros([len(self.datasets), m*k], dtype=object)

        for dataset_id, dataset_name in enumerate(tqdm(self.datasets, desc="DTS", ascii=True, disable=not verbose)):
            X, y = self.datasets[dataset_name]
            for fold_id, (train, test) in enumerate(tqdm(skf.split(X, y), desc="FLD", ascii=True, disable=not verbose)):
                self.true_values[dataset_id, fold_id] = y[test]
                for clf_id, clf_name in enumerate(self.clfs):
                    clf = clone(self.clfs[clf_name])
                    clf.fit(X[train], y[train])
                    y_pred = clf.predict(X[test])
                    self.predictions[dataset_id, clf_id, fold_id] = y_pred

        return self

    def score(self, metrics, return_std=False, verbose=False):
        """
        description

        Input arguments description:
        metrics: dictonary that contains metrics names and functions
                 ["name"] : function
        """
        self.metrics = metrics
        _ = (len(self.datasets), len(self.clfs), len(metrics))
        # Flatten or not...
        if return_std:
            self.stds = np.zeros(_)

        self.scores = np.zeros(_)
        m, k, random_state = self.protocol
        for dataset_id, dataset_name in enumerate(self.datasets):
            for clf_id, clf_name in enumerate(self.clfs):
                for metric_id, metric_name in enumerate(self.metrics):
                    partial_scores = np.zeros([m*k])
                    for i in range(m*k):
                        y_test = self.true_values[dataset_id, i]
                        y_pred = self.predictions[dataset_id, clf_id, i]
                        partial_scores[i] = self.metrics[metric_name](y_test, y_pred)
                    self.scores[dataset_id, clf_id, metric_id] = np.mean(partial_scores)
                    if return_std:
                        self.stds[dataset_id, clf_id, metric_id] = np.std(partial_scores)

        if verbose:
            for m, metric in enumerate(self.metrics):
                print("################ ", metric, " ################")
                scores_ = self.scores[:,:,m]

                # ranks
                ranks = []
                for row in scores_:
                    ranks.append(rankdata(row).tolist())
                ranks = np.array(ranks)
                mean_ranks = np.mean(ranks, axis=0)

                names_column = np.array(list(self.datasets.keys())).reshape(len(self.datasets), -1)
                scores_table = np.concatenate((names_column, scores_), axis=1)
                print(tabulate(scores_table, headers=self.clfs.keys(), floatfmt=".3f"), scores_table.shape)

                print("################ Mean ranks ################")
                print(tabulate(mean_ranks[np.newaxis,:], headers=self.clfs.keys(), floatfmt=".3f" ))

        if return_std:
            return self.scores, self.stds
        else:
            return self.scores
