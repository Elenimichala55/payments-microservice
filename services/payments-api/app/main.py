from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db
from app.models.payment import Payment
from app.schemas.payment_schema import PaymentCreate, PaymentResponse
from app.kafka_producer import send_payment_created_event

import asyncio

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payments API")

@app.post("/payments/", response_model=PaymentResponse)
async def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):

    payment = Payment(
        sender=payload.sender,
        receiver=payload.receiver,
        amount=payload.amount,
        status="PENDING"
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Send Kafka event
    asyncio.create_task(send_payment_created_event({
        "payment_id": payment.id,
        "amount": payment.amount,
        "sender": payment.sender,
        "receiver": payment.receiver
    }))

    return payment


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        return {"error": "Payment not found"}
    return payment
