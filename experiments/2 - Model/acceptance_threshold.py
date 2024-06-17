import random
from datetime import datetime, timedelta
from transitions import Machine

# Define a function to calculate Manhattan distance
def calculate_travel_time(zone1, zone2):
    return abs(zone1[0] - zone2[0]) + abs(zone1[1] - zone2[1])

# Define the Zone class
class Zone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = f"Zone ({x},{y})"
        self.traffic_state = "normal_traffic"  # Simplified traffic management

# Define the Driver class with state machine
class Driver:
    states = ['idle', 'en_route', 'waiting_for_rider', 'in_ride', 'ride_completed']

    def __init__(self, name, zone, preferences):
        self.name = name
        self.zone = zone
        self.preferences = preferences  # Driver's preferences for ride attributes
        self.time_to_next_zone = 0
        self.current_rider = None
        self.current_request = None
        self.machine = Machine(model=self, states=Driver.states, initial='idle')
        self.machine.add_transition('accept_ride', 'idle', 'en_route')
        self.machine.add_transition('arrive_at_pickup', 'en_route', 'waiting_for_rider')
        self.machine.add_transition('pick_up_rider', 'waiting_for_rider', 'in_ride')
        self.machine.add_transition('complete_ride', 'in_ride', 'ride_completed')
        self.machine.add_transition('reset', '*', 'idle')

    # Calculate acceptance threshold based on ride metadata and driver preferences
    def calculate_acceptance_threshold(self, ride_metadata):
        threshold = (
            ride_metadata['cost_usd'] * self.preferences['cost_weight'] +
            ride_metadata['distance_km'] * self.preferences['distance_weight'] +
            ride_metadata['duration_min'] * self.preferences['duration_weight'] +
            ride_metadata['driver_rating'] * self.preferences['driver_rating_weight'] +
            ride_metadata['rider_rating'] * self.preferences['rider_rating_weight']
        )
        return threshold

    # Determine if the driver accepts the ride based on the calculated threshold
    def will_accept_ride(self, ride_metadata):
        acceptance_threshold = self.calculate_acceptance_threshold(ride_metadata)
        return acceptance_threshold >= self.preferences['acceptance_threshold']

    def __str__(self):
        return f"{self.name} (State: {self.state}, Zone: {self.zone.name}, Time to next zone: {self.time_to_next_zone})"

# Define the Rider class with state machine
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

    def __str__(self):
        return f"{self.name} (State: {self.state}, Zone: {self.zone.name}, Estimated wait time: {self.estimated_wait_time})"

# Define the RideRequest class with state machine
class RideRequest:
    states = ['requested', 'accepted', 'in_progress', 'completed', 'canceled']

    def __init__(self, rider, origin_zone, destination_zone, driver_zone):
        self.rider = rider
        self.origin_zone = origin_zone
        self.destination_zone = destination_zone
        self.driver_zone = driver_zone
        self.metadata = self.generate_metadata()
        self.machine = Machine(model=self, states=RideRequest.states, initial='requested')
        self.machine.add_transition('accept', 'requested', 'accepted')
        self.machine.add_transition('start', 'accepted', 'in_progress')
        self.machine.add_transition('complete', 'in_progress', 'completed')
        self.machine.add_transition('cancel', '*', 'canceled')

    # Generate metadata for the ride request
    def generate_metadata(self):
        driver_to_pickup = calculate_travel_time((self.driver_zone.x, self.driver_zone.y), (self.origin_zone.x, self.origin_zone.y))
        pickup_to_destination = calculate_travel_time((self.origin_zone.x, self.origin_zone.y), (self.destination_zone.x, self.destination_zone.y))
        total_distance = driver_to_pickup + pickup_to_destination
        duration = total_distance  # 1 unit per zone
        cost = total_distance * 2.5  # Cost is based on the total distance with a multiplier
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

    def __str__(self):
        return f"RideRequest for {self.rider.name} (Origin: {self.origin_zone.name}, Destination: {self.destination_zone.name}, State: {self.state}, Metadata: {self.metadata})"

# Define the StateTracker class to keep track of the state of all entities
class StateTracker:
    def __init__(self, drivers, riders, ride_requests):
        self.drivers = drivers
        self.riders = riders
        self.ride_requests = ride_requests

    # Print the states of all entities
    def print_states(self, label):
        print(f"\n{label}")
        for rider in self.riders:
            print(rider)
        for driver in self.drivers:
            print(driver)
        for request in self.ride_requests:
            print(request)

# Create the 10x10 grid of zones
zones = {(x, y): Zone(x, y) for x in range(1, 11) for y in range(1, 11)}

