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

VERBOSE_COLUMNS = 80


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
        self.m, self.k, self.random_state = self.protocol

        skf = RepeatedStratifiedKFold(n_splits=self.k, n_repeats=self.m,
                                      random_state=self.random_state)
        self.predictions = np.zeros([len(self.datasets), len(self.clfs),
                                     self.m * self.k], dtype=object)
        self.true_values = np.zeros([len(self.datasets), self.m * self.k],
                                    dtype=object)

        # Iterate over datasets
        for dataset_id, dataset_name in enumerate(tqdm(self.datasets,
                                                       desc="DTS",
                                                       ascii=True,
                                                       disable=not verbose)):
            X, y = self.datasets[dataset_name]
            for fold_id, (train, test) in enumerate(skf.split(X, y)):
                self.true_values[dataset_id, fold_id] = y[test]
                for clf_id, clf_name in enumerate(self.clfs):
                    clf = clone(self.clfs[clf_name])
                    clf.fit(X[train], y[train])
                    y_pred = clf.predict(X[test])
                    self.predictions[dataset_id, clf_id, fold_id] = y_pred

        return self

    def score(self, metrics, verbose=False, return_flatten=True):
        """
        description

        Input arguments description:
        metrics: dictonary that contains metrics names and functions
                 ["name"] : function
        """
        self.metrics = metrics

        # Prepare storage for scores
        # DB x CLF x FOLD x METRIC
        self.scores = np.array([[[[
            metrics[m_name](
                self.predictions[db_idx, clf_idx, f_idx],
                self.true_values[db_idx, f_idx])
            for m_name in self.metrics]
            for f_idx in range(self.m * self.k)]
            for clf_idx, clf in enumerate(self.clfs)]
            for db_idx, db_name in enumerate(self.datasets)])

        # Store mean scores and stds
        # DB x CLF x METRIC
        self.mean_scores = np.mean(self.scores, axis=2)
        self.stds = np.std(self.scores, axis=2)

        # Verbose mode
        if verbose:
            lmn = len(max(list(self.metrics.keys()), key=len))
            lmc = (VERBOSE_COLUMNS-lmn)//2
            for m, metric in enumerate(self.metrics):
                print(lmc*"#", metric.center(lmn), lmc*"#")

                scores_ = self.mean_scores[:, :, m]

                # ranks
                ranks = []
                for row in scores_:
                    ranks.append(rankdata(row).tolist())
                ranks = np.array(ranks)
                mean_ranks = np.mean(ranks, axis=0)

                names_column = np.array(list(self.datasets.keys())).reshape(
                    len(self.datasets), -1)
                scores_table = np.concatenate((names_column, scores_), axis=1)
                print(tabulate(scores_table, headers=self.clfs.keys(),
                               floatfmt=".3f"))

                print(lmc*"-", "Mean ranks".center(lmn), lmc*"-")
                print(tabulate(mean_ranks[np.newaxis, :],
                               headers=self.clfs.keys(), floatfmt=".3f"))

        # Give output
        return {
            True: (self.mean_scores, self.stds),
            False: self.scores,
        }[return_flatten]
