*This project has been created as part of the 42 curriculum by ybel-maa.*

# Fly-in

## Description

Fly-in is a drone routing simulation system that navigates a fleet of drones through a network of connected zones, from a start hub to an end hub, in the minimum number of simulation turns. The system reads a map file describing the zone graph, computes optimal paths using a custom Dijkstra implementation, and simulates turn-by-turn movement while respecting all capacity and movement constraints.

Key features:
- Custom graph implementation (no external graph libraries)
- Dijkstra-based pathfinding with weighted zone types
- Multi-path distribution across available routes
- Turn-by-turn simulation with zone and connection capacity enforcement
- Full support for restricted zones (2-turn movement)
- Colored terminal output

## Instructions

### Installation

```bash
make install
```

### Running

```bash
make run MAP=maps/easy/01_linear_path.txt
```

### Debug mode

```bash
make debug MAP=maps/easy/01_linear_path.txt
```

### Lint

```bash
make lint
```

### Clean

```bash
make clean
```

## Map Format

```
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
connection: hub-roof1
connection: corridorA-tunnelB [max_link_capacity=2]
```

Zone types: `normal` (1 turn), `restricted` (2 turns), `priority` (1 turn, preferred), `blocked` (inaccessible).

## Algorithm

### Pathfinding

A manual Dijkstra implementation using Python's `heapq` module. Each zone has a movement cost based on its type (1 for normal/priority, 2 for restricted). The priority queue uses `(cost, counter, zone)` tuples to avoid direct zone comparisons. Multiple paths are discovered by temporarily penalizing intermediate zones of already-found paths, forcing Dijkstra to explore alternative routes and distribute drones across them.

### Scheduling

The `Scheduler` processes all drones each turn simultaneously. It maintains a reservation table (`dict[Zone, int]`) tracking how many drones are heading to each zone in the current turn. For each drone, it validates zone capacity (`max_drones`) and connection capacity (`max_link_capacity`) before confirming movement. Drones heading toward restricted zones are marked `IN_TRANSIT` and must complete their 2-turn movement without interruption. Conflict resolution uses drone ID order as a tiebreaker to prevent deadlocks.

### Simulation

The `Simulator` runs a turn loop until all drones reach the end zone. Each turn it calls the scheduler, applies confirmed movements, updates drone states, and outputs the turn result in the required format (`D1-zone D2-zone ...`).

## Visualization

Terminal output uses ANSI escape codes to colorize each drone movement according to its destination zone's color attribute defined in the map file. Supported colors: red, green, yellow, blue, orange, gray. Zones with no color defined are displayed without formatting. This allows quick visual identification of drone positions and zone states during simulation playback.

## Performance Benchmarks

| Map | Drones | Turns | Target |
|-----|--------|-------|--------|
| Easy: linear path | 2 | 4 | ≤ 6 |
| Easy: simple fork | 4 | 6 | ≤ 8 |
| Easy: basic capacity | 4 | 4 | ≤ 6 |
| Medium: dead end trap | 5 | 8 | ≤ 12 |
| Medium: circular loop | 6 | 9 | ≤ 15 |
| Medium: priority puzzle | 5 | 8 | ≤ 12 |
| Hard: maze nightmare | 8 | 13 | ≤ 30 |
| Hard: capacity hell | 12 | 16 | ≤ 35 |
| Hard: ultimate challenge | 15 | 26 | ≤ 45 |

## Resources

- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python heapq documentation](https://docs.python.org/3/library/heapq.html)
- [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)

### AI Usage

Claude (Anthropic) was used as a step-by-step guide throughout the project. AI assisted with: architecture design decisions, identifying bugs in type annotations and constructor assignments, explaining algorithm structure (Dijkstra, reservation tables), and reviewing code between implementation steps. All code was written and understood independently — AI was never used to generate complete implementations directly.