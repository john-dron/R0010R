import random
import csv
import os
from datetime import datetime, timedelta

# Path to the CSV datasheet for the fake orbital optical particle sensor
data_file = 'orbital_sensor_data.csv'

def simulate_optical_particle_sensor(count=500):
    """
    Simulate an optical particle sensor on an orbiting satellite by generating 'count'
    random particle-count readings (in particles per cubic meter) over a 24-hour period,
    and append them (time,reading) to a CSV file.

    On first run, writes header: Time,ParticleCount
    """
    # Set up 24-hour span from now with even intervals
    start_time = datetime.now().replace(second=0, microsecond=0)
    interval = timedelta(seconds=(24 * 3600) / count)

    # Generate timestamps and simulated readings
    times = [start_time + i * interval for i in range(count)]
    # Particle counts: use floats in a realistic LEO orbital debris range (0–500 particles/m³)
    readings = [random.uniform(0.0, 500.0) for _ in range(count)]

    file_exists = os.path.isfile(data_file)
    
    with open(data_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header once
        if not file_exists:
            writer.writerow(['Time', 'ParticleCount'])
        # Write each reading on its own line
        for t, r in zip(times, readings):
            writer.writerow([t.strftime("%H:%M"), f"{r:.2f}"])

    return list(zip(times, readings))

if __name__ == "__main__":
    data = simulate_optical_particle_sensor()
    print(f"Simulated and saved {len(data)} orbital particle readings to '{data_file}'.")
