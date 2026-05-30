import numpy as np
import pandas as pd


def generate_student_data(n_samples: int = 1000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    study_hours = np.random.uniform(0, 12, n_samples)
    attendance = np.random.uniform(50, 100, n_samples)
    previous_marks = np.random.uniform(20, 100, n_samples)

    noise = np.random.normal(0, 5, n_samples)

    final_marks = (
        10
        + 4.5 * study_hours
        + 0.35 * attendance
        + 0.30 * previous_marks
        + noise
    )

    final_marks = np.clip(final_marks, 0, 100)

    df = pd.DataFrame({
        "study_hours": np.round(study_hours, 1),
        "attendance": np.round(attendance, 1),
        "previous_marks": np.round(previous_marks, 1),
        "final_marks": np.round(final_marks, 1),
    })

    return df


if __name__ == "__main__":
    df = generate_student_data()
    print(f"Generated {len(df)} student records.")
    print(df.head())
    print("\nSummary statistics:")
    print(df.describe())
