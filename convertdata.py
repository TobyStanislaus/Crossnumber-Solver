import csv

# File paths
input_file = 'crosses.txt'  # Input .txt file
output_file = 'crosses.csv'  # Output .csv file

# Conversion function
def to_decimal(degrees, minutes, direction):
    decimal = degrees + minutes / 60
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

# Process the text file and write to a CSV
with open(input_file, 'r') as txt_file, open(output_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Latitude', 'Longitude'])  # CSV header
    
    for line in txt_file:
        # Parse each line from the .txt file
        parts = line.strip().split(', ')
        degrees_lat, minutes_lat, direction_lat = int(parts[0]), int(parts[1]), parts[2]
        degrees_lon, minutes_lon, direction_lon = int(parts[3]), int(parts[4]), parts[5]
        
        # Convert to decimal degrees
        latitude = to_decimal(degrees_lat, minutes_lat, direction_lat)
        longitude = to_decimal(degrees_lon, minutes_lon, direction_lon)
        
        # Write the result to the CSV
        csv_writer.writerow([latitude, longitude])

print(f"Conversion complete. Saved to {output_file}.")