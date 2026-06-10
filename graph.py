from connection import Connection
from zone import Zone


class Graph:
    def __init__(self) -> None:
        """Initialize an empty graph with zone and connection storage."""
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.start: Zone | None = None
        self.end: Zone | None = None

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the graph indexed by its name."""
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        """Add a connection to the graph."""
        self.connections.append(connection)

    def get_connections(self, z1: Zone, z2: Zone) -> Connection | None:
        """Return the connection between two zones if one exists."""
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
        """Return all passable neighboring zones connected to the
        provided zone."""
        neighbors = []
        for connection in self.connections:
            if connection.zone_a == zone:
                neighbors.append(connection.zone_b)
            elif connection.zone_b == zone:
                neighbors.append(connection.zone_a)
        return [z for z in neighbors if z.is_passable()]
