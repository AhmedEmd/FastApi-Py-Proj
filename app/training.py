#library imports
from fastapi import FastAPI
from random import randrange;
import time
from app import auth
from . import models
from .database import engine
from .routers import post, user , vote
from .configuration import settings
from fastapi.middleware.cors import CORSMiddleware




origins = [
    "*"
]



models.Base.metadata.create_all(bind=engine)

#create fastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapidatabase', user='postgres',
#                                 password='ah01011747352', cursor_factory=RealDictCursor)
#         curser = conn.cursor()
#         print("Database connection success")
#         break
#     except Exception as error:
#         print("Connecting to the database failed")
#         print("Error:", error)
#         time.sleep(2)