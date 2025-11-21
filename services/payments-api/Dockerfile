FROM python:3.11

WORKDIR /app

COPY ./app ./app

RUN pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary aiokafka pydantic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
