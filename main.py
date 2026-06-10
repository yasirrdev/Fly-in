import sys
from drone import Drone, DroneStatus
from map_parser import MapParser
from pathfinder import PathFinder
from simulator import Simulator


def main() -> None:
    """Run the delivery simulation using a map file provided via command-line.

    Exits with an error message if the map file is missing or invalid.
    """

    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        sys.exit(1)

    parser = MapParser()
    graph, nb_drones = parser.parse(sys.argv[1])

    if graph.start is None or graph.end is None:
        print("Error: map must have a start and end zone")
        sys.exit(1)

    drones = [
        Drone(i + 1, graph.start, DroneStatus.WAITING, [], 0)
        for i in range(nb_drones)
    ]

    pathfinder = PathFinder()
    paths = pathfinder.find_all_paths(graph, graph.start, graph.end, nb_drones)

    if not paths:
        print("Error: no path found between start and end")
        sys.exit(1)

    for i, drone in enumerate(drones):
        drone.path = list(paths[i % len(paths)][1:])

    simulator = Simulator(graph, drones)
    simulator.run()


if __name__ == "__main__":
    main()
