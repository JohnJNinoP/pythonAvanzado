from sklearn.linear_model import LinearRegression

#python
from typing import Optional 
from enum import Enum

# pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#fastapi
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Body, Query , Path , Form, Cookie , Header , UploadFile , File
from fastapi import status
app = FastAPI()

persons = [1,2,3,4,5]

#Enums

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blone = "blone"
    red = "red"

#Models
class Location(BaseModel):
    city : str
    state : str
    country : str

class PersonBase(BaseModel):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50,
        title="Person's name"
        )
    last_name  : str
    age : int = Field(
        ...,
        gt=0,
        le=115)
    hair_color : Optional[HairColor] = Field(default=None)
    is_married : Optional[bool] = Field(default=None)
    email : EmailStr = Field(...)


class Person(PersonBase):    
    password : str = Field(...,min_length=8)
    class Config:
        schema_extra = {
            "example" : {
                "first_name": "Ricardo",
                "last_name": "test",
                "age": 35,
                "hair_color": "white",
                "is_married": True,
                "email": "ricardo@mail.com",
                "password" :"12345678"
            }
        }    


class InputData(BaseModel):
    x: float
    y: float


#Responses 
class OutputData(BaseModel):
    slope: float
    intercept: float
    score: float      

class OutPerson(PersonBase):
    pass

class OutLogin(BaseModel):
    username : str = Field(...,max_length=20 )

@app.get( path= "/", status_code=status.HTTP_200_OK)
def  home():
    return {"Hello" : "world"}


# request and response body

@app.post(
    path= "/person/new" , 
    response_model = OutPerson , 
    status_code= status.HTTP_201_CREATED,
    tags=["Person"])
def create_person(person : Person = Body(...)):
    return person


# validation : queary parameters

@app.get( 
    path= "/person/detail" , 
    status_code=status.HTTP_200_OK,
    tags=["Person"] )
def show_person(
    name : Optional[str] = Query(
        None , 
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio"),
    age : int = Query(
        ...,
        title="Person age",
        description="This is the person age, It's required",
        example=50
    )):
    return { name,age }




@app.get( 
    path="/person/detail/{person_id}" ,
    status_code= status.HTTP_200_OK,
    deprecated=True,
    tags=["Person"])
def show_person_id(
    person_id : int = Path(
        ...,
        gt=0,
        title="Id the person"
        ,example=10
        )):
        if person_id not in persons:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="This id person doesn't found"
            )
        else :    
            return { "succes" : True, "Id" : person_id }

@app.put(path="/person/{person_id}",
status_code= status.HTTP_201_CREATED,
tags=["Person"] )
def udpate_person(
    person_id : int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        example=2),
    person :Person = Body(...)):
    return {person_id,person.first_name,person.last_name,person.age,person.hair_color,person.is_married}


@app.put(
    path="/person",
    status_code= status.HTTP_201_CREATED,
    tags=["Person"])
def udpate_person(
    person :Person = Body(...)
    ):

    result = person.dict()
    #result.update(location.dict())
    return result
    #return {person.dict(), location.dict()}

@app.post(
    path="/linear-regression/",
    status_code= status.HTTP_201_CREATED,
    tags=["Test"])
async def linear_regression(data: InputData):
    """
    Example about line regretion 
    """
    X = [[data.x]]
    y = [data.y]

    model = LinearRegression()
    model.fit(X, y)

    return OutputData(slope=model.coef_[0], intercept=model.intercept_, score=model.score(X, y))


@app.post(
    path="/login",
    response_model=OutLogin,
    status_code=status.HTTP_200_OK,
    tags=["login"])
def login(
    username : str = Form(...),
    password : str = Form(...)
    ):
    """Generate login of the user in the sistem"""
    return OutLogin(username=username)


# cookies and header parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_201_CREATED,
    tags=["Contact"]
    )
def contact(
    first_name : str = Form(..., max_length=20, min_length=1),
    last_name : str = Form(..., max_length=20, min_length=1),
    email : EmailStr = Form(...),
    message : str = Form(...,min_length=20), 
    user_agent : Optional[str] = Header(default=None),
    ads : Optional[str] = Cookie(default=None)
):
    """
    Valid header
    """
    return user_agent

@app.post(
    path="/post-image",
    tags=["UploadFile"])
def post_image(
    image : UploadFile = File(...)
):
    """
    Load file
    This path operation load a file and save
    parameters:
    - File path
    """
    return {
        "FileName" : image.filename,
        "Format" : image.content_type,
        "Size(kb)" : round(len(image.file.read())/1024,ndigits=2)
    }