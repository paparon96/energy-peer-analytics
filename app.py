import pandas as pd

import altair as alt
import streamlit as st


st.title('Energy Efficiency Peer Analytics')


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

# Data inputs for the analysed property
st.markdown(
"""
# Data input
In this section please provide the relevant parameters of your property that you would like to compare and analyse.
"""
)
size = st.number_input('How large is your property (in m2)?', value=70, min_value=0, max_value=500)

heating_type = st.selectbox(
    'What kind of heating system does your property have',
    ('Gas', 'Oil', 'Electricity'))

# Consumption chart
st.markdown(
"""
# Analysis
In this section you can see the analysis and comparisons regarding your property's energy consumption.
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
feature_imp_df['Type'] = feature_imp_df.index

f_imp = alt.Chart(feature_imp_df).mark_bar().encode(
    x='Importance:Q',
    y="Type:O"
).properties(height=700)
st.subheader(f'Importance of different factors for energy usage')
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
st.altair_chart(energy_by_dev, use_container_width=True)

# Energy usage and prices throughout the day (for behavioral load shifting)
fig_hourly_usage_price = alt.Chart(hourly_usage_price).mark_bar().encode(
    x='Hour:O',
    y='Energy usage (kWh):Q',
    color='Price (EUR/kWh):Q',
)

st.subheader(f'Energy usage throughout a typical day')
st.altair_chart(fig_hourly_usage_price, use_container_width=True)

st.subheader(f'Energy saving recommendations with savings potential')
col1, col2 = st.columns(2)
col1.metric(label="Charge your EV in the morning", value="50 EUR/month", delta="-0 EUR investment cost")
col2.metric(label="Better insulation for the windows", value="30 EUR/month", delta="-100 EUR investment cost")
