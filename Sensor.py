import random
import csv
import os
from datetime import datetime, timedelta

# Path to the CSV datasheet
file_path = 'data.csv'

def generate_and_save_numbers(count=500):
    """
    Generate 'count' random numbers between 1 and 100, assign each a fake time
    over a 24-hour period, and append each as its own line to a CSV file.

    Each line is formatted as "HH:MM,number".
    """
    # Define start time and interval for 24-hour span
    start_time = datetime.now().replace(second=0, microsecond=0)
    interval = timedelta(seconds=(24 * 3600) / count)

    # Generate times and values
    times = [start_time + i * interval for i in range(count)]
    numbers = [random.randint(1, 100) for _ in range(count)]

    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Optionally write header only once; uncomment if needed
        # if not file_exists:
        #     writer.writerow(['Time', 'Number'])
        # Write each timestamp and number as its own row
        for t, n in zip(times, numbers):
            time_str = t.strftime("%H:%M")
            writer.writerow([time_str, n])

    return list(zip(times, numbers))

if __name__ == "__main__":
    # Generate and save 500 timestamped numbers, one per row
    data = generate_and_save_numbers()
    print(f"Generated and saved {len(data)} timestamped data points.")
