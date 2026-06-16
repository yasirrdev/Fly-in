from drone import Drone, DroneStatus
from graph import Graph
from zone import Zone, ZoneType


class Scheduler:
    def schedule_turn(self, drones: list[Drone],
                      graph: Graph) -> dict[Drone, Zone]:
        """Schedule drone movements for a single turn while respecting
        capacities."""
        reservations: dict[Zone, int] = {}
        movements: dict[Drone, Zone] = {}

        for drone in drones:
            if drone.status != DroneStatus.DELIVERED:
                z = drone.current_zone
                if z != graph.start and z != graph.end:
                    reservations[z] = reservations.get(z, 0) + 1

        for drone in drones:
            if drone.status == DroneStatus.DELIVERED:
                continue

            if drone.status == DroneStatus.IN_TRANSIT:
                if drone.next_zone is None:
                    continue
                movements[drone] = drone.next_zone
                continue

            if not drone.path:
                continue

            next_zone = drone.path[0]
            current_count = reservations.get(next_zone, 0)

            if (next_zone != graph.end
                    and current_count >= next_zone.max_drones):
                continue

            conn = graph.get_connections(drone.current_zone, next_zone)
            if conn and conn.max_link_capacity <= current_count:
                continue

            if (drone.current_zone != graph.start
                    and drone.current_zone != graph.end):
                reservations[drone.current_zone] -= 1
            reservations[next_zone] = current_count + 1
            movements[drone] = next_zone

            if next_zone.zone_type == ZoneType.RESTRICTED:
                drone.status = DroneStatus.IN_TRANSIT
                drone.next_zone = next_zone

        return movements
