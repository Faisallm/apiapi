from fastapi import FastAPI

import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# imports should go below this line, for various reasons
from blog import models, database
from blog.routers import blog, user

app = FastAPI()

# this is what create the db
models.Base.metadata.create_all(bind=database.engine)


app.include_router(blog.router)
app.include_router(user.router)


