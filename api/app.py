from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
import pandas as pd
from predict import test
from typing import Literal

app = FastAPI()
subtype = ['HOUSE' ,'EXCEPTIONAL_PROPERTY'
, 'FARMHOUSE' ,'APARTMENT' ,'TOWN_HOUSE',
 'VILLA', 'CASTLE', 'APARTMENT_BLOCK', 'GROUND_FLOOR' ,'CHALET' ,'PENTHOUSE',
 'MIXED_USE_BUILDING', 'COUNTRY_COTTAGE', 'BUNGALOW' ,'DUPLEX', 'MANSION',
 'FLAT_STUDIO', 'SERVICE_FLAT', 'MANOR_HOUSE', 'LOFT', 'OTHER_PROPERTY',
 'TRIPLEX', 'KOT']
class property(BaseModel):
    type_of_property: Literal['HOUSE', 'APARTMENT', 'UNKNOWN']
    subtype_of_property: Literal['HOUSE' ,'EXCEPTIONAL_PROPERTY'
, 'FARMHOUSE' ,'APARTMENT' ,'TOWN_HOUSE',
 'VILLA', 'CASTLE', 'APARTMENT_BLOCK', 'GROUND_FLOOR' ,'CHALET' ,'PENTHOUSE',
 'MIXED_USE_BUILDING', 'COUNTRY_COTTAGE', 'BUNGALOW' ,'DUPLEX', 'MANSION',
 'FLAT_STUDIO', 'SERVICE_FLAT', 'MANOR_HOUSE', 'LOFT', 'OTHER_PROPERTY',
 'TRIPLEX', 'KOT']
    number_of_rooms: int
    living_area : int 
    furnished: Optional[bool]
    open_fire: Optional[bool]
    terrace_surface: Optional[int]
    garden: Optional[int]
    swimming_pool: Optional[bool]
    facades: Optional[int]
    land_area : Optional[int]
    state_of_building: Literal['UNKNOWN','GOOD', 'TO_BE_DONE_UP', 'TO_RENOVATE' ,'AS_NEW', 'JUST_RENOVATED'
, 'TO_RESTORE']
    equipped_kitchen: Literal['UNKNOWN','HYPER_EQUIPPED', 'INSTALLED','SEMI_EQUIPPED', 'NOT_INSTALLED', 'USA_INSTALLED', 'USA_HYPER_EQUIPPED', 'USA_SEMI_EQUIPPED', 'USA_UNINSTALLED']


@app.get('/')
def index():
    ''' Defining the starting index page'''
    return {'status':'Alive'}
@app.post('/property_info')
def create_property(data: property):
    #df = pd.DataFrame([data.dict()])
    try:
        input_data = property.model_validate(data)
    except ValidationError as e:
        return HTTPException(status_code=422, detail=f"Validation error in the request body: {str(e)}")
    print(input_data)
    data1 = input_data.model_dump()
    df = pd.DataFrame([data1])
    try:
        output = test(df)
    except Exception as e:
        return HTTPException(status_code=500, detail='Error in prediction')
    return {'price': output}
