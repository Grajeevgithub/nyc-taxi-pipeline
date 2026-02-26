



















import json
import mysql.connector
from kafka import KafkaProducer

from nyc_taxi_pipeline.config.settings import (
    MYSQL_CONFIG,
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC_RAW
)


def main():
    # Create Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8")
    )

    # Connect to MySQL
    mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = mysql_conn.cursor(dictionary=True)

    query = """
    SELECT
        VendorID AS vendor_id,
        tpep_pickup_datetime AS pickup_datetime,
        tpep_dropoff_datetime AS dropoff_datetime,
        passenger_count,
        trip_distance,
        PULocationID AS pickup_location_id,
        DOLocationID AS dropoff_location_id,
        payment_type,
        fare_amount,
        tip_amount,
        total_amount
    FROM yellow_taxi_trips
    """

    cursor.execute(query)

    count = 0
    for row in cursor:
        producer.send(KAFKA_TOPIC_RAW, row)
        count += 1

        if count % 1000 == 0:
            print(f"Sent {count} records to Kafka")

    producer.flush()
    cursor.close()
    mysql_conn.close()

    print(f"✅ Finished sending {count} records to Kafka")


if __name__ == "__main__":
    main()
