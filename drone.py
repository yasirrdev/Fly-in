from enum import Enum
from zone import Zone


class DroneStatus(Enum):
    WAITING = "WAITING"
    MOVING = "MOVING"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"


class Drone:
    def __init__(self, drone_id: int, current_zone: Zone, status: DroneStatus,
                 path: list[Zone], turns_remaining: int,
                 next_zone: Zone | None = None):
        self.drone_id = drone_id
        self.current_zone = current_zone
        self.status = status
        self.path = path
        self.turns_remaining = turns_remaining
        self.next_zone = next_zone
