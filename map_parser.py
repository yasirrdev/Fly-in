
from graph import Graph
from zone import Zone, ZoneType
from connection import Connection


class MapParser:

    def _split_metadata(self, line: str) -> tuple[str, dict[str, str]]:
        """Extract the main token and metadata key/value pairs from a line."""
        metadata: dict[str, str] = {}
        if '[' in line and line.endswith(']'):
            main = line[:line.index('[')].strip()
            raw = line[line.index('[') + 1:line.index(']')].strip()
            for token in raw.split():
                key, _, value = token.partition('=')
                metadata[key] = value
        else:
            main = line.strip()
        return main, metadata

    def _parse_connection(self, line: str, graph: Graph) -> Connection:
        """Parse a connection line into a Connection object."""
        main, metadata = self._split_metadata(line)
        names = main.removeprefix('connection:').strip().split('-')
        zone_a = graph.zones[names[0].strip()]
        zone_b = graph.zones[names[1].strip()]
        max_link_capacity = int(metadata.get('max_link_capacity', '1'))
        return Connection(zone_a, zone_b, max_link_capacity)

    def _parse_zone(self, line: str, prefix: str) -> Zone:
        """Parse a zone definition line into a Zone object."""
        main, metadata = self._split_metadata(line)
        parts = main.removeprefix(prefix).strip().split()
        name, x, y = parts[0], int(parts[1]), int(parts[2])
        zone_type = ZoneType[metadata.get('zone', 'NORMAL').upper()]
        color = metadata.get('color', '')
        max_drones = int(metadata.get('max_drones', '1'))
        return Zone(name, x, y, zone_type, color, max_drones)

    def parse(self, filepath: str) -> tuple[Graph, int]:
        """Parse a map file and return the resulting graph and drone count."""
        graph = Graph()
        nb_drones = 0

        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('nb_drones:'):
                    nb_drones = int(line.split()[1])
                elif line.startswith('start_hub:'):
                    start = self._parse_zone(line, 'start_hub:')
                    graph.add_zone(start)
                    graph.start = start
                elif line.startswith('end_hub:'):
                    end = self._parse_zone(line, 'end_hub:')
                    graph.add_zone(end)
                    graph.end = end
                elif line.startswith('hub:'):
                    zone = self._parse_zone(line, 'hub:')
                    graph.add_zone(zone)
                elif line.startswith('connection:'):
                    connection = self._parse_connection(line, graph)
                    graph.add_connection(connection)
                else:
                    raise ValueError(f"Invalid line {line_num}: {line}")
        return graph, nb_drones
