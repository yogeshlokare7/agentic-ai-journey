
from pydantic import BaseModel, Field, field_validator

class Address(BaseModel):
    city: str
    pincode: str = Field(max_length=6, pattern=r"^\d{6}$", description="Pincode must be a 6-digit number")

class Customer(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Customer name must be between 1 and 100 characters")
    age: int= Field(ge=18, le=100, description="Customer age must be between 18 and 100")
    email: str | None = None
    address: Address
    tags: list[str] = []

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str | None) -> str | None:
       if v is None:
           return v
       v = v.strip().lower()
       if "@" not in v:
           raise ValueError("Invalid email address")
       return v   