import pandas as pd
import numpy as np


# Configure parameters
dates = pd.date_range('2022-01-01', 'today', freq='bm')
n = len(dates)

# Data generating random processes
own_c = np.random.normal(loc=100, scale=5, size=n)
avg_c = np.random.normal(loc=100, scale=5, size=n)

# Data processing
values = pd.DataFrame({'your consumption': own_c,
                       'average consumption': avg_c,}, index=dates)

print(values)

# Export dummy data
values.to_csv('data/dummy_peer_consumption.csv')
