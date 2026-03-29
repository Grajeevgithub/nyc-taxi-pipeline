from datetime import datetime

def to_epoch(dt_value):
    """
    Convert datetime / string datetime to epoch milliseconds
    """
    if isinstance(dt_value, datetime):
        return int(dt_value.timestamp() * 1000)
    return int(datetime.fromisoformat(str(dt_value)).timestamp() * 1000)


def clean_record(record: dict):
    try:
        required_fields = [
            "vendor_id",
            "pickup_datetime",
            "dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "pickup_location_id",
            "dropoff_location_id",
            "payment_type",
            "fare_amount",
            "total_amount"
        ]

        for field in required_fields:
            if field not in record or record[field] is None:
                return None

        pickup_epoch = to_epoch(record["pickup_datetime"])
        dropoff_epoch = to_epoch(record["dropoff_datetime"])

        if dropoff_epoch <= pickup_epoch:
            return None

        passenger_count = int(record["passenger_count"])
        trip_distance = float(record["trip_distance"])
        fare_amount = float(record["fare_amount"])
        total_amount = float(record["total_amount"])

        if passenger_count <= 0 or passenger_count > 6:
            return None
        if trip_distance <= 0:
            return None
        if fare_amount < 0 or total_amount <= 0:
            return None

        return {
            "VENDOR_ID": int(record["vendor_id"]),
            "PICKUP_TIME": pickup_epoch,
            "DROPOFF_TIME": dropoff_epoch,
            "PASSENGER_COUNT": passenger_count,
            "TRIP_DISTANCE": trip_distance,
            "PICKUP_LOCATION": int(record["pickup_location_id"]),
            "DROPOFF_LOCATION": int(record["dropoff_location_id"]),
            "PAYMENT_TYPE": int(record["payment_type"]),
            "FARE_AMOUNT": fare_amount,
            "TOTAL_AMOUNT": total_amount
        }

    except Exception:
        return None
