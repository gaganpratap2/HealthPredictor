from datetime import datetime, timedelta

start_time = datetime.now()

events = [
    {
        "event_id": "TEST-001",
        "timestamp": start_time
    },
    {
        "event_id": "TEST-002",
        "timestamp": start_time + timedelta(minutes=1)
    },
    {
        "event_id": "TEST-003",
        "timestamp": start_time + timedelta(minutes=2)
    }
]

arrival_order = [
    events[0],
    events[2],
    events[1]
]

for event in arrival_order:
    print(
        event["event_id"],
        event["timestamp"]
    )