def detect_out_of_order(previous_timestamp, current_timestamp):
    if previous_timestamp is None:
        return False

    return current_timestamp < previous_timestamp


