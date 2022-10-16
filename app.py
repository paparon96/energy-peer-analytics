import pandas as pd

import altair as alt
import streamlit as st


st.title('Energy Efficiency Peer Analytics')


# Import data (we use @st.experimental_memo to keep the dataset in cache)
@st.experimental_memo
def get_data():
    consumption_df = pd.read_csv('data/dummy_peer_consumption.csv', index_col=0)
    return consumption_df

consumption_df = get_data()


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
