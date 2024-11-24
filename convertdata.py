import csv


input_file = 'crosses.txt'  
output_file_1 = 'crosses1.csv'  
output_file_2 = 'crosses2.csv' 

open('crosses1.csv', 'w+').close()
open('crosses2.csv', 'w+').close()

def to_decimal(degrees, minutes, direction):
    decimal = degrees + minutes / 60
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

i = 1
with open(input_file, 'r') as txt_file, open(output_file_1, 'w', newline='') as csv_file_1, open(output_file_2, 'w', newline='') as csv_file_2:
    csv_writer_1 = csv.writer(csv_file_1)
    csv_file_1 = open(output_file_1, 'w', newline='')
    csv_writer_1.writerow(['Latitude', 'Longitude', 'Name'])  

    csv_writer_2 = csv.writer(csv_file_2)
    csv_file_2 = open(output_file_2, 'w', newline='')
    csv_writer_2.writerow(['Latitude', 'Longitude', 'Name'])  

    for line in txt_file:
        if i >= 2000:
            csv_writer = csv_writer_2
        else:
            csv_writer = csv_writer_1

        parts = line.strip().split(', ')
        degrees_lat, minutes_lat, direction_lat = int(parts[0]), int(parts[1]), parts[2]
        degrees_lon, minutes_lon, direction_lon = int(parts[3]), int(parts[4]), parts[5]
        

        latitude = to_decimal(degrees_lat, minutes_lat, direction_lat)
        longitude = to_decimal(degrees_lon, minutes_lon, direction_lon)
        
        csv_writer.writerow([latitude, longitude, i])
        i+=1
print(f"Conversion complete. Saved.")