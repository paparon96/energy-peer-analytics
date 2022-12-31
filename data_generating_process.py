import pandas as pd
import numpy as np


# Configure parameters
dates = pd.date_range('2022-01-01', 'today', freq='bm')
n = len(dates)
own_mean = 120
avg_mean = 100
variance = 5
pv_gain = 20
pv_gain_variance = 3

# Data generating random processes
own_c = np.random.normal(loc=own_mean, scale=variance, size=n)
avg_c = np.random.normal(loc=avg_mean, scale=variance, size=n)

solar_pv_experiment_start = int(len(dates) / 2)
solar_pv_offset = np.random.normal(loc=-pv_gain, scale=pv_gain_variance)

# Data processing
values = pd.DataFrame({'your consumption': own_c,
                       'average consumption': avg_c,}, index=dates)

print(values)

own_c_with_pv = np.random.normal(loc=avg_mean, scale=variance, size=n)
own_c_with_pv[solar_pv_experiment_start:] += solar_pv_offset
values_with_pv = pd.DataFrame({'your consumption': own_c_with_pv,
                       'average consumption': avg_c,}, index=dates)
print(values_with_pv)

# Feature importance
feature_imp = pd.DataFrame({'Importance': {'Insulation': 0.3,
                                           'Heating system': 0.6,
                                           'Efficiency of electric devices': 0.1,}})
print(feature_imp)

# Energy usage and average prices throughout a day
hourly_rates = np.concatenate((np.random.uniform(3, 5, size=8),
                               np.random.uniform(0, 1, size=8),
                               np.random.uniform(5, 10, size=8)))

hourly_consumption = np.concatenate((np.random.normal(10, 1, size=6),
                                     np.random.normal(15, 1, size=3),
                                     np.random.normal(13, 1, size=9),
                                     np.random.normal(18, 1, size=6),
                                    ))

hourly_usage_price = pd.DataFrame({'Hour': range(0, 24),
                                   'Energy usage (kWh)': hourly_consumption,
                                   'Price (EUR/kWh)': hourly_rates})

# RDD natural experiment with home eligibility
n = 500
min_c = 0
max_c = 10
cutoff_c = 5

beta = -1
gamma = 3
alpha = 1

c = np.random.uniform(min_c, max_c, n)
x = (c > cutoff_c).astype(int)
epsilon = np.random.normal(0, 1, n)
y = alpha + beta * x + gamma * c + epsilon
electricity_consumption_rdd = pd.DataFrame({'home_size': c,
                                   'treatment': x,
                                   'electricity_consumption': y})

# Export dummy data
values.to_csv('data/dummy_peer_consumption.csv')
values_with_pv.to_csv('data/dummy_peer_consumption_with_pv.csv')
feature_imp.to_csv('data/dummy_feature_importance.csv')
hourly_usage_price.to_csv('data/hourly_usage_price.csv')
electricity_consumption_rdd.to_csv('data/electricity_consumption_rdd.csv')

