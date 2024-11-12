from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
import pandas as pd
from predict import test

app = FastAPI()
class property(BaseModel):
    type_of_property: str | None
    subtype_of_property: str | None = Field(default='UNKNOWN', title="The field can be apartment | house")
    number_of_rooms: int
    living_area : int 
    furnished: Optional[bool]
    open_fire: Optional[bool]
    terrace_surface: Optional[int]
    garden: Optional[int]
    swimming_pool: Optional[bool]
    facades: Optional[int]
    land_area : Optional[int]
    state_of_building: Optional[str]
    equipped_kitchen: Optional[str]


@app.get('/')
def index():
    ''' Defining the starting index page'''
    return 'Welcome to Immoeliza api page'
@app.post('/property_info')
def create_property(data: property):
    #df = pd.DataFrame([data.dict()])
    data1 = data.dict()
    df = pd.DataFrame([data1])
    output = test(df)
    return {'price': output}
