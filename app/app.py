# Importing libraries
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, authentication, vote, getuserpost
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


# This is commented out cos it's no longer needed since alembic takes
# care of creation and update of objects on database
# models.Base.metadata.create_all(bind=engine)

# instantiate fastapi
app = FastAPI()

# List of all domains that can talk to our API
# origins = ['https://www.google.com','https://www.youtube.com']

# Allow every domain access the API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)
app.include_router(getuserpost.router)

# retrieve home page
@app.get("/")
def root():
    return {"message": "Hello World"}





