import csv
import time
import heapq
import random
from sys import argv
from math import ceil, floor
import networkx as nx
import heapq
from collections import deque, defaultdict, Counter
from transitions import Machine
from typing import List, Dict, Any
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor


@dataclass(order=True)
class Event:
    t: int
    action: str
    spaces: Dict[str, Any] = field(compare=False)

class Grid:
    def __init__(self, width=4, height=4, min_weight=1, max_weight=10, alpha=0.9):
        self.width = width
        self.height = height
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.alpha = alpha
        self.graph = nx.DiGraph()
        self.zones = {}
        self.queues = defaultdict(int)
        self.priorities = defaultdict(int)
        self.create_graph()
        self.create_zones()
        self.precompute_shortest_paths()

    def create_graph(self):
        for i in range(self.width):
            for j in range(self.height):
                self.graph.add_node((i, j))
        for i in range(self.width):
            for j in range(self.height - 1):
                weight_1 = random.randint(self.min_weight, self.max_weight)
                weight_2 = random.randint(self.min_weight, self.max_weight)
                self.graph.add_edge((i, j), (i, j + 1), weight=weight_1)
                self.graph.add_edge((i, j + 1), (i, j), weight=weight_2)
                weight_3 = random.randint(self.min_weight, self.max_weight)
                weight_4 = random.randint(self.min_weight, self.max_weight)
                self.graph.add_edge((j, i), (j + 1, i), weight=weight_3)
                self.graph.add_edge((j + 1, i), (j, i), weight=weight_4)

    def create_zones(self):
        self.zones = {(i, j): Zone(i, j) for i in range(self.width) for j in range(self.height)}

    def precompute_shortest_paths(self):
        self.shortest_paths = dict(nx.all_pairs_dijkstra_path_length(self.graph, weight='weight'))

    def update_priorities(self):
        for node in self.graph.nodes:
            self.priorities[node] = self.alpha * self.priorities[node] + self.queues[node]      

class Zone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = f"Zone ({x},{y})"
        self.queue_length = 0

    def __str__(self):
        return f"Zone ({self.x},{self.y})"

    def update_queue(self, length):
        self.queue_length = length

