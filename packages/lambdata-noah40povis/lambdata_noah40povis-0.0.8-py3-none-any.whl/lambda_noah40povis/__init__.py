#!/usr/bin/env python
"""
lambdata - a collection of Data Science helper functions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

TEST = pd.DataFrame(np.ones(10))


def null_info(x):
    a = x.isnull().sum()
    return print(a)

def split_data(x, y):
    X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.33, random_state=42)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    return X_train, X_test, y_train, y_test

z = 2