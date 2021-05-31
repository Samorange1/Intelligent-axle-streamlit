from enum import auto
import streamlit as st
import plotly.graph_objects as go
import urllib.request
import json
import time
from datetime import datetime
from dateutil import tz
import re
from PIL import Image

READ_API_KEY='BN6PPECPATKW9JWB'
CHANNEL_ID= '1387825'
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

page_logo = "https://www.aam.com/images/default-source/logos/aam-logo.svg?sfvrsn=fba51032_4"

banner = Image.open('C:\\Users\\madha\\Downloads\\Banner.png')

st.set_page_config(
    page_title="AAM Inteligent Axle Client", page_icon=page_logo, layout = "wide"
)


st.image(banner, use_column_width=True)

st.text("")
st.text("")

st.markdown("<h2><b>Welcome to AAM's Axle Health Monitoring Console!</b></h2>", unsafe_allow_html=True)

st.markdown("<h3>This is a web tool to monitor the status of the axle of your vehicle in real time</h3>", unsafe_allow_html=True)

st.text("")
st.text("")
st.text("")
st.text("")

col1, col2 = st.beta_columns((1,1))

with col1:
    ut1= st.empty()
    ut2= st.empty()
    ut3= st.empty()
    ut4= st.empty()
    st.text("")
    st.text("")
    ut5= st.empty()
with col2:
    pl = st.empty()



while True:
    TS = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                       % (CHANNEL_ID,READ_API_KEY))

    response = TS.read()
    data=json.loads(response)


    a = data['created_at']
    b = float(data['field1'])
    new_data = b
    Date_Time = re.sub('[A-Z]', ' ', a).strip()
    utc = datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    Local_Date_Time = str(utc.astimezone(to_zone))
    Local_Date_Time,y = Local_Date_Time.split("+",1)
  
    fig = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = b,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Axle Health", 'font': {'size': 30}},
   # delta = {'reference': temp, 'increasing': {'color': "Red"}, 'decreasing': {'color':"Gray"} },
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "Black",'ticklen':20},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 5,
        'bordercolor': "black",
        'steps': [
            {'range': [0, 50], 'color': 'green'},
            {'range': [50, 80], 'color': 'yellow'},
            {'range': [80, 100], 'color': 'red'}],
        }))

           
    ut1.markdown("<h3><b>Name</b>: XXXXXXXXXXXXX</h3>", unsafe_allow_html=True)
    ut2.markdown("<h3><b>Vehicle</b> : XXXXXXXXXX</h3>", unsafe_allow_html=True)
    ut3.markdown("<h3><b>Registration number</b>: XXXXXXXXX</h3>", unsafe_allow_html=True)
    ut4.markdown("<h3><b>Driver name </b>: Aryaman Patel</h3>", unsafe_allow_html=True)
    if (b<50):
        ut5.info('Remark: Axle is in Good Condition')
    elif(b>=50 and b<80):
        ut5.warning('Remark: Axle needs servicing soon')
    else:
        ut5.error('Remark: AXLE SERVICE REQUIRED IMMEDIATELY')
    

    pl.plotly_chart(fig, width=100)
    fig.update_layout(paper_bgcolor = "white", font = {'color': "darkblue", 'family': "Arial",'size':24})
    

    
        
    time.sleep(2)   
    TS.close()



    