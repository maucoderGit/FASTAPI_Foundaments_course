#Python
from datetime import date as date_type
from enum import Enum
from typing import Optional

#Pydanyic
from pydantic import BaseModel, Field

#FastAPI
from fastapi import FastAPI, Path, Body, Query


app = FastAPI()

# Models

class Countries(Enum):
    venezuela = 'venezuela'
    peru = 'peru'
    argentina = 'argentina'
    chile = 'chile'


class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=180,
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=180,
    )
    country: Countries = Field(
        ...
    )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    birthday: date_type = Field(
        ...,
        alias='date'
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


@app.get('/')
def home():
    return {'Hello': 'World'}


@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person

# Validations: Query Parameters
# min_length and max_length both are query validators

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None, min_length=1,
        max_length=50,
        title='Person Name',
        description='This is the person name, It\'s between 1 and 50 characters'
        ),
    born_day: Optional[str] = Query(
        ...,
        title='Person Age',
        description='This is the person age. It\'s required'
        ),
):
    return {name: born_day}

# Validations: Path parameters

@app.get('/person/detail{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='User id',
        description='This is the User Id, It\'s required'
        )
):
    return {person_id: 'It exists!'}

# Validations: Request Body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is the person ID',
        gt=0,
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = dict(person)
    result.update(dict(location))
    return result