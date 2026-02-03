# 🚕 NYC Taxi Real-Time Data Pipeline (Kafka → Snowflake)

This project demonstrates a complete **real-time Data Engineering pipeline** using **Kafka, Python, Docker, and Snowflake**.  
NYC Yellow Taxi trip data is streamed, cleaned in real time, and loaded into Snowflake for analytics and reporting.

---

## 🎯 Objective

To build an end-to-end streaming pipeline that:
- Extracts data from a **MySQL source database**
- Streams records to **Apache Kafka**
- Cleans data **message by message**
- Loads clean records into **Snowflake**
- Handles large-scale data efficiently using batching

---

## 🧰 Tools & Skills Used

- **Python** (kafka-python, mysql-connector, Snowflake Connector)
- **Apache Kafka & Zookeeper**
- **MySQL** (Source system)
- **Snowflake** (Cloud Data Warehouse)
- **Docker & Docker Compose**
- **SQL**
- **Git & GitHub**

---

## ✅ Key Features

- ⚙️ Real-time streaming pipeline (MySQL → Kafka → Snowflake)  
- 🧹 Record-level data cleaning before ingestion  
- 📦 Batch inserts for high-performance Snowflake loading  
- 🧠 Fault-tolerant consumer with bad-record handling  
- 🐳 Fully Dockerized Kafka & Zookeeper setup  
- 📊 Production-ready project structure  

---

## 🧹 Data Cleaning Logic

Implemented in `utils/data_cleaner.py`

- Drop records with missing pickup/dropoff timestamps  
- Remove trips with invalid or zero distance  
- Filter out negative or invalid fare values  
- Convert timestamps to Snowflake-compatible format  
- Safely cast numeric columns  
- Skip invalid records without stopping the pipeline  

---

## 📊 Source & Target Tables

### Source: MySQL
- **Table:** `yellow_taxi_trips`

### Kafka
- **Topic:** `nyc_taxi_raw`

### Target: Snowflake
- **Database:** `NYC_TAXI_PROJECT`
- **Schema:** `CLEAN`
- **Table:** `YELLOW_TAXI_CLEAN`

**Target Columns:**
- `VENDOR_ID`
- `PICKUP_TIME`
- `DROPOFF_TIME`
- `PASSENGER_COUNT`
- `TRIP_DISTANCE`
- `PICKUP_LOCATION`
- `DROPOFF_LOCATION`
- `PAYMENT_TYPE`
- `FARE_AMOUNT`
- `TOTAL_AMOUNT`

---

## 📂 Project Folder Structure

