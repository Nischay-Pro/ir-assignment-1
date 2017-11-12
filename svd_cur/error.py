from sklearn.metrics import precision_score
from scipy import stats


def rmse(a, b):
    mse = ((a - b)**2).mean()
    rmse = mse**0.5
    return rmse



