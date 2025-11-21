import asyncio
from aiokafka import AIOKafkaConsumer
import json
import os

KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")

async def start_consumer(handler):
    while True:
        try:
            consumer = AIOKafkaConsumer(
                "payment_created",
                bootstrap_servers=KAFKA_SERVER,
                value_deserializer=lambda v: json.loads(v.decode("utf-8"))
            )

            await consumer.start()
            print("Kafka connected! Listening for events...")
            break

        except Exception as e:
            print(f"Kafka not ready, retrying in 3s... ({e})")
            await asyncio.sleep(3)

    try:
        async for msg in consumer:
            await handler(msg.value)
    finally:
        await consumer.stop()