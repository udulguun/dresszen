import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

# Log file path
log_file_path = 'access.log'  # Ensure this is the correct path to your access.log

# Initialize lists to hold log data
log_data = []
error_data = []

# Read and parse the log file
with open(log_file_path, 'r') as log_file:
    for line in log_file:
        # Pattern to extract relevant information from log entries
        log_pattern = re.compile(r'(?P<date>[\d\-]+ [\d\:]+) - (?P<method>\w+) (?P<url>[^\s]+)')
        match = log_pattern.search(line)
        if match:
            date_str = match.group('date')
            method = match.group('method')
            url = match.group('url')

            # Convert the date string to a datetime object
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')

            # Append the parsed log data
            log_data.append({'date': date, 'method': method, 'url': url})

        # You can also add error log parsing here (if you have a specific pattern)
        # For example, if you log errors as: "YYYY-MM-DD HH:MM - ERROR - message"
        error_pattern = re.compile(r'(?P<date>[\d\-]+ [\d\:]+) - ERROR - (?P<message>.*)')
        error_match = error_pattern.search(line)
        if error_match:
            error_date_str = error_match.group('date')
            error_message = error_match.group('message')
            error_date = datetime.strptime(error_date_str, '%Y-%m-%d %H:%M')
            error_data.append({'date': error_date, 'message': error_message})

# Create DataFrames from the log data
df = pd.DataFrame(log_data)
error_df = pd.DataFrame(error_data)

# Analyze page access counts
page_access_count = df.groupby('url').size().reset_index(name='count')

# Save page access analysis to a CSV file
page_access_count.to_csv('page_access_count.csv', index=False)

# Create a bar plot for page access counts
plt.figure(figsize=(10, 6))
plt.barh(page_access_count['url'], page_access_count['count'], color='skyblue')
plt.xlabel('Number of Accesses')
plt.ylabel('Page URL')
plt.title('Page Access Count')
plt.tight_layout()
plt.savefig('page_access_count.png')
plt.show()  # Display the plot if running locally

# Create a timeline for page access
df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' is in datetime format
page_access_timeline = df.groupby('date').size().reset_index(name='count')

# Save page access timeline to a CSV file
page_access_timeline.to_csv('page_access_timeline.csv', index=False)

# Create a line plot for page access timeline
plt.figure(figsize=(10, 6))
plt.plot(page_access_timeline['date'], page_access_timeline['count'], marker='o')
plt.xlabel('Date')
plt.ylabel('Number of Accesses')
plt.title('Page Access Timeline')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('page_access_timeline.png')
plt.show()  # Display the plot if running locally

# Analyze error occurrences
if not error_df.empty:
    error_occurrence_timeline = error_df.groupby('date').size().reset_index(name='count')

    # Save error occurrence timeline to a CSV file
    error_occurrence_timeline.to_csv('error_occurrence_timeline.csv', index=False)

    # Create a line plot for error occurrence timeline
    plt.figure(figsize=(10, 6))
    plt.plot(error_occurrence_timeline['date'], error_occurrence_timeline['count'], color='red', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Errors')
    plt.title('Error Occurrence Timeline')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('error_occurrence_timeline.png')
    plt.show()  # Display the plot if running locally
else:
    print("No errors found in the log file.")
