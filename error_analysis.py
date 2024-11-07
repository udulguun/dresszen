import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import re

# Read data from the error_info.txt file
file_path = 'error_info2.txt'

# List to store extracted date and IP address information
dates = []
ips = []

# Read the error_info.txt line by line
with open(file_path, 'r') as file:
    for line in file:
        # Extract the date and IP using regex
        date_match = re.search(r'Date:\s*([^,]+)', line)
        ip_match = re.search(r'IP:\s*([\d\.]+)', line)
        
        if date_match and ip_match:
            date = date_match.group(1)
            ip = ip_match.group(1)
            
            # Append the extracted information to the lists
            dates.append(date)
            ips.append(ip)

# Convert the dates to datetime objects and create a DataFrame
df = pd.DataFrame({
    'Date': pd.to_datetime(dates, format='%d/%b/%Y %H:%M:%S'),
    'IP': ips
})


color_map = {
    'blue': 'blue',
    'red': 'red',
    'orange': 'orange'
}


unique_ips = df['IP'].unique()

ip_to_color = {}
for i, ip in enumerate(unique_ips):
    if i % 3 == 0:
        ip_to_color[ip] = color_map['blue']
    elif i % 3 == 1:
        ip_to_color[ip] = color_map['red']
    else:
        ip_to_color[ip] = color_map['orange']


fig, ax = plt.subplots(figsize=(10, 6))

# Plot each point with the corresponding color based on the IP
for ip in unique_ips:
    ip_df = df[df['IP'] == ip]
    ax.scatter(ip_df['Date'], ip_df['IP'], label=ip, color=ip_to_color[ip], alpha=0.6, edgecolors="w", s=100)

# Formatting the plot
ax.set_title('Error Timeline by IP Address', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('IP Address', fontsize=12)

# Rotate x-axis labels for readability
plt.xticks(rotation=45)

# Set the x-axis to show the date 
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%b/%Y')) 
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  

# Add a legend for the IP addresses
ax.legend(title='IP Addresses', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

# Show the plot
plt.tight_layout()
plt.show()