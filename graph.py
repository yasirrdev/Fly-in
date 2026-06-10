from connection import Connection
from zone import Zone


class Graph:
    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Zone | None = None
        self.end: Zone | None = None

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)

    def get_connections(self, z1: Zone, z2: Zone) -> Connection | None:
        for connection in self.connections:
            if (
                connection.zone_a == z1
                and connection.zone_b == z2
            ) or (
                connection.zone_a == z2
                and connection.zone_b == z1
            ):
                return connection
        return None

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        neighbors = []
        for connection in self.connections:
            if connection.zone_a == zone:
                neighbors.append(connection.zone_b)
            elif connection.zone_b == zone:
                neighbors.append(connection.zone_a)
        return [z for z in neighbors if z.is_passable()]
