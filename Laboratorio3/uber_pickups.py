from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import time
import math 


st.title("Uber pickups test")

DATA_SOURCE = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"

@st.cache(allow_output_mutation=True)
def dowload_data(nrows):
    return (pd.read_csv(DATA_SOURCE, nrows=nrows).rename(columns={'Lat':'lat','Lon':'lon'}))

df = dowload_data(100000)

df['time'] = pd.to_datetime(df['Date/Time'])
df['hour'] = df['time'].dt.hour

values = st.sidebar.slider('Hour range', df.hour.min(), df.hour.max(), (6, 9))


dfMap = df.loc[((df['hour'] >=values[0]) & (df['hour']<=values[1]))]
dfPickups = df.loc[((df['hour'] >=values[0]) & (df['hour']<=values[1])), ['hour','time']]

page_size = 1000    
total_pages = math.ceil(len(dfMap) / page_size)
starting_value = 0
slider = st.slider('Seleccione la página',1, total_pages)

st.write('page selected', slider, 'with limits', (((slider-1)*page_size),(slider*page_size)-1))
dfMap = dfMap.loc[((slider-1)*page_size):(slider*page_size)]

"""
## Map 
"""
st.map(dfMap)
"""
## Data 
"""
dfMap

"""
## Pickups por hora
"""
st.bar_chart(dfPickups.groupby('Hora').count())
