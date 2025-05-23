import random
import csv
import os
from datetime import datetime, timedelta

# Path to the CSV datasheet
pressure_file = 'preassure_data'
optical_file = 'orbital_sensor_data'
spectrometer_file = 'spectrometer_data'
file_end='.csv'


def simulate_optical_particle_sensor(count=500):
    """
    Simulate an optical particle sensor on an orbiting satellite by generating 'count'
    random particle-count readings (in particles per cubic meter) over a 24-hour period,
    and append them (time,reading) to a CSV file.

    On first run, writes header: Time,ParticleCount
    """
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    optical_file_now=optical_file+time_stamp+file_end

    start_time = datetime.now().replace(second=0, microsecond=0)
    interval = timedelta(seconds=(24 * 3600) / count)

    times = [start_time + i * interval for i in range(count)]
    readings = [random.uniform(0.0, 500.0) for _ in range(count)]

    file_exists = os.path.isfile(optical_file_now)
    with open(optical_file_now, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Time', 'ParticleCount'])
        for t, r in zip(times, readings):
            writer.writerow([t.strftime("%H:%M"), f"{r:.2f}"])
    return list(zip(times, readings))


def simulate_spectrometer_sensor(count=500, bands=10):
    """
    Simulate a spectrometer sensor by generating 'count' spectral readings over 24 hours.
    Each reading includes 'bands' intensity values at fixed wavelength bands.
    Appends rows (Time, I1, I2, ..., I_bands) to a CSV file.

    On first run, writes header: Time, Band1, Band2, ..., BandN
    """
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    spectrometer_file_now=spectrometer_file+time_stamp+file_end
    
    start_time = datetime.now().replace(second=0, microsecond=0)
    interval = timedelta(seconds=(24 * 3600) / count)

    wavelengths = [380 + i * ((780 - 380) / (bands - 1)) for i in range(bands)]
    file_exists = os.path.isfile(spectrometer_file_now)

    with open(spectrometer_file_now, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            header = ['Time'] + [f"Band_{int(wl)}nm" for wl in wavelengths]
            writer.writerow(header)
        for i in range(count):
            t = start_time + i * interval
            # Generate realistic intensity values (e.g., 0-1000 arbitrary units)
            intensities = [random.uniform(0, 1000) for _ in range(bands)]
            row = [t.strftime("%H:%M")] + [f"{val:.1f}" for val in intensities]
            writer.writerow(row)
    # Return list of (time, [intensities]) tuples
    return [(start_time + i * interval, [random.uniform(0, 1000) for _ in range(bands)]) for i in range(count)]

def simulate_pressure_sensor(count=500):
    """
    Generate 'count' random numbers between 1 and 100, assign each a fake time
    over a 24-hour period, and append each as its own line to a CSV file.

    Each line is formatted as "HH:MM,number".
    """
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pressure_file_now=pressure_file+time_stamp+file_end
    
    # Define start time and interval for 24-hour span
    start_time = datetime.now().replace(second=0, microsecond=0)
    interval = timedelta(seconds=(24 * 3600) / count)

    # Generate times and values
    times = [start_time + i * interval for i in range(count)]
    numbers = [random.randint(1, 100) for _ in range(count)]

    file_exists = os.path.isfile(pressure_file_now)

    with open(pressure_file_now, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
             writer.writerow(['Time', 'Pressure (10^-12 Pa)'])
        
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
    data = simulate_pressure_sensor()
    print(f"Generated and saved {len(data)} timestamped pressure points.")
    
    optical_data = simulate_optical_particle_sensor()
    print(f"Simulated and saved {len(optical_data)} optical particle readings to '{optical_file}'.")

    spectro_data = simulate_spectrometer_sensor()
    print(f"Simulated and saved {len(spectro_data)} spectrometer readings ({len(spectro_data[0][1])} bands) to '{spectrometer_file}'.")
