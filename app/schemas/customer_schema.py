from pydantic import BaseModel


class CustomerBase(BaseModel):
    name = str
    address = str
    salary = float

class CustomerCreate(CustomerBase):
    id: str

class CustomerUpdate(BaseModel):
    name: str|None = None
    address: str|None = None
    salary: float|None = None

class CustomerResponce(CustomerBase):
    id: str

    class Config:
        orm_mode = True