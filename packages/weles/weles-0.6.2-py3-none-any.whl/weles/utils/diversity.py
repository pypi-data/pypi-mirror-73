import numpy as np

def entropy_measure_e(ensemble, X, y):
    L = len(ensemble)
    return np.mean(
        (
            L // 2
            - np.abs(
                np.sum(
                    y[np.newaxis, :] == np.array([clf.predict(X) for clf in ensemble]),
                    axis=0,
                )
                - L // 2
            )
        )
        / (L / 2)
    )
