

from models.drone import Drone, DroneStatus
from models.graph import Graph


class Simulator:
	def __init__(self, graph: Graph, drones: list[Drone]):
		self.graph = graph
		self.drones = drones
		self.turn = 0

	def run(self):
		while not self.all_delivered():
			self.process_turn()
			self.turn += 1

	def process_turn(self):
		movements = []
		for drone in self.drones:
			if drone.status.value == "DELIVERED":
				continue

			move = self.move_drone(drone)

			if move:
				movements.append(move)
		self.print_turn(movements)

	def move_drone(self, drone: Drone) -> str | None:
		next_zone = drone.path[0] if drone.path else None
		if not next_zone:
			drone.status = DroneStatus.DELIVERED
			return None

	def all_delivered(self) -> bool:
		return all(drone.status.value == "DELIVERED" for drone in self.drones)

	def print_turn(self, movements: list[str]):
		print(" ".join(movements))
