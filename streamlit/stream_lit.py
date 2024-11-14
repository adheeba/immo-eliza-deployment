import streamlit as st
import pandas as pd
import requests
import json

st.title('Immo Eliza Property Price Predictor')

st.write("Provide the property details you want to predict the price")

type_of_property = st.selectbox('What is the type of your property', ('UNKNOWN','HOUSE', 'APARTMENT'))

subtype_of_property = st.selectbox('What is the sub type of your property', ('HOUSE' ,'EXCEPTIONAL_PROPERTY', 'FARMHOUSE' ,'APARTMENT' ,'TOWN_HOUSE',
 'VILLA', 'CASTLE', 'APARTMENT_BLOCK', 'GROUND_FLOOR' ,'CHALET' ,'PENTHOUSE',
 'MIXED_USE_BUILDING', 'COUNTRY_COTTAGE', 'BUNGALOW' ,'DUPLEX', 'MANSION',
 'FLAT_STUDIO', 'SERVICE_FLAT', 'MANOR_HOUSE', 'LOFT', 'OTHER_PROPERTY',
 'TRIPLEX', 'KOT'))
number_of_rooms = st.slider("Number of rooms", 0, 100,1)
number_of_rooms = "1"
living_area = st.slider("Living area in m2", 0, 100000,50)

furnished = st.selectbox('Furnished', ('YES','NO'))

open_fire = st.selectbox('Openfire', ('YES','NO'))
terrace_surface = st.slider("Terrace area in m2", 0, 1000,50)

garden = st.slider("Garden area in m2", 0, 1000,50)

swimming_pool = st.selectbox('Swimming pool?', ('YES','NO'))

facades = st.slider("Facades", 0, 100,1)

land_area = st.slider("Land area in m2", 0, 1000000,1)

state_of_building = st.selectbox('What is the state of your buiding', ('UNKNOWN','GOOD', 'TO_BE_DONE_UP', 'TO_RENOVATE' ,'AS_NEW', 'JUST_RENOVATED'
, 'TO_RESTORE'))

equipped_kitchen = st.selectbox('What is the state of your kitchen', ('UNKNOWN','HYPER_EQUIPPED', 'INSTALLED','SEMI_EQUIPPED', 'NOT_INSTALLED', 'USA_INSTALLED', 'USA_HYPER_EQUIPPED', 'USA_SEMI_EQUIPPED', 'USA_UNINSTALLED'))


property = {
  "type_of_property": type_of_property,
  "subtype_of_property": subtype_of_property,
  "number_of_rooms": number_of_rooms,
  "living_area": living_area,
  "furnished": furnished,
  "open_fire": open_fire,
  "terrace_surface": terrace_surface,
  "garden": garden,
  "swimming_pool": swimming_pool,
  "facades": facades,
  "land_area": land_area,
  "state_of_building": state_of_building,
  "equipped_kitchen": equipped_kitchen
}
#st.button('Predict', key=1)
json_data = json.dumps(property)
print(json_data)
base_url = 'https://immo-eliza-deployment-a02a.onrender.com/'
#base_url = 'http://127.0.0.1:8000'
endpoint = 'property_info'
if st.button('Predict'):
    response = requests.get(base_url)
    if response.status_code == 200:
        #st.success(response.content)
      result = requests.post(url=f'{base_url}/{endpoint}', data=json_data)
      if result.status_code == 200:
          st.markdown(f"### Predicted price for your property is € {result.json()['price']}")
      else:
          st.error(result.json())