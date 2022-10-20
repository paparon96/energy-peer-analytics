"""Utilities module"""
import pandas as pd
import datetime

import statsmodels
from statsmodels.formula.api import ols

def diff_in_diff_regr(df: pd.DataFrame, date: datetime.date) -> statsmodels.regression.linear_model.RegressionResultsWrapper:
    """Treatment effect estimation.

    Estimate causal treatment effect with difference-in-differences methodology.

    Args:
        df: pandas DataFrame with the observations
        date: treatment date

    Returns:
        Estimated OLS model

    """

    df.index = pd.DatetimeIndex(df.index)
    df = pd.melt(df, ignore_index=False, var_name='type')
    df['post_treatment_period'] = (df.index.date > date).astype(int)
    df['type'] = (df['type']=='your consumption').astype(int)
    df['treatment'] = ((df['post_treatment_period']==1) &
                               (df['type']==1)).astype(int)

    model = ols('value ~ type + post_treatment_period + treatment', data=df).fit(cov_type='HC1',)

    return model