class Simulation:
    def __init__(self, riders, drivers, ride_requests, grid):
        self.riders = riders
        self.drivers = drivers
        self.ride_requests = ride_requests
        self.grid = grid
        self.completed_rides = []
        self.state_map = StateMap()

    def calculate_cost(self, zone1, zone2):
        try:
            distance = self.grid.shortest_paths[(zone1.x, zone1.y)][(zone2.x, zone2.y)]
        except KeyError as e:
            print(f"KeyError: {e} - Zone1: {zone1}, Zone2: {zone2}")
            raise e
        priority = self.grid.priorities[(zone2.x, zone2.y)]
        lambda_factor = 1 
        return distance + lambda_factor * priority
    
    def calculate_travel_time(self, zone1, zone2):
        try:
            return self.grid.shortest_paths[(zone1.x, zone1.y)][(zone2.x, zone2.y)]
        except KeyError:
            return float('inf')

    def handle_ride_request_event(self, event, event_queue, current_time, retry_queue):
        ride_id = event.spaces["ride_id"]
        ride_request = self.ride_requests[ride_id]
        print(f"Handling ride request event for ride {ride_id} at time {current_time}")

        for driver in self.drivers:
            if driver.state == 'idle' and driver.will_accept_ride(ride_request.metadata):
                travel_time = self.calculate_travel_time(driver.zone, ride_request.origin_zone)
                try:
                    cost = self.calculate_cost(driver.zone, ride_request.origin_zone)
                except KeyError as e:
                    print(f"KeyError: {e} - Driver Zone: {driver.zone}, Origin Zone: {ride_request.origin_zone}")
                    retry_queue.append(Event(t=current_time + 1, action="Request Ride", spaces={"ride_id": ride_id, "retry_count": event.spaces.get("retry_count", 0) + 1}))
                    return
                
                print(f"Travel time: {travel_time}, Cost: {cost}")
                if travel_time < float('inf'):
                    driver.zone = ride_request.origin_zone
                    driver.time_to_next_zone = travel_time
                    driver.current_rider = ride_request.rider
                    driver.current_request = ride_request
                    driver.accept_ride()
                    ride_request.driver = driver
                    ride_request.accept()
                    ride_request.rider.match_with_driver()
                    ride_request.rider.estimated_wait_time = travel_time
                    ride_request.metadata["pickup_time"] = current_time + travel_time
                    heapq.heappush(event_queue, Event(t=current_time + travel_time, action="Driver Assigned", spaces={"ride_id": ride_id, "driver_id": driver.name}))
                    print(f"{driver.name} assigned to ride {ride_id} at time {current_time + travel_time}")
                    return
    
        print(f"No driver available for ride {ride_id} at time {current_time}, retrying...")
        ride_request.increase_cost()
        retry_queue.append(Event(t=current_time + 1, action="Request Ride", spaces={"ride_id": ride_id}))

    def handle_driver_assigned_event(self, event, event_queue, current_time):
        ride_id = event.spaces["ride_id"]
        driver_id = event.spaces["driver_id"]
        ride_request = self.ride_requests[ride_id]
        driver = next(d for d in self.drivers if d.name == driver_id)
        print(f"{driver_id} arrived at pickup for {ride_id} at time {current_time}")

        driver.arrive_at_pickup()
        driver.pick_up_rider()
        ride_request.start()
        ride_request.rider.start_ride()
        travel_time = self.calculate_travel_time(driver.zone, ride_request.destination_zone)
        driver.time_to_next_zone = travel_time
        ride_request.metadata["dropoff_time"] = current_time + travel_time
        heapq.heappush(event_queue, Event(t=current_time + travel_time, action="Complete Ride", spaces={"ride_id": ride_id, "driver_id": driver.name}))
        print(f"Ride {ride_id} in progress, will complete at time {current_time + travel_time}")

    def handle_complete_ride_event(self, event, current_time):
        
        ride_id = event.spaces["ride_id"]
        driver_id = event.spaces["driver_id"]
        ride_request = self.ride_requests[ride_id]
        driver = next(d for d in self.drivers if d.name == driver_id)
        print(f"Completing ride {ride_id} by driver {driver_id} at time {current_time}")

        driver.complete_ride()
        ride_request.complete()
        ride_request.rider.complete_ride()
        ride_request.metadata["dropoff_time"] = current_time
        driver.zone = ride_request.destination_zone  # Update driver's zone to the destination
        driver.current_rider = None
        driver.current_request = None
        driver.reset()

        self.completed_rides.append(ride_request)
        print(f"Ride {ride_id} completed")
        
    def record_state(self, current_time):
        completed_rides = len(self.completed_rides)
        total_distance = sum([ride.metadata['distance_km'] for ride in self.completed_rides])
        total_cost = sum([ride.metadata['cost_usd'] for ride in self.completed_rides])
        self.state_map.record_state(current_time, completed_rides, total_distance, total_cost)

class Driver:
    states = ['idle', 'en_route', 'waiting_for_rider', 'in_ride', 'ride_completed']

    def __init__(self, name, zone, preferences):
        self.name = name
        self.zone = zone
        self.preferences = preferences
        self.time_to_next_zone = 0
        self.current_rider = None
        self.current_request = None
        self.machine = Machine(model=self, states=Driver.states, initial='idle')
        self.machine.add_transition('accept_ride', 'idle', 'en_route')
        self.machine.add_transition('arrive_at_pickup', 'en_route', 'waiting_for_rider')
        self.machine.add_transition('pick_up_rider', 'waiting_for_rider', 'in_ride')
        self.machine.add_transition('complete_ride', 'in_ride', 'ride_completed')
        self.machine.add_transition('reset', '*', 'idle')

    def calculate_acceptance_threshold(self, ride_metadata):
        threshold = (
            ride_metadata['cost_usd'] * self.preferences['cost_weight'] +
            ride_metadata['distance_km'] * self.preferences['distance_weight'] +
            ride_metadata['duration_min'] * self.preferences['duration_weight'] +
            ride_metadata['driver_rating'] * self.preferences['driver_rating_weight'] +
            ride_metadata['rider_rating'] * self.preferences['rider_rating_weight']
        )
        return threshold

    def will_accept_ride(self, ride_metadata):
        acceptance_threshold = self.calculate_acceptance_threshold(ride_metadata)
        return acceptance_threshold >= self.preferences['acceptance_threshold']

