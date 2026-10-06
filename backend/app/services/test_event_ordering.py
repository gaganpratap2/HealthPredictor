from datetime import datetime

from app.services.event_ordering import detect_out_of_order


previous = datetime.fromisoformat(
    "2026-10-05T10:10:00"
)

normal_event = datetime.fromisoformat(
    "2026-10-05T10:15:00"
)

late_event = datetime.fromisoformat(
    "2026-10-05T10:05:00"
)

print("Normal event:")
print(
    detect_out_of_order(
        previous,
        normal_event,
    )
)

print("\nOut-of-order event:")
print(
    detect_out_of_order(
        previous,
        late_event,
    )
)