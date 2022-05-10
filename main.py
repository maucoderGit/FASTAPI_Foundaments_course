#Python
from datetime import date as date_type
from enum import Enum
from typing import Optional

#Pydanyic
from pydantic import BaseModel, Field

#FastAPI
from fastapi import FastAPI, Path, Body, Query
from fastapi import status

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
        max_length=100,
        example='Caracas city'
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=180,
        example='Caracas'
    )
    country: Countries = Field(
        ...,
        example='venezuela'
    )

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Mauricio'
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Gonzalez Falcon'
        )
    birthday: date_type = Field(
        ...,
        alias='date',
        example='2003-10-30'
        )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example='black',
        )
    is_married: Optional[bool] = Field(
        default=None,
        example=False
        )

class Person(PersonBase):
        Password: str = Field(
        ...,
        min_length=8,
        example= 'MySecurePassword1234!"#$'
        )


@app.get(
    path='/',
    status_code=status.HTTP_200_OK
    )
def home():
    return {'Hello': 'World'}

# Request and response body

@app.post(
    path='/person/new', 
    response_model=Person,
    status_code=status.HTTP_201_CREATED)
def create_person(
    person: Person = Body(...)
    ):
    return person

# Validations: Query Parameters
# min_length and max_length both are query validators

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None, min_length=1,
        max_length=50,
        title='Person Name',
        description='This is the person name, It\'s between 1 and 50 characters',
        example='Rocio'
        ),
    born_day: Optional[date_type] = Query(
        ...,
        title='Person Age',
        description='This is the person age. It\'s required',
        example='2022-05-08'
        ),
):
    return {name: born_day}

# Validations: Path parameters

@app.get(
    path='/person/detail{person_id}',
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='User id',
        description='This is the User Id, It\'s required',
        example=3
        )
):
    return {person_id: 'It exists!'}

# Validations: Request Body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is the person ID',
        gt=0,
        example=3
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = dict(person)
    result.update(dict(location))
    return result