

import json
from kafka import KafkaConsumer
import snowflake.connector

from nyc_taxi_pipeline.config.settings import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC_RAW,
    KAFKA_GROUP_ID,
    SNOWFLAKE_CONFIG
)
from nyc_taxi_pipeline.utils.data_cleaner import clean_record


def main():
    # ================= Kafka Consumer =================
    consumer = KafkaConsumer(
        KAFKA_TOPIC_RAW,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    # ================= Snowflake Connection =================
    sf_conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    sf_cursor = sf_conn.cursor()

    # ================= Insert SQL (EXACT MATCH TO TABLE) =================
    insert_sql = """
    INSERT INTO NYC_TAXI_PROJECT.CLEAN.YELLOW_TAXI_CLEAN (
        "VENDOR_ID",
        "PICKUP_TIME",
        "DROPOFF_TIME",
        "passenger_count",
        "trip_distance",
        "PICKUP_LOCATION",
        "DROPOFF_LOCATION",
        "payment_type",
        "fare_amount",
        "total_amount"
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    batch = []
    BATCH_SIZE = 500
    total_inserted = 0
    total_dropped = 0

    print("✅ Consumer started. Cleaning data and inserting into Snowflake...")

    # ================= Consume → Clean → Insert =================
    try:
        for msg in consumer:
            cleaned = clean_record(msg.value)

            if cleaned:
                batch.append((
                    cleaned["VENDOR_ID"],
                    cleaned["PICKUP_TIME"],
                    cleaned["DROPOFF_TIME"],
                    cleaned["PASSENGER_COUNT"],
                    cleaned["TRIP_DISTANCE"],
                    cleaned["PICKUP_LOCATION"],
                    cleaned["DROPOFF_LOCATION"],
                    cleaned["PAYMENT_TYPE"],
                    cleaned["FARE_AMOUNT"],
                    cleaned["TOTAL_AMOUNT"]
                ))
            else:
                total_dropped += 1

            if len(batch) >= BATCH_SIZE:
                sf_cursor.executemany(insert_sql, batch)
                sf_conn.commit()
                total_inserted += len(batch)

                print(
                    f"Inserted: {total_inserted} | Dropped (bad records): {total_dropped}"
                )
                batch.clear()

    except KeyboardInterrupt:
        print("⛔ Consumer stopped manually")

    finally:
        if batch:
            sf_cursor.executemany(insert_sql, batch)
            sf_conn.commit()
            total_inserted += len(batch)

        sf_cursor.close()
        sf_conn.close()
        print(f"✅ Final Inserted: {total_inserted}")
        print(f"⚠️ Total Dropped: {total_dropped}")


if __name__ == "__main__":
    main()