class Rider:
    states = ['waiting', 'matched', 'in_ride', 'ride_completed', 'ride_canceled']

    def __init__(self, name, zone):
        self.name = name
        self.zone = zone
        self.estimated_wait_time = 0
        self.machine = Machine(model=self, states=Rider.states, initial='waiting')
        self.machine.add_transition('match_with_driver', 'waiting', 'matched')
        self.machine.add_transition('start_ride', 'matched', 'in_ride')
        self.machine.add_transition('complete_ride', 'in_ride', 'ride_completed')
        self.machine.add_transition('cancel_ride', '*', 'ride_canceled')

class RideRequest:
    states = ['requested', 'accepted', 'in_progress', 'completed', 'canceled']

    def __init__(self, ride_id, rider, origin_zone, destination_zone, grid):
        self.ride_id = ride_id
        self.rider = rider
        self.origin_zone = origin_zone
        self.destination_zone = destination_zone
        self.grid = grid
        self.metadata = self.generate_metadata()
        self.driver = None
        self.machine = Machine(model=self, states=RideRequest.states, initial='requested')
        self.machine.add_transition('accept', 'requested', 'accepted')
        self.machine.add_transition('start', 'accepted', 'in_progress')
        self.machine.add_transition('complete', 'in_progress', 'completed')
        self.machine.add_transition('cancel', '*', 'canceled')

    def generate_metadata(self):
        driver_to_pickup = self.calculate_travel_time(self.origin_zone, self.origin_zone)
        pickup_to_destination = self.calculate_travel_time(self.origin_zone, self.destination_zone)
        total_distance = driver_to_pickup + pickup_to_destination
        duration = total_distance
        cost = total_distance * 2.5
        return {
            "distance_km": total_distance,
            "duration_min": duration,
            "pickup_time": None,
            "dropoff_time": None,
            "cost_usd": round(cost, 2),
            "driver_rating": round(random.uniform(4.0, 5.0), 2),
            "rider_rating": round(random.uniform(4.0, 5.0), 2),
            "ride_type": random.choice(["economy", "premium", "pool"]),
            "traffic_conditions": random.choice(["normal", "heavy", "light"]),
            "weather_conditions": random.choice(["clear", "rainy", "stormy", "snowy"]),
        }

    def calculate_travel_time(self, zone1, zone2):
        try:
            return self.grid.shortest_paths[(zone1.x, zone1.y)][(zone2.x, zone2.y)]
        except KeyError:
            return float('inf')
        
    def increase_cost(self, increment=15):
        """
        Increase the cost of the ride by a fixed amount (default is 5 units).
        """
        self.metadata['cost_usd'] += increment
        print(f"Cost increased to {self.metadata['cost_usd']} for ride {self.ride_id}")
        
class StateMap:
    def __init__(self):
        self.states = []

    def record_state(self, current_time, completed_rides, total_distance, total_cost):
        state = {
            "time": current_time,
            "completed_rides": completed_rides,
            "total_distance": total_distance,
            "total_cost": total_cost
        }
        self.states.append(state)

    def print_state_map(self):
        for state in self.states:
            print(f"Time: {state['time']}, Completed Rides: {state['completed_rides']}, Total Distance: {state['total_distance']}, Total Cost: {state['total_cost']}")

    def write_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['time', 'completed_rides', 'total_distance', 'total_cost']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for state in self.states:
                writer.writerow(state)

def initialize_event_queue(ride_requests) -> List[Event]:

    initial_events = []
    start_time_counter = Counter()

    for ride_id in ride_requests:
        start_time = random.randint(1, len(ride_requests))
        start_time_counter[start_time] += 1
        initial_events.append(Event(t=start_time, action="Request Ride", spaces={"ride_id": ride_id}))
    for _, count in list(start_time_counter.items()):
        if count > 10:
            start_time_counter[start_time] = 10
            
    heapq.heapify(initial_events)

    return initial_events
    
