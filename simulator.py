from drone import Drone, DroneStatus
from graph import Graph
from scheduler import Scheduler
from terminal import TerminalVisualization


class Simulator:
    def __init__(self, graph: Graph, drones: list[Drone]) -> None:
        """Initialize the simulator with the graph and set of drones."""
        self.graph = graph
        self.terminal = TerminalVisualization()
        self.drones = drones
        self.turn = 0
        self.scheduler = Scheduler()

    def run(self) -> None:
        """Run simulation turns until all drones have completed delivery."""
        while not self.all_delivered():
            self.process_turn()
            self.turn += 1
        self._print_summary()

    def _print_summary(self) -> None:
        """Print a summary of the simulation results."""
        print(f"\n{'='*40}")
        print("  Simulation complete!")
        print(f"  Total turns   : {self.turn}")
        print(f"  Drones routed : {len(self.drones)}")
        print(f"{'='*40}")

    def process_turn(self) -> None:
        """Process a single turn by scheduling movements and updating
        drone states."""
        movements = self.scheduler.schedule_turn(self.drones, self.graph)
        output = []

        for drone, next_zone in movements.items():
            if drone.status == DroneStatus.IN_TRANSIT:
                conn_name = f"{drone.current_zone.name}-{next_zone.name}"
                output.append(self.terminal.colorize(
                    f"D{drone.drone_id}-{conn_name}", next_zone.color))
            else:
                output.append(self.terminal.colorize(
                    f"D{drone.drone_id}-{next_zone.name}", next_zone.color))

            drone.current_zone = next_zone
            if drone.path and drone.path[0] == next_zone:
                drone.path.pop(0)
            if next_zone == self.graph.end:
                drone.status = DroneStatus.DELIVERED
            elif drone.status == DroneStatus.IN_TRANSIT:
                drone.status = DroneStatus.MOVING
                drone.next_zone = None

        if output:
            print(f"Turn {self.turn + 1}: {' '.join(output)}")

    def all_delivered(self) -> bool:
        """Return True when every drone has reached the delivered status."""
        return all(
            drone.status == DroneStatus.DELIVERED for drone in self.drones)
