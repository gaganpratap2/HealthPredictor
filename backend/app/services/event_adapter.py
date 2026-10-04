def wearable_event_to_dict(event):
    return {
        "timestamp": event.timestamp,
        "glucose_level": event.glucose_level,
        "heart_rate": event.heart_rate,
        "hrv": event.hrv,
        "spo2": event.spo2,
        "steps": event.steps,
        "sleep_state": event.sleep_state,
        "activity_state": event.activity_state,
    }


#Why this is useful

# Your ML/feature code shouldn't need to know:

# "Am I reading PostgreSQL?"

# It should only care:

# "Give me patient measurements."

# That's an important architectural separation.