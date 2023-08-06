import numpy as np
    

def _log_transform(y):
    return y.apply(np.log)


def _exp_transform(y):
    return y.apply(np.exp)