from pydantic import BaseModel, Field

class Company(BaseModel):
    name: str

class User(BaseModel):
    id: int
    name: str
    email: str
    company: Company

class Post(BaseModel):
    id: int
    user_id: int = Field(alias="userId")
    title: str
    body: str
