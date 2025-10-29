from google.transit import gtfs_realtime_pb2
import logging

logger = logging.getLogger(__name__)

def parse_feed(raw_data: bytes):
    """
    Parse GTFS-Realtime protobuf bytes into a list of structured vehicle objects.

    Args:
        raw_data (bytes): Raw GTFS-Realtime protobuf data from the feed.

    Returns:
        list[dict]: A list of vehicles, where each vehicle is represented as a dictionary:
            {
                "id": str,            # Unique entity ID (from GTFS feed)
                "trip_id": str,       # Associated trip identifier
                "route_id": str,      # Route identifier
                "lat": float,         # Vehicle latitude
                "lon": float,         # Vehicle longitude
                "timestamp": int,     # Last update timestamp (epoch)
                "status": int | None  # Vehicle status (if present)
            }
    """
    # Create FeedMessage object and parse the protobuf data
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(raw_data)

    vehicles = []

    # Iterate through entities in the GTFS feed
    for entity in feed.entity:
        if entity.HasField("vehicle"):  # We check if entity.HasField("vehicle") to keep only vehicle positions.
            vehicle = entity.vehicle
            vehicles.append({
                "id": entity.id,
                "trip_id": vehicle.trip.trip_id if vehicle.trip else None,
                "route_id": vehicle.trip.route_id if vehicle.trip else None,
                "lat": vehicle.position.latitude if vehicle.position else None,
                "lon": vehicle.position.longitude if vehicle.position else None,
                "timestamp": vehicle.timestamp if vehicle.timestamp else None,
                "status": vehicle.current_status if vehicle.HasField("current_status") else None,
            })

    # Logs how many vehicles were parsed for debugging.
    logger.info(f"Parsed {len(vehicles)} vehicles from GTFS feed")
    return vehicles
