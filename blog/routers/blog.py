from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, utils
from typing import List

router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    
    new_blog = models.Blog(**(request.model_dump()), user_id=1)

    db.add(new_blog)
    # commit changes to db
    db.commit()
    # same as returning *
    db.refresh(new_blog)

    return new_blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends()):

    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id: {id} does not exist!"
        )
    
    # delete the blog
    blog.delete(synchronize_session=False)
    # commit changes to db
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id: {id} does not exist!"
        )
    
    blog.update(request.model_dump(), synchronize_session=False)
    # persist changes to db
    db.commit()

    return "Updated successfully"


@router.get("/", response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(database.get_db)):
    # querying all the blogs from the db
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{id}", response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(database.get_db)):
    # get the first blog that matches our id
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id: {id} does not exist!"
        )

    return blog