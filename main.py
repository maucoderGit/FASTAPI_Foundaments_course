#Python
from typing import Optional

#Pydanyic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query


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
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    born_day: Optional[str] = Query(...),
):
    return {name: born_day}