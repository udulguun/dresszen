import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

# Read the content of the log file
with open('nohup.out', 'r') as file:
    logs = file.readlines()

# Extract the relevant information from each log line
log_entries = []
for line in logs:
    # Regex to extract the IP address, timestamp, and requested page
    match = re.match(r'(\d+\.\d+\.\d+\.\d+).\[([^\]]+)\] "GET (/[^ ]+).', line)
    if match:
        ip = match.group(1)
        timestamp_str = match.group(2)  # Corrected timestamp extraction
        url = match.group(3)
        
        # Convert the timestamp string to a datetime object
        # Updated the format string to match the log format correctly
        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y %H:%M:%S')  # Removed the colon after year
        
        # Append the data to the list
        log_entries.append({'ip': ip, 'timestamp': timestamp, 'url': url})

# Create a DataFrame from the list of log entries
df = pd.DataFrame(log_entries)

# Create a plot with the IP addresses on the y-axis and timestamps on the x-axis
plt.figure(figsize=(10, 6))

# We will assign each IP a unique numerical index for plotting
df['ip_index'] = df['ip'].astype('category').cat.codes

# Plot each point on the graph
for ip in df['ip'].unique():
    ip_data = df[df['ip'] == ip]
    plt.scatter(ip_data['timestamp'], ip_data['ip_index'], label=ip, alpha=0.7)

# Adjust labels and the plot
plt.xlabel('Timestamp')
plt.ylabel('IP Address')
plt.title('IP Addresses and Webpage Requests Timeline')

# Customize y-ticks to show actual IP addresses
plt.yticks(df['ip_index'].unique(), df['ip'].unique())

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)
plt.tight_layout()

# Show the legend
plt.legend(title='IP Addresses', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.show()