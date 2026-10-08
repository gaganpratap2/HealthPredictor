from dataclasses import dataclass
from datetime import datetime, timedelta
import math
import random


@dataclass
class SyntheticPatient:
    patient_id: int
    glucose_baseline: float
    glucose_variability: float
    resting_heart_rate: float
    hrv_baseline: float
    spo2_baseline: float
    meal_response: float


MEAL_HOURS = [8, 13, 19]


def generate_patient_profile(patient_id, rng):
    return SyntheticPatient(
        patient_id=patient_id,
        glucose_baseline=rng.uniform(95, 125),
        glucose_variability=rng.uniform(2, 6),
        resting_heart_rate=rng.uniform(60, 80),
        hrv_baseline=rng.uniform(35, 60),
        spo2_baseline=rng.uniform(96.5, 99.0),
        meal_response=rng.uniform(25, 50),
    )


def get_activity_state(hour):
    if 7 <= hour < 8:
        return "walking"

    if 17 <= hour < 18:
        return "walking"

    if 23 <= hour or hour < 7:
        return "sleeping"

    return "resting"


def get_sleep_state(hour):
    if 23 <= hour or hour < 7:
        return "sleeping"

    return "awake"


def calculate_meal_effect(timestamp, meal_response):
    effect = 0.0

    for meal_hour in MEAL_HOURS:
        meal_time = timestamp.replace(
            hour=meal_hour,
            minute=0,
            second=0,
            microsecond=0,
        )

        elapsed_minutes = (
            timestamp - meal_time
        ).total_seconds() / 60

        if 0 <= elapsed_minutes <= 120:
            effect += (
                meal_response
                * math.exp(-elapsed_minutes / 45)
            )

    return effect


def generate_observation(patient, timestamp, rng):
    hour = timestamp.hour

    activity = get_activity_state(hour)
    sleep = get_sleep_state(hour)

    meal_effect = calculate_meal_effect(
        timestamp,
        patient.meal_response,
    )

    noise = rng.gauss(
        0,
        patient.glucose_variability,
    )

    glucose = (
        patient.glucose_baseline
        + meal_effect
        + noise
    )

    if activity == "walking":
        heart_rate = (
            patient.resting_heart_rate
            + rng.uniform(15, 30)
        )

        hrv = (
            patient.hrv_baseline
            - rng.uniform(5, 12)
        )

        steps = rng.randint(20, 60)

    elif sleep == "sleeping":
        heart_rate = (
            patient.resting_heart_rate
            - rng.uniform(5, 12)
        )

        hrv = (
            patient.hrv_baseline
            + rng.uniform(3, 10)
        )

        steps = 0

    else:
        heart_rate = (
            patient.resting_heart_rate
            + rng.uniform(-5, 8)
        )

        hrv = (
            patient.hrv_baseline
            + rng.uniform(-5, 5)
        )

        steps = rng.randint(0, 10)

    spo2 = (
        patient.spo2_baseline
        + rng.gauss(0, 0.3)
    )

    return {
        "patient_id": patient.patient_id,
        "timestamp": timestamp,
        "glucose_level": round(glucose, 2),
        "heart_rate": round(heart_rate, 2),
        "hrv": round(hrv, 2),
        "spo2": round(spo2, 2),
        "steps": steps,
        "activity_state": activity,
        "sleep_state": sleep,
    }


def generate_patient_day(
    patient,
    start_time,
    rng,
):
    readings = []

    current_time = start_time

    for _ in range(288):
        readings.append(
            generate_observation(
                patient=patient,
                timestamp=current_time,
                rng=rng,
            )
        )

        current_time += timedelta(minutes=5)

    return readings


def generate_patient_history(
    patient,
    start_time,
    number_of_days,
    rng,
):
    readings = []

    for day in range(number_of_days):
        day_start = (
            start_time
            + timedelta(days=day)
        )

        day_readings = generate_patient_day(
            patient=patient,
            start_time=day_start,
            rng=rng,
        )

        readings.extend(day_readings)

    return readings


def generate_population(
    number_of_patients,
    start_time,
    number_of_days,
    rng,
):
    all_readings = []

    for patient_id in range(
        1,
        number_of_patients + 1,
    ):
        patient = generate_patient_profile(
            patient_id=patient_id,
            rng=rng,
        )

        patient_readings = generate_patient_history(
            patient=patient,
            start_time=start_time,
            number_of_days=number_of_days,
            rng=rng,
        )

        all_readings.extend(
            patient_readings
        )

    return all_readings