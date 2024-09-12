from fastapi import APIRouter, status, Depends, utils, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    user_input = request.model_dump()
    user_input['password'] = utils.Hash.bcrypt(user_input['password'])
    new_user = models.User(**(user_input))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist!"
        )
    
    return user