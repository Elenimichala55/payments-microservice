# Payments Microservice - (Kafka + FastAPI + PostgreSQL + Docker Compose)
A fully containerized payments microservice demonstrating event-driven architecture using Apache Kafka, FastAPI, PostgreSQL, and Python workers.
The service allows clients to create payments, publishes events to Kafka, processes them asynchronously with a background worker, and updates the database.

## Features
### FastAPI Payments API
- Create new payments
- Store data in PostgreSQL
- Emit a Kafka payment_created event

### Payments Processor (Worker Service)
- Listens to Kafka events
- Simulates fraud check / processing
- Updates payment status (CONFIRMED or FAILED)
- Publishes results to new Kafka topics

### Kafka Integration
Topics auto-created:
- payment_created
- payment_confirmed
- payment_failed

### Fully Containerized
All services run using a single command:
```bash
docker compose up --build
```

## Architecture Overview
```
FastAPI (Payments API)
      ↓ emits
Kafka topic: payment_created
      ↓ consumed by
Payments Processor (Python worker)
      ↓ updates
PostgreSQL (payments table)
      ↓ emits
Kafka: payment_confirmed / payment_failed
```

## Run Locally (Docker Compose)

1. ### Clone the repository
```bash
  git clone https://github.com/<your-username>/payments-microservice.git
  cd payments-microservice
  ```

2. ### Start all services
```bash
docker compose up --build
```

This will start:
- Zookeeper
- Kafka
- PostgreSQL
- FastAPI service
- Payment processor worker

3. ### Test API
- Create a payment:
```bash
curl -X POST http://localhost:8000/payments \
-H "Content-Type: application/json" \
-d '{"sender":"alice","receiver":"bob","amount":50}'
```

- Get a payment:
```bash
curl http://localhost:8000/payments/1
```

## Project Structure
```
services
├── payments-api
│   ├── Dockerfile
│   ├── app
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── kafka_producer.py
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── payment.py
│   │   └── schemas
│   │       ├── __init__.py
│   │       └── payment_schema.py
│   └── requirements.txt
└── payments-processor
    ├── Dockerfile
    ├── app
    │   ├── __init__.py
    │   ├── db.py
    │   ├── kafka_consumer.py
    │   └── processor.py
    └── wait_for_kafka.sh

7 directories, 16 files
```
