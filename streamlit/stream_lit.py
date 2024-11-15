import streamlit as st
import pandas as pd
import requests
import json
from PIL import Image
from requests.models import Response

#st.set_page_config(layout="wide")
st.set_page_config(
    page_title="'Immo Eliza Property Price Predictor",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

property = {
  "type_of_property": "UNKNOWN",
  "subtype_of_property": "UNKNOWN",
  "number_of_rooms": 0,
  "living_area": 0,
  "furnished": True,
  "open_fire": True,
  "terrace_surface": 0,
  "garden": 0,
  "swimming_pool": True,
  "facades": 0,
  "land_area": 0,
  "state_of_building": "UNKNOWN",
  "equipped_kitchen": "UNKNOWN"
}
image, title = st.columns([0.8,2])
with image:
  image = Image.open('./streamlit/property.png')
  st.image(image, width=200)
with title:
  st.title(':rainbow[Immo Eliza Property Price Predictor]')

  st.subheader("Provide the property details to predict the price")
col1, col2, col3 = st.columns(3)
with col1:
  property['type_of_property'] = st.selectbox(f':blue[What is the type of your property?]', placeholder='Choose an option', options=('UNKNOWN','HOUSE', 'APARTMENT'))

  property['subtype_of_property'] = st.selectbox(':blue[What is the sub type of your property?]', ('HOUSE' ,'EXCEPTIONAL_PROPERTY', 'FARMHOUSE' ,'APARTMENT' ,'TOWN_HOUSE',
  'VILLA', 'CASTLE', 'APARTMENT_BLOCK', 'GROUND_FLOOR' ,'CHALET' ,'PENTHOUSE',
  'MIXED_USE_BUILDING', 'COUNTRY_COTTAGE', 'BUNGALOW' ,'DUPLEX', 'MANSION',
  'FLAT_STUDIO', 'SERVICE_FLAT', 'MANOR_HOUSE', 'LOFT', 'OTHER_PROPERTY',
  'TRIPLEX', 'KOT'))
  property['number_of_rooms'] = st.slider(":blue[Enter the number of rooms for the property]", 0, 100,1)

  property['living_area'] = st.slider(":blue[Provide Living area in m2]", 0, 10000,50)

with col2:
  property['furnished'] = st.selectbox(':blue[Is the property Furnished?]', ('YES','NO'))

  property['open_fire'] = st.selectbox(':blue[Does property have Openfire?]', ('YES','NO'))
  property['terrace_surface'] = st.slider(":blue[Provide terrace area in m2]", 0, 1000,50)

  property['swimming_pool'] = st.selectbox(':blue[Does the property have Swimming pool?]', ('YES','NO'))  
  property['garden'] = st.slider(":blue[Provide Garden area in m2]", 0, 1000,50)
with col3:
  

  property['facades'] = st.slider(":blue[Please provide number of Facades]", 0, 15,1)

  property['land_area'] = st.slider(":blue[Provide land area in m2]", 0, 1000000,1)

  property['state_of_building'] = st.selectbox(':blue[What is the state of your buiding?]', ('UNKNOWN','GOOD', 'TO_BE_DONE_UP', 'TO_RENOVATE' ,'AS_NEW', 'JUST_RENOVATED'
  , 'TO_RESTORE'))

  property['equipped_kitchen'] = st.selectbox(':blue[What is the state of your kitchen?]', ('UNKNOWN','HYPER_EQUIPPED', 'INSTALLED','SEMI_EQUIPPED', 'NOT_INSTALLED', 'USA_INSTALLED', 'USA_HYPER_EQUIPPED', 'USA_SEMI_EQUIPPED', 'USA_UNINSTALLED'))

#st.button('Predict', key=1)
json_data = json.dumps(property)
base_url = 'https://immo-eliza-deployment-a02a.onrender.com/'
#base_url = 'http://127.0.0.1:8000'
endpoint = 'property_info'
c0l1,col2,col3 = st.columns([10,2,10])
col11,col21,col31 = st.columns([0.5,1,0.3])
result = Response()

with col2:
  st.markdown("""
<style>.element-container:has(#button-after) + div button {
 background-color: blue;
 p{
 color : white;
  }
 }</style>""", unsafe_allow_html=True)
  st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
  #st.button('My Button')
  if st.button('Predict Price'):
      response = requests.get(base_url)
      if response.status_code == 200:
          #st.success(response.content)
        
        result = requests.post(url=f'{base_url}/{endpoint}', data=json_data)
        with col21:
          if result.status_code == 200:
            st.balloons()
            st.success(f"### Predicted price for your property is € {result.json()['price']}")
          else:
            st.error(f"{result.content}")
