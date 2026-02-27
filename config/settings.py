







# Kafka
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC_RAW = "nyc_taxi_raw"
KAFKA_GROUP_ID = "nyc_taxi_consumer"

# MySQL (SOURCE)
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Dimpu@123",
    "database": "new_york_taxi "
}

# Snowflake (TARGET)
SNOWFLAKE_CONFIG = {
    "user": "Giramonirp",
    "password": "Rajeev@123123123",
    "account": "gkvycjb-kl73766",
    "warehouse": "COMPUTE_WH",
    "database": "NYC_TAXI_PROJECT",
    "schema": "CLEAN"
}
