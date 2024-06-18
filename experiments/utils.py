def find_nearest_driver(rider_zone, ride_metadata, drivers, shortest_paths):
    nearest_drivers = []
    for driver in drivers:
        travel_time = calculate_travel_time(driver.zone, rider_zone, shortest_paths)
        if driver.state == 'idle' and driver.will_accept_ride(ride_metadata):
            nearest_drivers.append((driver, travel_time))
    
    if nearest_drivers:
        nearest_drivers.sort(key=lambda x: x[1])
        return nearest_drivers[0][0], nearest_drivers[0][1]
    
    return None, None

def calculate_travel_time(zone1, zone2, shortest_paths):
    try:
        return shortest_paths[(zone1.x, zone1.y)][(zone2.x, zone2.y)]
    except KeyError:
        return float('inf')