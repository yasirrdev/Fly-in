import heapq
from models.graph import Graph
from models.zone import Zone


class PathFinder:

    def find_path(self, graph: Graph, start: Zone,
                  end: Zone) -> list[Zone]:
        dist: dict[Zone, float] = {
            zone: float('inf') for zone in graph.zones.values()}
        dist[start] = 0
        previous: dict[Zone, Zone | None] = {
            zone: None for zone in graph.zones.values()}

        counter = 0
        heap = [(0, counter, start)]
        while heap:
            cost, _, zone = heapq.heappop(heap)
            if zone == end:
                break
            if cost > dist[zone]:
                continue
            for neighbor in graph.get_neighbors(zone):
                new_cost = cost + neighbor.movement_cost()
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    previous[neighbor] = zone
                    counter += 1
                    heapq.heappush(heap, (new_cost, counter, neighbor))
        path = []
        current: Zone | None = end
        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()
        if path[0] != start:
            return []
        return path
