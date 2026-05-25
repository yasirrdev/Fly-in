from enum import Enum


class ZoneType(Enum):
    NORMAL = "NORMAL"
    RESTRICTED = "RESTRICTED"
    PRIORITY = "PRIORITY"
    BLOCKED = "BLOCKED"


class Zone:
    def __init__(self, name: str, x: int, y: int,
                 zone_type: ZoneType, color: str, max_drones: int):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = ZoneType.NORMAL
        self.color = ""
        self.max_drones = 1

    def movement_cost(self) -> int:
        if self.zone_type == ZoneType.RESTRICTED:
            return 2
        else:
            return 1

    def is_passable(self) -> bool:
        return self.zone_type != ZoneType.BLOCKED
