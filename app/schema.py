from typing import Optional
from pydantic import BaseModel, conint
from datetime import datetime

#each model is respondible for what the user could enter , ex is 
#the model is only is_published the user can only set true or false


class CreatePost(BaseModel):
    title: str
    content: str


class ReturnedData(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        orm_mode = True

class PostSchema(BaseModel):
    id : int
    title: str
    content: str
    user_id: int
    owner: ReturnedData

class PostOut(BaseModel):
     Posts : PostSchema
     votes : int

class Usercreate(BaseModel):
     email : str
     password : str

class Useresponse(BaseModel):
     id: int
     email : str
     created_at : datetime


class Userlogin(BaseModel):
     email : str
     password: str     

class Token(BaseModel):
     access_token : str
     token_type: str

class TokenData(BaseModel):
     id: Optional[str]
          

class VoteSchema(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

