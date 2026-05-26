from .zone import Zone


class Connection:

    def __init__(self, zone_a: Zone, zone_b: Zone, max_link_capacity: int):
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity

    def other(self, zone: Zone) -> Zone:
        if zone == self.zone_a:
            return self.zone_b
        elif zone == self.zone_b:
            return self.zone_a
        else:
            raise ValueError("Zone not part of this connection")
