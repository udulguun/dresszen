import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Log file paths (change these to your actual log file locations)
access_log_path = 'C:/Apache24/logs/access.log'  # Example path
error_log_path = 'C:/Apache24/logs/error.log'    # Example path

# Regex patterns to match log entries
access_pattern = re.compile(r'(?P<ip>[\d\.]+) - - \[(?P<date>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<referer>[^"]+)" "(?P<user_agent>[^"]+)"')
error_pattern = re.compile(r'^\[(?P<date>[^\]]+)\] \[(?P<level>[^\]]+)\] \[(?P<module>[^\]]+)\] (?P<message>.*)')

# Initialize lists to hold extracted data
access_data = []
error_data = []

# Read the access log
with open(access_log_path, 'r') as log_file:
    for line in log_file:
        match = access_pattern.match(line)
        if match:
            ip = match.group('ip')
            date_str = match.group('date')
            request = match.group('request')
            user_agent = match.group('user_agent')
            date = datetime.strptime(date_str.split()[0], '%d/%b/%Y:%H:%M:%S')
            page = request.split(' ')[1]  # Extract the page from the request
            access_data.append({'ip': ip, 'date': date, 'page': page, 'user_agent': user_agent})

# Read the error log
with open(error_log_path, 'r') as log_file:
    for line in log_file:
        match = error_pattern.match(line)
        if match:
            date_str = match.group('date')
            level = match.group('level')
            module = match.group('module')
            message = match.group('message')
            date = datetime.strptime(date_str, '%a %b %d %H:%M:%S.%f %Y')
            error_data.append({'date': date, 'level': level, 'module': module, 'message': message})

# Create DataFrames
access_df = pd.DataFrame(access_data)
error_df = pd.DataFrame(error_data)

# Group by page and count accesses
page_access_count = access_df.groupby(['page', 'ip']).size().reset_index(name='count')

# Create a timeline of accesses
timeline = access_df.groupby(['date', 'page']).size().unstack(fill_value=0)

# Plot the access count for each page
plt.figure(figsize=(12, 6))
for page in timeline.columns:
    plt.plot(timeline.index, timeline[page], label=page)

plt.title('Page Access Timeline')
plt.xlabel('Date')
plt.ylabel('Access Count')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('page_access_timeline.png')
plt.show()

# Save page access statistics to CSV
page_access_count.to_csv('page_access_statistics.csv', index=False)

# Create a timeline for errors
error_timeline = error_df.groupby(['date']).size()

# Plot the error occurrences
plt.figure(figsize=(12, 6))
plt.plot(error_timeline.index, error_timeline.values, marker='o', color='r', label='Error Count')
plt.title('Error Occurrences Timeline')
plt.xlabel('Date')
plt.ylabel('Error Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.savefig('error_occurrences_timeline.png')
plt.show()

# Save error statistics to CSV
error_df.to_csv('error_statistics.csv', index=False)
