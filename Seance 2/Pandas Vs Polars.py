import pandas as pd
import numpy as np
import random
import string
import time

# Function to generate random strings
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to generate random dates
def random_date(start='2010-01-01', end='2025-12-31'):
    return pd.to_datetime(pd.to_datetime(start) + np.random.rand() * (pd.to_datetime(end) - pd.to_datetime(start)))

# Number of rows to generate (adjust for file size)
num_rows = 10**5  # ~1 million rows; adjust as needed for your file size

# Generate a large dataset
data = {
    'id': range(1, num_rows + 1),
    'name': [random_string(10) for _ in range(num_rows)],
    'date_of_birth': [random_date() for _ in range(num_rows)],
    'city': [random_string(5) for _ in range(num_rows)],
    'income': np.random.randint(30000, 150000, size=num_rows),
    'status': [random.choice(['Single', 'Married', 'Divorced', 'Widowed']) for _ in range(num_rows)],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Specify the path to save the CSV file
file_path = r'C:\Users\Notebook\Jupyter Python Notebooks\large_test_file.csv'

# Measure the time taken to save the file
start_time = time.time()
df.to_csv(file_path, index=False)
end_time = time.time()

print(f"CSV file generated at: {file_path}")
print(f"Time taken to generate the file: {end_time - start_time:.2f} seconds")

# You can change num_rows to generate a larger file if needed.


















####################################################################################################################################



import polars as pl
import numpy as np
import string
import os
import time

file_path = r"C:\Users\Notebook\Jupyter Python Notebooks\large_test_file.csv"

rows_per_chunk = 1_000_000
num_chunks = 25

if os.path.exists(file_path):
    os.remove(file_path)

def random_strings(n, length):
    letters = np.array(list(string.ascii_letters))
    return (
        np.random.choice(letters, (n, length))
        .view(f'U{length}')
        .reshape(n)
    )

start_total = time.time()

for chunk in range(num_chunks):

    start_id = chunk * rows_per_chunk
    end_id = start_id + rows_per_chunk

    df = pl.DataFrame({
        "id": np.arange(start_id, end_id),
        "name": random_strings(rows_per_chunk, 10),
        "city": random_strings(rows_per_chunk, 6),
        "income": np.random.randint(30000, 150000, rows_per_chunk),
        "status": np.random.choice(
            ["Single", "Married", "Divorced", "Widowed"],
            rows_per_chunk
        )
    })

    if chunk == 0:
        # First chunk creates file + header
        df.write_csv(file_path)
    else:
        # Append in binary mode (IMPORTANT)
        with open(file_path, "ab") as f:
            df.write_csv(f, include_header=False)

    print(f"Chunk {chunk+1}/{num_chunks} written")

end_total = time.time()

print("\nFinished!")
print(f"Total generation time: {end_total - start_total:.2f} seconds")



####################################################################################################################################
