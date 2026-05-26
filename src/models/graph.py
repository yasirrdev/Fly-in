from .connection import Connection
from .zone import Zone


class Graph:
    def __init__(
        self,
        zones: dict[str, Zone],
        connections: list[Connection],
        start: Zone,
        end: Zone,
    ):
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Zone | None = None
        self.end: Zone | None = None

    def add_zone(self, zone: Zone):
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection):
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
