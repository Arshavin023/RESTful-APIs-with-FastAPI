# Connecting to Postgres database with SQL Achemy
# Importing libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# Creating connecting strings
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#SQL engine to interact with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


# Create session for the database 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    # # Connect to postgres database    
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='admin123!',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Succesfully connected to the database")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print(f"Error: {error}")
#         time.sleep(5)

# #This is acting like the database
# my_posts=[{"title":"title of post 1","content":"content 1","id":1},
#           {"title":"favorite foods","content":"I love Pizze","id":2}]

# def find_post(id):
#      for post in my_posts:
#         if post['id'] == id:
#              return post

# def find_index_post(id):
#     for index, post in enumerate(my_posts):
#         if post['id'] == id:
#             return index