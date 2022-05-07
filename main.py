#Python
from turtle import title
from typing import Optional

#Pydanyic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Path, Body, Query


app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    birthday: str
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None
    

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