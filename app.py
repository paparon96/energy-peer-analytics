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


consumption_df = get_dummy_peer_consumption_data()
feature_imp_df = get_dummy_feature_importance_data()


# Consumption chart
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
#
# feature_imp_df_melted = pd.melt(consumption_df,
#                     id_vars=['Type'],
#                     var_name='Value',
#                     value_name='Monthly electricity consumption (kWh)')

f_imp = alt.Chart(feature_imp_df).mark_bar().encode(
    x='Importance:Q',
    y="Type:O"
).properties(height=700)
st.subheader(f'Importance of different factors for energy usage')
st.altair_chart(f_imp, use_container_width=True)
