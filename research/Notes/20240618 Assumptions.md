### Scenario Overview

In this scenario, we will walk through the steps and events that occur when a rider makes a ride request, a driver accepts it, and the ride is completed. 

### Events and Function Calls

#### Initialization
1. **Grid Initialization**
   - **Function**: `Grid.__init__(width, height, weight)`
   - **Data**: `width=4`, `height=4`, `weight=2`
   - **Outcome**: Creates a 4x4 grid with zones and precomputes shortest paths.

2. **Driver and Rider Initialization**
   - **Function**: `Driver.__init__(name, zone, preferences)`
   - **Data**: Various driver names, zones, and preferences.
   - **Outcome**: Initializes drivers in random zones with specified preferences.

   - **Function**: `Rider.__init__(name, zone)`
   - **Data**: Various rider names and zones.
   - **Outcome**: Initializes riders in random zones.

3. **Ride Request Initialization**
   - **Function**: `RideRequest.__init__(rider, origin_zone, destination_zone, shortest_paths, event_queue)`
   - **Data**: `rider=Rider instance`, `origin_zone=random Zone instance`, `destination_zone=random Zone instance`, `shortest_paths=Grid.shortest_paths`, `event_queue=Simulation.event_queue`
   - **Outcome**: Creates ride requests and puts 'ride_request' events into the event queue.

4. **Simulation Initialization**
   - **Function**: `Simulation.__init__(riders, drivers, ride_requests, shortest_paths, max_iterations)`
   - **Data**: `riders=[list of Rider instances]`, `drivers=[list of Driver instances]`, `ride_requests=[list of RideRequest instances]`, `shortest_paths=Grid.shortest_paths`, `max_iterations=1000`
   - **Outcome**: Initializes the simulation with all components and sets up an event queue.

### Detailed Event Sequence

#### Time Unit 1

1. **Ride Request Event Processing**
   - **Function**: `Simulation.process_events()`
   - **Data**: `event_queue`
   - **Outcome**: Processes the first event in the queue, which is a 'ride_request' event.

2. **Driver Handling Ride Request**
   - **Function**: `Driver.handle_ride_request(ride_request, event_queue)`
   - **Data**: `ride_request=RideRequest instance`, `event_queue=Simulation.event_queue`
   - **Outcome**: Each idle driver evaluates the ride request and, if acceptable, emits a 'driver_assigned' event to the event queue.

3. **Driver Acceptance and Assignment**
   - **Function**: `Simulation.handle_driver_assigned(driver, ride_request, travel_time)`
   - **Data**: `driver=Driver instance`, `ride_request=RideRequest instance`, `travel_time=calculated travel time`
   - **Outcome**: Updates the driver and ride request states, sets the driver’s `time_to_next_zone`, and puts the 'driver_assigned' event in the event queue.

#### Time Unit 2

1. **Driver En Route to Pickup**
   - **Function**: `Driver.arrive_at_pickup()`
   - **Data**: `None`
   - **Outcome**: Changes the driver's state to 'waiting_for_rider'.

2. **Rider Matched with Driver**
   - **Function**: `Rider.match_with_driver()`
   - **Data**: `None`
   - **Outcome**: Changes the rider's state to 'matched'.

3. **Driver Picks Up Rider**
   - **Function**: `Driver.pick_up_rider()`
   - **Data**: `None`
   - **Outcome**: Changes the driver's state to 'in_ride'.

4. **Ride Request Start**
   - **Function**: `RideRequest.start()`
   - **Data**: `None`
   - **Outcome**: Changes the ride request state to 'in_progress'.

5. **Rider Starts Ride**
   - **Function**: `Rider.start_ride()`
   - **Data**: `None`
   - **Outcome**: Changes the rider's state to 'in_ride'.

#### Time Unit 3

1. **Driver Completes Ride**
   - **Function**: `Driver.complete_ride()`
   - **Data**: `None`
   - **Outcome**: Changes the driver's state to 'ride_completed'.

2. **Ride Request Complete**
   - **Function**: `RideRequest.complete()`
   - **Data**: `None`
   - **Outcome**: Changes the ride request state to 'completed'.

3. **Rider Completes Ride**
   - **Function**: `Rider.complete_ride()`
   - **Data**: `None`
   - **Outcome**: Changes the rider's state to 'ride_completed'.

4. **Reset Driver to Idle**
   - **Function**: `Driver.reset()`
   - **Data**: `None`
   - **Outcome**: Resets the driver to 'idle' state and ready for the next ride request.

5. **Remove Completed Ride Request**
   - **Function**: `Simulation.update_drivers()`
   - **Data**: `None`
   - **Outcome**: Removes the completed ride request from the active ride requests list.

### Event Queue Implementation Code

Here is the implementation of the scenario using an event queue model:

```python
from datetime import datetime, timedelta
from transitions import Machine, MachineError
import networkx as nx
import random
from queue import Queue

class Zone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = f"Zone ({x},{y})"

    def __str__(self):
        return f"Zone ({self.x},{self.y})"

class Grid:
    def __init__(self, width=4, height=4, weight=2):
        self.width = width
        self.height = height
        self.weight = weight
        self.graph = nx.DiGraph()
        self.zones = {}
        self.shortest_paths = None
        self.create_graph()
        self.create_zones()
        self.precompute_shortest_paths()

    def create_graph(self):
        for i in range(self.width):
            for j in range(self.height):
                self.graph.add_node((i, j))

        for i in range(self.width):
            for j in range(self.height - 1):
                self.graph.add_edge((i, j), (i, j + 1), weight=self.weight)
                self.graph.add_edge((i, j + 1), (i, j), weight=self.weight)
                self.graph.add_edge((j, i), (j + 1, i), weight=self.weight)
                self.graph.add_edge((j + 1, i), (j, i), weight=self.weight)

    def create_zones(self):
        self.zones = {(i, j): Zone(i, j) for i in range(self.width) for j in range(self.height)}

    def precompute_shortest_paths(self):
        self.shortest_paths = dict(nx.all_pairs_dijkstra_path_length(self.graph, weight='weight'))

class Driver:
    states = ['idle', 'en_route', 'waiting_for_rider', 'in_ride', 'ride_completed