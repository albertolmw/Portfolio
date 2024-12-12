import pandas as pd
import yfinance as yf
import datetime
from datetime import date, timedelta
today = date.today()
#from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
#Info stocks close price from 03 oct 2024 until today, META, NVDA, GOOGL, BABA, WMT in mexican pesos
PORT=pd.DataFrame()
start='2024-10-03'
STOCKS=['META.MX','NVDA.MX','GOOGL.MX','BABAN.MX','WALMEX.MX']
for stock in STOCKS:
    PORT[stock]= yf.Ticker(stock).history(start=start, end=today).Close
#Number of days
days=(today-datetime.datetime.strptime(start, '%Y-%m-%d').date()).days
weights=[1,4,3,5,32]
#Yields
for stock in STOCKS:
    PORT[stock+'_yield']=PORT[stock].pct_change()
SUMYIELD={}
for stock in STOCKS:
    SUMYIELD[stock]=PORT[stock+'_yield'].sum()
#Earning each stock
EARNING={}
for stock in STOCKS:
    EARNING[stock]=(PORT[stock].iloc[-1]-PORT[stock].iloc[0])*weights[STOCKS.index(stock)]
SUMPORT=0
HISTPORT=pd.DataFrame()
#HISTPORT to plot
for stock in STOCKS:
    HISTPORT[stock]=PORT[stock]*weights[STOCKS.index(stock)]
HISTPORT['SUM']=HISTPORT.sum(axis=1)
#Portfolio Value
SUMPORT=HISTPORT['SUM'].iloc[-1]
#Yield port hist
YIELDp=(HISTPORT['SUM'].iloc[-1]/HISTPORT['SUM'].iloc[0])-1
#Earning port hist
EARNp=HISTPORT['SUM'].iloc[-1]-HISTPORT['SUM'].iloc[0]
#Yield port today
YIELDt=(HISTPORT['SUM'].iloc[-1]/HISTPORT['SUM'].iloc[-2])-1
#Earning port today
EARNt=HISTPORT['SUM'].iloc[-1]-HISTPORT['SUM'].iloc[-2]
import streamlit as st
import pandas as pd


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('My Portfolio in GBM')

#st.sidebar.subheader('Start data:', start,'\nEnd data:', today)
#time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max'))

#st.sidebar.subheader('Donut chart parameter')
#donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

#st.sidebar.subheader('Line chart parameters')
#plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
#plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown('''
---
Created with ❤️ by albertolmw.
''')


# Row A
st.markdown('### Portfolio')
col1, col2= st.columns(2)
col1.metric("Valor Actual", SUMPORT)
col2.metric("Dias transcurridos",days)

# Row B
#seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
#stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

'''c1, c2 = st.columns((7,3)) #70%screen Plot 1 and 30% P2
with c1:
    st.markdown('### Historic Portfolio')
    st.line_chart(HISTPORT, x = HISTPORT.index, y = HISTPORT.columns)
with c2:
    st.markdown('### Rendimiento hoy')
    metric('Earning', EARNt)

# Row C
#st.markdown('### Line chart')
#st.line_chart(seattle_weather, x = 'date', y = plot_data, height = plot_height)'''
