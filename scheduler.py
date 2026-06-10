

from drone import Drone, DroneStatus
from graph import Graph
from zone import Zone, ZoneType


class Scheduler:
    def schedule_turn(self, drones: list[Drone],
                      graph: Graph) -> dict[Drone, Zone]:
        reservations: dict[Zone, int] = {}
        movements: dict[Drone, Zone] = {}

        for drone in drones:
            if drone.status == DroneStatus.DELIVERED:
                continue
            if drone.status == DroneStatus.IN_TRANSIT:
                if drone.next_zone is None:
                    continue

                reservations[drone.next_zone] = reservations.get(
                    drone.next_zone, 0) + 1
                movements[drone] = drone.next_zone
                continue
            if not drone.path:
                continue
            next_zone = drone.path[0]

            current_count = reservations.get(next_zone, 0)
            if current_count >= next_zone.max_drones:
                continue

            connection = graph.get_connections(drone.current_zone, next_zone)
            if connection and connection.max_link_capacity <= current_count:
                continue

            reservations[next_zone] = current_count + 1
            movements[drone] = next_zone

            if next_zone.zone_type == ZoneType.RESTRICTED:
                drone.status = DroneStatus.IN_TRANSIT
                drone.next_zone = next_zone
        return movements
