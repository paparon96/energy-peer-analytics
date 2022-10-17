import pandas as pd
import numpy as np


# Configure parameters
dates = pd.date_range('2022-01-01', 'today', freq='bm')
n = len(dates)

# Data generating random processes
own_c = np.random.normal(loc=100, scale=5, size=n)
avg_c = np.random.normal(loc=100, scale=5, size=n)

solar_pv_experiment_start = int(len(dates) / 2)
solar_pv_offset = np.random.normal(loc=-20, scale=3)

# Data processing
values = pd.DataFrame({'your consumption': own_c,
                       'average consumption': avg_c,}, index=dates)

print(values)

own_c_with_pv = own_c.copy()
own_c_with_pv[solar_pv_experiment_start:] += solar_pv_offset
values_with_pv = pd.DataFrame({'your consumption': own_c_with_pv,
                       'average consumption': avg_c,}, index=dates)
print(values_with_pv)

# Feature importance
feature_imp = pd.DataFrame({'Importance': {'Insulation': 0.5,
'Heating system': 0.3}})
print(feature_imp)

# Export dummy data
values.to_csv('data/dummy_peer_consumption.csv')
values_with_pv.to_csv('data/dummy_peer_consumption_with_pv.csv')
feature_imp.to_csv('data/dummy_feature_importance.csv')
