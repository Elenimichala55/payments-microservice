FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

COPY ./app ./app
COPY wait_for_kafka.sh .

RUN pip install sqlalchemy psycopg2-binary aiokafka

RUN chmod +x wait_for_kafka.sh

CMD ["./wait_for_kafka.sh", "python", "-m", "app.processor"]