import asyncio
import json
import random
from aiokafka import AIOKafkaProducer
from sqlalchemy.orm import Session
from app.db import get_db
from app.kafka_consumer import start_consumer
from sqlalchemy import update
from sqlalchemy import text
import os

DATABASE_URL = os.getenv("DATABASE_URL")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")


# Kafka producer
async def get_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()
    return producer


# Payment processing logic
async def process_payment(event):
    payment_id = event["payment_id"]
    amount = event["amount"]

    print(f"Processing payment {payment_id} ...")

    # Decide success or failure (simple simulation)
    success = random.random() > 0.2   # 80% success rate

    # Update DB
    from sqlalchemy import create_engine
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()

    if success:
        new_status = "CONFIRMED"
        topic = "payment_confirmed"
    else:
        new_status = "FAILED"
        topic = "payment_failed"

    conn.execute(text("UPDATE payments SET status = :s WHERE id = :pid"),
                 {"s": new_status, "pid": payment_id})
    conn.commit()
    conn.close()

    # Emit Kafka event
    producer = await get_producer()
    await producer.send_and_wait(topic, {
        "payment_id": payment_id,
        "status": new_status
    })
    await producer.stop()

    print(f"Payment {payment_id} → {new_status}")


# Entry point
async def main():
    print("Starting payments processor ...")
    await start_consumer(process_payment)


if __name__ == "__main__":
    asyncio.run(main())