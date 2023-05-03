from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
import json
import time
from kafka import KafkaProducer



ORDER_KAFKA_TOPIC = "user_posts"

producer = KafkaProducer(bootstrap_servers=["b-2.kafkaproject.9ke3eg.c3.kafka.eu-west-3.amazonaws.com:9092"],
                                            value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# ORDER_LIMIT = 150

# producer = KafkaProducer(bootstrap_servers=["localhost"],
# 			value_serializer=lambda x: json.dumps(x).encode('utf-8'))

router = APIRouter(
    prefix="/posts", #replace /posts with / or /{id} in different routes below
    tags=["Posts"]
)
# retrieve all posts with ORM or SQL Alchemy
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db),
              current_user: int=Depends(oauth2.get_current_user),
              limit: int = 10,skip: int = 0,
              search: Optional[str] = ""):
    
    # # To show the user all posts
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)
    #                                    ).limit(limit).offset(skip).all()

    # Performing left outer join, group by and count 
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id) \
    .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #To ensure the current logged user retrieves only his his posts
    # posts=db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

    return posts


# Create a new post
@router.post("/create",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate,db: Session=Depends(get_db),
                 current_user: int=Depends(oauth2.get_current_user)):

    new_post=models.Post(user_id=current_user.id,**post.dict()) #unpack post request from user and stores in different fields for the database
    db.add(new_post) #add the post to the database
    db.commit() # commit changes to the database
    db.refresh(new_post) #refresh the database to return the new post
    producer.send(ORDER_KAFKA_TOPIC, post.dict()) 
    # print(json.dumps(post.dict())) 
    # print(post.dict())
    return new_post


# Retrieve a particular post by its USER ID
@router.get("/{id}",response_model=List[schemas.PostOut])
def get_post(id:int, db: Session=Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,skip: int = 0,
              search: Optional[str] = ""):

    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id) \
    .filter(models.Post.user_id == id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    post = post_query.all()
        
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} or {search} search word were not found')
    
    # # To ensure user only retrieve only post with his user id
    # if post.id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"You are not authorized to view this post")    
    # To ensure current logged in user retrieves only his post

    return post


# Updating a post by its USER ID
@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.PostResponse)
def update_post(id:int, updated_post: schemas.PostCreate,
                db: Session=Depends(get_db),
                current_user: int=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} doesn't exists and can't be updated")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"You are not authorized to update this post")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()


# Deleting a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session=Depends(get_db),
                current_user: int=Depends(oauth2.get_current_user)):
    
    post_query=db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exist and can't deleted")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"You are not authorized to delete this post")

    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)