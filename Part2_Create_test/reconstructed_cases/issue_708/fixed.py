from datetime import datetime

# Example properties dict as returned by backend.properties()
properties = {
    'last_update_date': '2019-11-11T07:16:13+00:00',
    'backend_name': 'ibmq_essex',
    'general': [],
    'qubits': []
}

# Fix: parse the full ISO 8601 string including the UTC offset so the
# timezone information is preserved (the offset shown, +00:00, is UTC).
raw_date = properties['last_update_date']
last_update_time = datetime.fromisoformat(raw_date)

print("last_update_time (timezone-aware, UTC):", last_update_time)
