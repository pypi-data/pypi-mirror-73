import numpy as np
from ..statistics import statistics
import warnings
from tabulate import tabulate


class PairedTests():
    def __init__(self, evaluator):
        self.evaluator = evaluator

    def process(self, test_name, alpha=.05, m_fmt="%.3f", std_fmt=None,
                nc="---", db_fmt="%s", tablefmt="plain", **kwargs):
        try:
            test, tkwargs = statistics.IMPLEMENTED_TESTS[test_name]
            # Remove kwarg missmatches and update tkwargs
            missmatches = list(set(kwargs.keys()).difference(tkwargs.keys()))
            if len(missmatches) > 0:
                WARN_MESSAGE = '%s parameter(s) of %s are not supported and will be ignored' % (
                    ", ".join(missmatches), test_name)
                warnings.warn(WARN_MESSAGE)
                for key in missmatches:
                    del kwargs[key]
            tkwargs.update(kwargs)

            try:
                # Gather data
                scores = self.evaluator.scores
                mean_scores = self.evaluator.mean_scores
                stds = self.evaluator.stds
                metrics = list(self.evaluator.metrics.keys())
                clfs = list(self.evaluator.clfs.keys())
                datasets = list(self.evaluator.datasets.keys())
                n_clfs = len(clfs)

                # Perform tests
                tables = {}
                for m_idx, m_name in enumerate(metrics):
                    # Prepare storage for table
                    t = []

                    for db_idx, db_name in enumerate(datasets):
                        # Row with mean scores
                        t.append([db_fmt % db_name] + [m_fmt %
                                                       v for v in
                                                       mean_scores[db_idx, :,
                                                                   m_idx]])

                        # Row with std
                        if std_fmt:
                            t.append([''] + [std_fmt %
                                             v for v in
                                             stds[db_idx, :, m_idx]])
                        # Calculate T and p
                        T, p = np.array(
                            [[test(scores[db_idx, i, :, m_idx],
                                   scores[db_idx, j, :, m_idx],
                                   **tkwargs)
                              for i in range(n_clfs)]
                             for j in range(n_clfs)]
                        ).swapaxes(0, 2)
                        _ = np.where((p < alpha) * (T > 0))
                        conclusions = [list(1 + _[1][_[0] == i])
                                       for i in range(n_clfs)]

                        # Row with conclusions
                        t.append([''] + [", ".join(["%i" % i for i in c])
                                         if len(c) > 0 else nc
                                         for c in conclusions])

                    # Store formatted table
                    tables.update({m_name: tabulate(
                        t, headers=['DATASET'] + clfs, tablefmt=tablefmt)})

                return tables
            except AttributeError:
                WARN_MESSAGE = "Call evaluator's score method first."
                raise Exception(WARN_MESSAGE)
        except KeyError:
            WARN_MESSAGE = '%s is not a supported test. Use one of: %s.' % (
                test_name, ", ".join(list(statistics.IMPLEMENTED_TESTS.keys()))
            )
            warnings.warn(WARN_MESSAGE)
