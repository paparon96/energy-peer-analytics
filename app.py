import pandas as pd

import altair as alt
import streamlit as st


st.title('Energy Efficiency Peer Analytics')
st.markdown(
"""
This is an interactive app that provides energy efficiency insights to household consumers.
\n
You can follow the sections below to get transparent peer analytics (comparison to similar households)
through charts and dashboards regarding your energy usage and savings potential. By acting upon these data-driven insights,
you can reduce energy consumption at home and realize financial savings as well.
"""
)


# Import data (we use @st.experimental_memo to keep the dataset in cache)
@st.experimental_memo
def get_dummy_peer_consumption_data():
    consumption_df = pd.read_csv('data/dummy_peer_consumption.csv', index_col=0)
    return consumption_df

@st.experimental_memo
def get_dummy_feature_importance_data():
    feature_imp_df = pd.read_csv('data/dummy_feature_importance.csv', index_col=0)
    return feature_imp_df

@st.experimental_memo
def get_dummy_hourly_usage_price_data():
    hourly_usage_price = pd.read_csv('data/hourly_usage_price.csv', index_col=0)
    return hourly_usage_price


consumption_df = get_dummy_peer_consumption_data()
feature_imp_df = get_dummy_feature_importance_data()
hourly_usage_price = get_dummy_hourly_usage_price_data()

# Data inputs for the analysed home
st.markdown(
"""
# Data input
In this section please provide the relevant parameters of your home that you would like to compare and analyse.
"""
)
size = st.number_input('How large is your home (in m2)?', value=70, min_value=0, max_value=500)

year_built = st.number_input('In which year was your home built?', value=1980, min_value=1900, max_value=pd.to_datetime('today').year)

heating_type = st.selectbox(
    'What kind of heating system does your home have?',
    ('Gas', 'Oil', 'Electricity'))

# Consumption chart
st.markdown(
"""
# Analysis
In this section you can see the comparison of your home's energy consumption to that of similar households'.
"""
)
consumption_df['Date'] = consumption_df.index

df_melted = pd.melt(consumption_df,
                    id_vars=['Date'],
                    var_name='Value',
                    value_name='Monthly electricity consumption (kWh)')
c = alt.Chart(df_melted).mark_line(point={
      "filled": False,
      "fill": "white"
    }).encode(
x='Date', y='Monthly electricity consumption (kWh)', color='Value').interactive()

st.subheader(f'Peer-group consumption analytics in 2022')
st.altair_chart(c, use_container_width=True)

# Feature importance
feature_imp_df['Factor'] = feature_imp_df.index

f_imp = alt.Chart(feature_imp_df).mark_bar().encode(
    x='Importance:Q',
    y="Factor:O"
).properties(height=200)
st.subheader(f'Importance of different factors for energy usage')
st.markdown(
"""
In this section you can investigate which factors explain the difference in your home's energy consumption
compared to similar households. This could highlight potential improvement areas to increase energy efficiency.
\n
The importance of different factors is estimated using the
[Shapley values](https://christophm.github.io/interpretable-ml-book/shapley.html) methodology.
"""
)
st.altair_chart(f_imp, use_container_width=True)

# Energy usage by devices
energy_usage_by_devices = pd.DataFrame({"device": ['Oven', 'Washing machine', 'Dryer'],
                                        "value": [4, 6, 6]})

energy_by_dev = alt.Chart(energy_usage_by_devices).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(field="device", type="nominal"),
    tooltip=['device:N','value:Q']
)
st.subheader(f'Electricity usage distribution among household devices')
st.markdown(
"""
In this section you can analyse how much electricity is consumed by your different electric devices
(note that this section assumes that you have a smart home and/or IoT devices such that the required data can be collected).
"""
)
st.altair_chart(energy_by_dev, use_container_width=True)

# Energy usage and prices throughout the day (for behavioral load shifting)
fig_hourly_usage_price = alt.Chart(hourly_usage_price).mark_bar().encode(
    x='Hour:O',
    y='Energy usage (kWh):Q',
    color='Price (EUR/kWh):Q',
)

st.subheader(f'Energy usage throughout a typical day')
st.markdown(
"""
In this section you can monitor how your average energy usage varies during a day and how it correlates with the energy price
throughout a day. This could help to highlight potential changes in your consumption pattern that could reduce your
energy bills.
"""
)
st.altair_chart(fig_hourly_usage_price, use_container_width=True)

st.subheader(f'Energy efficiency recommendations with financial savings potential')
st.markdown(
"""
In this section you receive personalized recommendations based on your energy usage data. These suggestions have the highest
expected financial impact for your household. You can see both the expected benefits/savings, as well as the required investments
below.
"""
)
col1, col2 = st.columns(2)
col1.metric(label="Charge your EV in the morning", value="50 EUR/month", delta="-0 EUR investment cost")
col2.metric(label="Better insulation for the windows", value="30 EUR/month", delta="-100 EUR investment cost")
