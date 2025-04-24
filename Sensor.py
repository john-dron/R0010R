#This is the sensor where data will be produced, still figuring out hwhat that should be
import random
import csv
import os

# Path to the CSV datasheet
file_path = 'data.csv'

def generate_and_save_numbers(count=500):
    numbers = [random.randint(1, 100) for _ in range(count)]
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header if creating a new file
        if not file_exists:
            header = [f"Number{i+1}" for i in range(count)]
            writer.writerow(header)
        # Append generated numbers as one row
        writer.writerow(numbers)
    return numbers

if __name__ == "__main__":
    # Generate and save 500 random numbers in a single row
    generated_numbers = generate_and_save_numbers()
    print(f"Generated and saved {len(generated_numbers)} numbers in a new row.")