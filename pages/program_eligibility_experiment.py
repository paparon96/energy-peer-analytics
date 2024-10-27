import pandas as pd
import numpy as np

import altair as alt
import streamlit as st


st.title('Energy Efficiency Peer Analytics')

st.markdown('''
## Description
Treatment effect estimation of home energy efficiency programs based on `Regression Discontinuity Design (RDD)` methodology.
## Analysis
DUMMY
'''
)


# Import data (we use @st.cache_data to keep the dataset in cache)
@st.cache_data
def get_dummy_electricity_consumption_rdd_data():
    consumption_df = pd.read_csv('data/electricity_consumption_rdd.csv', index_col=0)
    return consumption_df

electricity_consumption_rdd_df = get_dummy_electricity_consumption_rdd_data()

# Exploratory chart to visually show the pattern 
c = alt.Chart(electricity_consumption_rdd_df).mark_circle(size=60).encode(
    x='home_size',
    y='electricity_consumption',
    #color='treatment',
    tooltip=['home_size', 'treatment', 'electricity_consumption']
).interactive()

rules = alt.Chart(pd.DataFrame({
  'home_size': 5,
  'color': ['red']
})).mark_rule().encode(
  x='home_size',
  color=alt.Color('color:N', scale=None)
)
# TO-DO: add legend to the chart!

st.subheader(f'Peer-group consumption analytics with energy efficiency support programme eligibility based on home size')
st.altair_chart(c + rules, use_container_width=True)

# Estimate treatment effect
n = len(electricity_consumption_rdd_df)
X = np.concatenate([np.ones(n).reshape(n, 1), electricity_consumption_rdd_df[['treatment', 'home_size']].values], axis=1)
y = electricity_consumption_rdd_df['electricity_consumption'].values
coefs = np.linalg.inv(X.T@X)@X.T@y
# TO-DO: Outsource treatment effect estimation to /utils

st.metric(label="Estimated treatment effect of the support programme", value=f"{round(coefs[1], 3)} unit")