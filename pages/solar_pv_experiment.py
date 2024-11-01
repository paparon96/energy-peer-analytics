import datetime

import pandas as pd

import matplotlib.pyplot as plt
import altair as alt
import streamlit as st

from utils import diff_in_diff_regr


st.title('Energy Efficiency Peer Analytics')

st.markdown('''
## Description
On this page you can test how installing photovoltaic solar panels on your house affected your net electricity consumption.
This enables you to calculate the realized return on this investment and compare your house to similar households.
## Methodology
The impact of solar panel installation on electricity usage is estimated with the difference-in-differences method
([see here](https://dimewiki.worldbank.org/Difference-in-Differences#) for additional details regarding the method),
where your home's electricity usage trend is compared to the trend of your peer group. A confidence interval is also provided
for the estimated effect at the required significance level.
\n
The same general methodology could be applied to any household action (e.g. insulation, usage pattern changes etc.) to investigate its impact on energy consumption.
## Analysis
'''
)


# Import data (we use @st.cache_data to keep the dataset in cache)
@st.cache_data
def get_dummy_peer_consumption_with_pv_data():
    consumption_df = pd.read_csv('data/dummy_peer_consumption_with_pv.csv', index_col=0)
    return consumption_df

consumption_with_pv_df = get_dummy_peer_consumption_with_pv_data()

# Experiment start date selector
experiment_start_date = st.date_input(
    "Solar PV installation date",
    datetime.date(2022, 5, 31))

# Net consumption with PV experiment chart (DinD model)
consumption_with_pv_df['Date'] = consumption_with_pv_df.index

df_with_pv_melted = pd.melt(consumption_with_pv_df,
                    id_vars=['Date'],
                    var_name='Value',
                    value_name='Net monthly electricity consumption (kWh)')
c = alt.Chart(df_with_pv_melted).mark_line(point={
      "filled": False,
      "fill": "white"
    }).encode(
x='monthdate(Date)', y='Net monthly electricity consumption (kWh)', color='Value').interactive()

rules = alt.Chart(pd.DataFrame({
  'Date': [experiment_start_date.strftime("%Y-%m-%d")],
  'color': ['red']
})).mark_rule().encode(
  x='monthdate(Date):T',
  color=alt.Color('color:N', scale=None)
)

st.subheader(f'Peer-group consumption analytics with solar PV installation in 2022')
st.altair_chart(c + rules, use_container_width=True)

# Output (Causal effect estimate)
confidence_level = st.number_input('Required confidence level for estimate: (in %)?', value=95, min_value=0, max_value=100)

model = diff_in_diff_regr(consumption_with_pv_df.drop(columns=['Date']), experiment_start_date)
est = model.params['treatment']
ci = model.conf_int(alpha=1 - confidence_level/100).loc['treatment']
errors = [[est - ci[0]], [ci[1] - est]]

plt.bar([0], est, yerr=errors, color=['lightgreen'])

plt.ylabel('kWh')
plt.title('Estimated monthly effect of \n PV installation on electricity consumption')
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
st.pyplot(plt)
