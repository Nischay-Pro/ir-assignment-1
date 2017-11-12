from sklearn.metrics import precision_score
from scipy import stats


def spearman(a, b):
    return stats.spearmanr(a, b)


def rmse(a, b):
    mse = ((a - b)**2).mean()
    rmse = mse**0.5
    return rmse


def precision(a, b):
    return precision_score(a, b, average='weighted')