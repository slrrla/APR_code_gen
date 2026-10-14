from datetime import datetime

# Example properties dict as returned by backend.properties()
properties = {
    'last_update_date': '2019-11-11T07:16:13+00:00',
    'backend_name': 'ibmq_essex',
    'general': [],
    'qubits': []
}

# Bug: strip off the timezone offset and treat the timestamp as naive/local time,
# leading to confusion about whether it's UTC or local time.
raw_date = properties['last_update_date']
naive_part = raw_date[:19]  # drops the "+00:00" offset
last_update_time = datetime.strptime(naive_part, '%Y-%m-%dT%H:%M:%S')

print("last_update_time (incorrectly treated as naive/local):", last_update_time)
