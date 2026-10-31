
from pydantic import BaseModel, Field

class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str

class User(BaseModel):
    id: int
    name: str
    email: str
    company: Company

class Post(BaseModel):
    id: int
    userId: int = Field(alias="userId")
    title: str
    body: str

    