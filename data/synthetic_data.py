import numpy as np
import pandas as pd
from config.settings import FEATURE_NAMES


def generate_student_data(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    study_hours = np.random.uniform(0, 12, n_samples)
    attendance = np.random.uniform(50, 100, n_samples)
    previous_marks = np.random.uniform(20, 100, n_samples)
    sleep_hours = np.random.uniform(3, 12, n_samples)
    assignment_completion_rate = np.random.uniform(0, 100, n_samples)
    practice_test_score = np.random.uniform(0, 100, n_samples)
    stress_level = np.random.uniform(1, 10, n_samples)

    noise = np.random.normal(0, 4, n_samples)

    stress_penalty = np.where(
        stress_level > 7,
        (stress_level - 7) * 3,
        np.where(stress_level < 4, (4 - stress_level) * 1.5, 0),
    )

    sleep_penalty = np.where(
        sleep_hours < 6,
        (6 - sleep_hours) * 2,
        np.where(sleep_hours > 9, (sleep_hours - 9) * 1.5, 0),
    )

    assignment_bonus = assignment_completion_rate * 0.20
    practice_bonus = practice_test_score * 0.25

    final_marks = (
        5
        + 4.0 * study_hours
        + 0.30 * attendance
        + 0.25 * previous_marks
        + assignment_bonus
        + practice_bonus
        - stress_penalty
        - sleep_penalty
        + noise
    )

    final_marks = np.clip(final_marks, 0, 100)

    df = pd.DataFrame({
        "study_hours": np.round(study_hours, 1),
        "attendance": np.round(attendance, 1),
        "previous_marks": np.round(previous_marks, 1),
        "sleep_hours": np.round(sleep_hours, 1),
        "assignment_completion_rate": np.round(assignment_completion_rate, 1),
        "practice_test_score": np.round(practice_test_score, 1),
        "stress_level": np.round(stress_level, 1),
        "final_marks": np.round(final_marks, 1),
    })

    return df


if __name__ == "__main__":
    df = generate_student_data()
    print(f"Generated {len(df)} student records with {len(FEATURE_NAMES)} features.")
    print(df.head())
    print("\nSummary statistics:")
    print(df.describe())
