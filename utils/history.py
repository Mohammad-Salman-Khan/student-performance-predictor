import os
import pandas as pd
from datetime import datetime

HISTORY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history")
HISTORY_PATH = os.path.join(HISTORY_DIR, "predictions.csv")

COLUMNS = [
    "timestamp",
    "student_name",
    "study_hours",
    "attendance",
    "previous_marks",
    "final_marks",
    "grade",
]


def save_prediction(
    student_name: str,
    study_hours: float,
    attendance: float,
    previous_marks: float,
    final_marks: float,
    grade: str,
):
    os.makedirs(HISTORY_DIR, exist_ok=True)

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student_name": student_name,
        "study_hours": study_hours,
        "attendance": attendance,
        "previous_marks": previous_marks,
        "final_marks": final_marks,
        "grade": grade,
    }

    df = pd.DataFrame([row])

    if os.path.exists(HISTORY_PATH):
        existing = pd.read_csv(HISTORY_PATH)
        df = pd.concat([existing, df], ignore_index=True)

    df.to_csv(HISTORY_PATH, index=False)


def load_history() -> pd.DataFrame:
    if not os.path.exists(HISTORY_PATH):
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(HISTORY_PATH)


def clear_history():
    if os.path.exists(HISTORY_PATH):
        os.remove(HISTORY_PATH)
