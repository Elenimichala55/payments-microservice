from pydantic import BaseModel

class PaymentCreate(BaseModel):
    sender: str
    receiver: str
    amount: float

class PaymentResponse(BaseModel):
    id: int
    sender: str
    receiver: str
    amount: float
    status: str

    class Config:
        orm_mode = True