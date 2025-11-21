#!/bin/sh
echo "Waiting for Kafka at $KAFKA_BOOTSTRAP_SERVER..."

while ! nc -z kafka 9092; do
  sleep 1
done

echo "Kafka is up!"
exec "$@"