#Python
from datetime import date as date_type
from enum import Enum
from typing import Optional

#Pydanyic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import HTTPException
from fastapi import FastAPI, Form, Path, Body, Query, Header, Cookie, UploadFile, File
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

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=25,
        example='maucoder'
        )
    message: str = Field(
        default='Login Succesfuly!',
        max_length=80,        
        )
    
class LoginPassword(LoginOut):
    password: str = Field(...)

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
    status_code=status.HTTP_200_OK,
    tags=['Home']
    )
def home():
    """
    Home Page
    
    This Path operation shows a JSON message with keys: "Hello" and "world" as values.
    
    Parameters:
    - This function doesn't receive parameters

    Returns a JSON with key: "hello", value: "world"
    """
    return {'Hello': 'World'}

# Request and response body

@app.post(
    path='/person/new', 
    response_model=Person,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons'],
    summary='Create Persons in the app'
    )
def create_person(
    person: Person = Body(...)
    ):
    """
    Create Person
    
    This Path operation creates a person in the app and saves the information in the database
    
    Parameters:
    - Request body parameter
        - **person: Person** -> A person model with first name, last name, birthday, hair_color, is_married
    
    Returns a person model with first name, last name, birthday, hair_color, marital_status
    """
    return person

# Validations: Query Parameters
# min_length and max_length both are query validators

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    deprecated=True
    )
def show_person(
    name: Optional[str] = Query(
        default=None,
         min_length=1,
        max_length=50,
        title='Person Name',
        description='This is the person name, It\'s between 1 and 50 characters',
        example='Rocio'
        ),
    born_day: Optional[date_type] = Query(
        default= None,
        title='Person Age',
        description='This is the person age. It\'s required',
        example='2022-05-08'
        ),
):
    """
    Show Person
    
    This Path operation Shows a person in the app
    
    Parameters:
    - Request body parameter
        - **name: Str** -> A optional person name
        - **born_day: Date_type** A optional birthday

    Returns a person's data with first name, birthday
    """
    return {name: born_day}

# Validations: Path parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path='/person/detail{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons']
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
    """
    Show Person
    
    This Path operation validates if a person exists in the database
    
    Parameters:
    - Request body parameter
        - **id: int** -> A person id
    
    Returns a message with id, message if it exists or doesn't exist
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This id doesn\'t exist'
        )
    return {person_id: 'It exists!'}


# Validations: Request Body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons']
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
    """
    Update Person

    Gets a person id, Person Model with the first name, last name, birthday, hair color, marital status and update information in a database
    
    Parameters:
    - Request body parameter
        - **person_id: int** -> an id from an user
        - **person: Person** -> A person model with first name, last name, birthday, hair color, marrital status
        - **location: Location** -> A location Model that receives an city, country and status
    
    Returns a New Person model with first name, last name, birthday, hair color, married status, and Location with city, status, and country
    """
    result = dict(person)
    result.update(dict(location))
    return result

# Forms

@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Forms']
    )
def login(
    Username: str = Form(...),
    Password: str = Form(...)
    ):
    """
    Login

    This Path operation gets the username and password to validate the user account
    
    Parameters:
    - Request Body
        - **Username: str** -> Obligatory Form model
        - **Password: str** -> Obligatory Form model
    
    returns a LoginOut model with a username
    """
    return LoginOut(username=Username)

# Coockie & Header

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Support']
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email: EmailStr = Form(
        ...,
    ),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    """
    Contact

    This Path operation gets information to contact developers.
    
    Parameters:
    - Request Body:
        - **First_name: str** -> Obligatory Form Object, Person's last name
        - **Last_name: str** -> Obligatory Form Object. Person's last name
        - **Email: EmailStr** -> Person's email adress, Obligatory
        - **message: str** -> Form obligatory object, gets user message
        - **user_agent: Optional[str]** -> gets parameter HEADER.
        - **ads: Optional[str]** -> Cookie's from user
    
    Returns user_agent model with first name, last name, email, header, cookies
    """
    return user_agent

@app.post(
    path='/post-image',
    status_code=status.HTTP_202_ACCEPTED,
    tags=['Upload']
    )
def post_image(
    image: UploadFile = File(...),
):
    """
    Post Image

    This Path Operator gets a user image with Filename, size, and format.

    Parameters:
    - Request Body:
        - **Image: UploadFile** -> Gets an obligatory user image

    returns a JSON of an image with filename, format, and size.
    """
    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': round((len(image.file.read()) / 1024), ndigits=2)
    }