#Python
from typing import Optional

#Pydanyic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body


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