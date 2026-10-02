from data_quality import check_wearable_event


class Event:
    heart_rate = 72
    hrv = None
    spo2 = 158
    glucose_level = 120


event = Event()

issues = check_wearable_event(event)

print(issues)