def process_events(event_queue, simulation):
    current_time = 0
    retry_queue = deque()

    while event_queue or retry_queue:
        while event_queue and event_queue[0].t == current_time:
            current_event = heapq.heappop(event_queue)
            handle_event(current_event, event_queue, simulation, retry_queue, current_time)
        while retry_queue and retry_queue[0].t <= current_time:
            current_event = retry_queue.popleft()
            handle_event(current_event, event_queue, simulation, retry_queue, current_time)
        
        # Record the state at each time step
        simulation.record_state(current_time)
        current_time += 1
        simulation.grid.update_priorities()
    
def handle_event(event, event_queue, simulation, retry_queue, current_time):
    print(f"Processing event: {event} at time {current_time}")

    if event.action == "Request Ride":
        simulation.handle_ride_request_event(event, event_queue, current_time, retry_queue)
    elif event.action == "Driver Assigned":
        simulation.handle_driver_assigned_event(event, event_queue, current_time)
    elif event.action == "Complete Ride":
        print(f"\nEvent: {event}\n")
        simulation.handle_complete_ride_event(event, current_time)
    else:
        print(f"Unknown event action: {event.action}")

def adjust_inputs(seed=0, upper_limit=1000):
    random.seed(time.time())
    increase_factor = 1 + (max(0, min(seed, 100)) / 100) * 500
    random_factor = lambda: random.uniform(0.9, 1.1)

    grid_width = ceil(4 * increase_factor * random_factor())
    grid_height = ceil(4 * increase_factor * random_factor())
    num_riders = ceil(4 * increase_factor * random_factor())

    num_drivers = max(1, min(num_riders + random.randint(-100, -1), upper_limit))

    grid_width = max(2, min(grid_width, 15))
    grid_height = max(2, min(grid_height, 15))
    num_riders = max(1, min(num_riders, upper_limit))
    num_drivers = max(1, min(num_drivers, num_riders - 1))

    grid = Grid(width=grid_width, height=grid_height)
    
    riders = [Rider(f'Rider {i}', random.choice(list(grid.zones.values()))) for i in range(num_riders)]
    drivers = [Driver(f'Driver {i}', random.choice(list(grid.zones.values())), {
        "cost_weight": 0.4, "distance_weight": 0.1, "duration_weight": 0.1,
        "driver_rating_weight": 0.2, "rider_rating_weight": 0.2, "acceptance_threshold": 20
    }) for i in range(floor(num_drivers / 4))]

    ride_requests = {
        i + 1: RideRequest(i + 1, riders[i], random.choice(list(grid.zones.values())), random.choice(list(grid.zones.values())), grid)
        for i in range(num_riders)
    }

    return grid, riders, drivers, ride_requests

if __name__ == "__main__":
    if len(argv) == 2:
        upper_limit = int(argv[1])
    elif len(argv) == 3:
        upper_limit = int(argv[1])
        file_path = argv[2]
    elif len(argv) == 4:
        seed = int(argv[1])
        upper_limit = int(argv[2])
        file_path = argv[3]
    else:
        seed = 100
        upper_limit = 75000
        file_path = "/Users/sayertindall/Documents/GitHub/block.science/rideshare/research/DataViews/ResultsTracker2.csv"
    
    random.seed(42)
    
    grid, riders, drivers, ride_requests = adjust_inputs(seed, upper_limit)
    
    print("Grid dimensions:", grid.width, grid.height)
    print("Number of Zones:", len(grid.zones))
    print("Number of Nodes:", str(grid.graph.number_of_nodes()))
    print("Number of Edges:", str(grid.graph.number_of_edges()))
    print("Number of Riders:", len(riders))
    print("Number of Drivers:", len(drivers))
    print("Number of Ride Requests:", len(ride_requests))
    print("\n")
    
    event_queue = initialize_event_queue(ride_requests)
    simulation = Simulation(riders, drivers, ride_requests, grid)

    process_events(event_queue, simulation)
    
    # simulation.state_map.write_to_csv('state_map_dipr.csv')

    if len(ride_requests) == len(simulation.completed_rides):
        print("Verification successful: All ride requests were completed.")
    else:
        print(f"Verification failed: {len(ride_requests)} requests, {len(simulation.completed_rides)} completed.")