# Define driver preferences with weights for different ride attributes
driver_preferences = [
    {"cost_weight": 0.4, "distance_weight": 0.1, "duration_weight": 0.1, "driver_rating_weight": 0.2, "rider_rating_weight": 0.2, "acceptance_threshold": 20},
    {"cost_weight": 0.3, "distance_weight": 0.2, "duration_weight": 0.1, "driver_rating_weight": 0.1, "rider_rating_weight": 0.3, "acceptance_threshold": 15},
    {"cost_weight": 0.2, "distance_weight": 0.3, "duration_weight": 0.2, "driver_rating_weight": 0.2, "rider_rating_weight": 0.1, "acceptance_threshold": 25}
]

# Initialize 1 rider and 1 driver with specific zones and preferences
rider_zone = zones[(2, 7)]
driver_zone = zones[(5, 5)]
destination_zone = zones[(5, 7)]

riders = [Rider('Rider 0', rider_zone)]
drivers = [Driver('Driver 0', driver_zone, driver_preferences[0])]
ride_request = RideRequest(riders[0], rider_zone, destination_zone, driver_zone)
ride_requests = [ride_request]

# Create the state tracker
state_tracker = StateTracker(drivers, riders, ride_requests)

# Function to find the nearest available driver who accepts the ride based on their preferences
def find_nearest_driver(rider_zone, ride_metadata):
    sorted_drivers = sorted(drivers, key=lambda d: calculate_travel_time((d.zone.x, d.zone.y), (rider_zone.x, rider_zone.y)))
    for driver in sorted_drivers:
        if driver.state == 'idle':
            return driver, calculate_travel_time((driver.zone.x, driver.zone.y), (rider_zone.x, rider_zone.y))
    return None, None

# Simulation workflow
def simulate_rideshare(price_increment=5):
    time_unit = 0

    # Print initial ride requests
    state_tracker.print_states("Initial ride requests")

    # while any(rider.state != 'ride_completed' for rider in riders):
    while time_unit < 20:
        print(f"\nTime Unit: {time_unit}")

        # Print states before updates
        # state_tracker.print_states("Before updates")

        for rider in riders:
            if rider.state == 'waiting':
                ride_request = next((request for request in ride_requests if request.rider == rider), None)
                if ride_request:
                    current_cost = ride_request.metadata["cost_usd"]
                    driver, travel_time = find_nearest_driver(rider.zone, ride_request.metadata)
                    # while not driver:
                    #     current_cost += price_increment
                    #     ride_request.metadata["cost_usd"] = current_cost
                    #     driver, travel_time = find_nearest_driver(rider.zone, ride_request.metadata)

                    if driver:
                        print(f"{driver.name} will pick up {rider.name} from {rider.zone.name}. Travel time: {travel_time}")
                        driver.time_to_next_zone = travel_time
                        driver.current_rider = rider
                        driver.current_request = ride_request
                        driver.accept_ride()  # This should trigger the transition to 'en_route'
                        driver.current_request.metadata["pickup_time"] = datetime.now() + timedelta(minutes=time_unit)
                        driver.current_request.accept()
                        rider.match_with_driver()
                        rider.estimated_wait_time = travel_time

        for driver in drivers:
            if driver.time_to_next_zone > 0:
                driver.time_to_next_zone -= 1
                print(f"{driver.name} is traveling. Time to next zone: {driver.time_to_next_zone}")
                print("Driver State:", driver)
            elif driver.time_to_next_zone == 0:
                if driver.state == 'en_route':
                    driver.arrive_at_pickup()
                    driver.zone = driver.current_rider.zone
                    print(f"{driver.name} has arrived at the pickup zone for {driver.current_rider.name}.")
                elif driver.state == 'waiting_for_rider':
                    driver.pick_up_rider()
                    driver.current_request.start()
                    driver.current_rider.start_ride()
                    driver.time_to_next_zone = calculate_travel_time((driver.zone.x, driver.zone.y), (driver.current_request.destination_zone.x, driver.current_request.destination_zone.y))
                    print(f"{driver.name} picked up {driver.current_rider.name} and is now in ride.")
                elif driver.state == 'in_ride':
                    if driver.time_to_next_zone == 0:
                        driver.complete_ride()
                        driver.current_request.metadata["dropoff_time"] = datetime.now() + timedelta(minutes=time_unit)
                        driver.current_request.complete()
                        driver.current_rider.complete_ride()
                        print(f"{driver.name} completed the ride with {driver.current_rider.name}.")
                        driver.current_rider = None
                        driver.current_request = None
                        driver.reset()
                        print(f"{driver.name} is now idle.")

        # Print states after updates
        # state_tracker.print_states("After updates")

        time_unit += 1

simulate_rideshare()
 