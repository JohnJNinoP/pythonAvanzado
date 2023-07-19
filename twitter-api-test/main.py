#python
import json
from uuid import UUID
from datetime import date , datetime
from typing import Optional, List




#pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body , Path
from fastapi import HTTPException

app = FastAPI()


 
class UserBase(BaseModel):
    user_Id : UUID = Field(...)
    email : EmailStr = Field(...)

class UserLogin(UserBase):
    password : str = Field(
        ...,
        min_length=8,
        max_length=60
    )    

class User(UserBase):
    first_Name : str  = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_Name : str  = Field(
        ...,
        min_length=1,
        max_length=50
        )
    birth_date : Optional[datetime] = Field(default=None)

class UserRegister(User):
    password : str = Field(
        ...,
        min_length=8,
        max_length=60
    )  

class Tweet(BaseModel):
    Id : UUID = Field(...)
    Content : str = Field(
        ...,
        min_length=1,
        max_length=250
        )
    create_at : datetime = Field(default=datetime.now())
    update_at : Optional[datetime] = Field(...)
    by : User
## Users
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
    )
def signup(user : UserRegister = Body(...)):
    """
    This path operation registres a user in the app
    
    Parameter
    - Requst body parameter
        - user: UserRegister

    Return a json with the next information
        - used_id : UUID
        - Email : EmalStr
        - First_name : str
        - Last_name : str
        - birth_date : datetime

    """

    with open("users.json","r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_Id"] = str(user_dict["user_Id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))

        return user;

    return User

@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Login"]
    )
def login():
    pass

@app.get(
    path="/users",
    response_model= List[User],
    status_code=status.HTTP_201_CREATED,
    summary="Show all users",
    tags=["Users"]
    )
def Users():
    """
    This method retorn all user in the app
    """
    with open("users.json","r" , encoding="utf-8") as f:
        results = json.loads(f.read());
        return results

@app.get(
    path="/users/{user_id}",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_users(
    user_id :str = Path(...) 
    ):
    with open("users.json","r",encoding="utf-8") as f:
        result_userts = json.loads(f.read())
        found_user = None
        for user in result_userts:
            if user['user_Id'] == user_id:
                found_user = user
                break
        if found_user == None:
            raise HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT,
                    detail="This id person doesn't found"
                )
        else:
            return found_user
        
@app.delete(
    path="/users/{user_id}/Delete",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Delete all users",
    tags=["Users"]
    )
def delete_user(
    user_id : str = Path(...)
):
    """
    This method delete a item about its Id

    Parameter 
        - ID
    """
    with open("users.json","r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_delete = None
        for user in results:
            if user["user_Id"] == user_id:
                user_delete = user
                user_delete['user_Id'] == str(user_delete['user_Id'])
                #del user
                results.remove(user)
                break   

                
        if  user_delete == None:
            raise HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT,
                    detail="This id person doesn't found"
                )
        else:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(results))
            return user_delete        

@app.put(
    path="/users/Update",
    response_model= User,
    status_code=status.HTTP_200_OK,
    summary="Update user",
    tags=["Users"]
    )
def udpate_user(user_udpate : User = Body(...)):
    """
    This method udpate a item about its Id

    Parameter 
        - ID
    """
    with open("users.json","r+",encoding="utf-8") as f:
        user_results = json.loads(f.read())
        user_found = None
        for user in user_results:
            if str(user['user_Id']) == str(user_udpate.user_Id):
                
                user['first_Name'] = user_udpate.first_Name
                user['last_Name'] = user_udpate.last_Name
                user['birth_date'] = str(user_udpate.birth_date)
                user['email'] == user_udpate.email
                user_found = user
                break
        
        if user_found == None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="This person doesn't found"
            )
        else:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(user_results))
            return user_found    

#tweet
@app.get(
    path="/",
    response_model=list[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Tweets",
    tags=["Tweets"]
    )
def home():
    """
    Home API endpoint for retrieving tweets.

    This method returns tweets as the response. The response data is validated against
    the 'Tweet' model, and the HTTP status code 200 (OK) is returned on
    success.

    Returns:
        List[Tweet]: List of tweets
    """
    with open("tweets.json","r",encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Post tweets",
    tags=["Tweets"]
    )
def post_tweet(tweet :Tweet = Body(...)):
    """
    """
    with open("tweets.json","r+",encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["Id"] = str(tweet_dict["Id"])
        tweet_dict["create_at"] = str(tweet_dict["create_at"])
        tweet_dict["by"]["user_Id"] = str(tweet_dict["by"]["user_Id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        
        if 'update_at' in tweet_dict:
            tweet_dict["update_at"] = str(tweet_dict["update_at"]) 
        results.append(tweet_dict)
        f.seek(0)
        f.truncate()
        f.write(json.dumps(results))
        return tweet

@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweets",
    tags=["Tweets"]
    )
def show_tweet(tweet_id:str = Path(...)):
    """
    """
    with open("tweets.json","r",encoding="utf-8") as f:
        results = json.loads(f.read())
        found_tweet = None
        for tweet in results:
            if tweet["Id"] == tweet_id:
                found_tweet = tweet
                break
        if found_tweet == None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="This Id tweet doesn's found"
            )
        else:
            return found_tweet

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweets",
    tags=["Tweets"]
    )
def delete_tweet(tweet_id:str = Path(...)):
    """
    """
    with open("tweets.json","r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_delete = None
        for tweet in results:
            if tweet["Id"] == tweet_id:
                tweet_delete = tweet
                #tweet_delete['user_Id'] == str(tweet_delete['user_Id'])
                #del user
                results.remove(tweet)
                break   

                
        if  tweet_delete == None:
            raise HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT,
                    detail="This id tweet doesn't found"
                )
        else:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(results))
            return tweet_delete

@app.put(
    path="/tweets/udpate",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweets",
    tags=["Tweets"]
    )
def update_tweet(tweet_update : Tweet = Body(...)):
    """
    """
    with open("tweets.json","r+",encoding="utf-8") as f:
        tweet_results = json.loads(f.read())
        tweet_found = None
        for tweet in tweet_results:
            if str(tweet['Id']) == str(tweet_update.Id):
                tweet['Content'] = tweet_update.Content
                tweet['update_at'] = str(datetime.now())
                tweet_found = tweet
                break
        
        if tweet_found == None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="This person doesn't found"
            )
        else:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(tweet_results))
            return tweet_found   