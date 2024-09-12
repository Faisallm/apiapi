from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    body: str

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

class ShowBlog(Blog):
    author: ShowUser

class User(ShowUser):
    password: str