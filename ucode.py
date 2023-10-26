import csv
import hashlib

# Function to get the SHA256 hash of a given code
def get_sha256_hash(code):
    return hashlib.sha256(code.encode()).hexdigest()

# Name of the input CSV file
input_filename = "input.csv"
# Name of the output CSV file
output_filename = "output.csv"

# Read the codes from the input CSV and write to the output CSV with hashed values
with open(input_filename, 'r') as infile, open(output_filename, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Write the header to the output file
    header = next(reader)
    writer.writerow(header + ["SHA256 Hash"])
    
    # Read each code from column B, hash it, and write to the output file
    for row in reader:
        code = row[1]  # Assuming column B is the second column (index 1)
        hashed_value = get_sha256_hash(code)
        writer.writerow(row + [hashed_value])

print(f"CSV file with hashed values has been generated as {output_filename}!")
