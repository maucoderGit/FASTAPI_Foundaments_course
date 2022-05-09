# Donation's API

# Challenge: Create a API to recive donations
# Getting: Person data, Payment Data, email and date

# Python

from datetime import date as date_type
from enum import Enum
from typing import Optional

#Pydanyic

from pydantic import BaseModel, EmailStr, Field, PaymentCardNumber

# FastAPI

from fastapi import Body, FastAPI, Path, Query

# MODELS

class Payment(BaseModel):
    card_num: PaymentCardNumber = Field(...)

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=60,
    )
    msg: str = Field(..., min_length=2,max_length=300)
    email: EmailStr = Field(...)
    birthday: date_type = Field(...)
    country: str = Field(...)

app = FastAPI()

@app.get('/')
def home():
    return {'Hello': 'World'}

@app.post('/dotanions/')
def donations(
    ong_id:Optional[int] = Query(
        default=None,
        gt=0,
        title='ONG ID',
        description='This is the ONG ID',
    ),
    person: Optional[Person]= Body(default=None),
    payment: Optional[Payment]= Body(default=None),
):
    results = (dict(person))
    results.update(dict(payment))
    return {ong_id: results}