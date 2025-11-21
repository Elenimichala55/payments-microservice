import os
import asyncio
from aiokafka import AIOKafkaProducer
import json

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")

producer = None

async def get_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        await producer.start()
    return producer

async def send_payment_created_event(payment):
    producer = await get_producer()
    await producer.send_and_wait("payment_created", payment)
