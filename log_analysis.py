import csv
import re

log_file = 'access.log'
csv_file = 'access.csv'

with open(log_file, 'r') as infile, open(csv_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['IP Address', 'Date', 'Time', 'Request', 'Status Code', 'Size'])

    for line in infile:
        match = re.match(r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+)', line)
        if match:
            ip_address = match.group(1)
            datetime = match.group(2).split(':')
            request = match.group(3)
            status_code = match.group(4)
            size = match.group(5)
            writer.writerow([ip_address, datetime[0], datetime[1], request, status_code, size])
