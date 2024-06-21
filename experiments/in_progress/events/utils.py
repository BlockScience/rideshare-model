import os
import csv


def append_to_csv(file_path, completed_rides, total_distance, total_usd, current_time, num_drivers, num_ride_requests, num_riders):
    try:    
        # Define the header
        header = ["Completed Rides", "Total Distance", "Total USD", "Current Time", "Number of Drivers", "Number of Ride Requests", "Number of Riders"]
        
        # Check if the file exists
        file_exists = os.path.isfile(file_path)
        
        # If the file does not exist, write the header first
        if not file_exists:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
        
        # Append the new entry to the file
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([completed_rides, total_distance, total_usd, current_time, num_drivers, num_ride_requests, num_riders])
        
        print(f"Appended to CSV")
    except Exception as e:
        print(f"Error appending to CSV: {e}")
    
def update_entry_count(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)

    # Count the number of data entries (excluding the header)
    entry_count = len(lines) - 1  # Subtracting 1 for the header row

    # Remove any previous "Number of entries" line
    lines = [line for line in lines if line and (len(line) != 2 or line[0] != "Number of entries")]

    # Write the updated lines back to the file and append the count of entries
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)
        writer.writerow([])
        writer.writerow(["Number of entries", entry_count])
