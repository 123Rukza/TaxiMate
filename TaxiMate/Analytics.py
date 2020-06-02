# Analytics and verification module
# Imports
import numpy as np


class Analytics:

    # Calculating MAPE score for future analytics
    @staticmethod
    def mape(a, f):
        return 1 / len(a) * np.sum(2 * np.abs(f - a) / (np.abs(a) + np.abs(f)))

    # Calculating SMAPE score for future analytics
    @staticmethod
    def smape(a, f):
        return 100 / len(a) * np.sum(2 * np.abs(f - a) / (np.abs(a) + np.abs(f)))
