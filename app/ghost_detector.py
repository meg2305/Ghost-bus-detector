import time


class GhostDetector:
    def __init__(self, stale_threshold: int = 600):
        """
        Initialize the GhostDetector.

        Args:
            stale_threshold (int): Number of seconds a bus can remain at the
                                   same location before it is flagged as a "ghost".
                                   Default = 600s (10 minutes).
        """
        self.stale_threshold = stale_threshold
        self.vehicle_states = {}  # {vehicle_id: {"lat": ..., "lon": ..., "last_seen": ..., "updates": ...}}

    def update(self, vehicles):
        """
        Update the detector with the latest list of vehicles.

        Args:
            vehicles (list of dict): Each dict should have {"id", "lat", "lon"}.

        Returns:
            list: Vehicles flagged as "ghosts".
        """
        ghosts = []  # list of ghost buses
        current_time = int(time.time())  # current timestamp in seconds

        for v in vehicles:
            vid = v["id"]
            lat, lon = v["lat"], v["lon"]

            # First time seeing this vehicle → initialize state
            if vid not in self.vehicle_states:
                self.vehicle_states[vid] = {
                    "lat": lat,
                    "lon": lon,
                    "last_seen": current_time,
                    "updates": 1
                }
            else:
                # Already seen before → update state
                state = self.vehicle_states[vid]
                state["updates"] += 1

                if state["lat"] == lat and state["lon"] == lon:
                    # same position as before → check staleness
                    if current_time - state["last_seen"] > self.stale_threshold:
                        ghosts.append(v)
                else:
                    # vehicle moved → update position + timestamp
                    state["lat"], state["lon"] = lat, lon
                    state["last_seen"] = current_time

        # Find vehicles that only appeared once (never updated again)
        for vid, state in self.vehicle_states.items():
            if state["updates"] == 1 and current_time - state["last_seen"] > self.stale_threshold:
                ghosts.append({"id": vid, "reason": "one-time ghost"})

        return ghosts
