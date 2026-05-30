import os
import pandas as pd
from datetime import datetime
from config.settings import FEATURE_NAMES

HISTORY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "history")
HISTORY_PATH = os.path.join(HISTORY_DIR, "predictions.csv")

COLUMNS = [
    "timestamp",
    "student_name",
    *FEATURE_NAMES,
    "final_marks",
    "grade",
    "performance_category",
    "confidence_score",
]


def save_prediction(
    student_name: str,
    features: dict,
    final_marks: float,
    grade: str,
    performance_category: str,
    confidence_score: float,
):
    os.makedirs(HISTORY_DIR, exist_ok=True)

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student_name": student_name,
        **{name: features.get(name, 0) for name in FEATURE_NAMES},
        "final_marks": final_marks,
        "grade": grade,
        "performance_category": performance_category,
        "confidence_score": confidence_score,
    }

    df = pd.DataFrame([row])

    if os.path.exists(HISTORY_PATH):
        existing = pd.read_csv(HISTORY_PATH)
        df = pd.concat([existing, df], ignore_index=True)

    df.to_csv(HISTORY_PATH, index=False)


def load_history() -> pd.DataFrame:
    if not os.path.exists(HISTORY_PATH):
        return pd.DataFrame(columns=COLUMNS)

    df = pd.read_csv(HISTORY_PATH)

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""

    return df


def clear_history():
    if os.path.exists(HISTORY_PATH):
        os.remove(HISTORY_PATH)


def delete_prediction(index: int) -> bool:
    df = load_history()
    if df.empty or index < 0 or index >= len(df):
        return False

    df = df.drop(df.index[index]).reset_index(drop=True)
    df.to_csv(HISTORY_PATH, index=False)
    return True


def get_history_stats(history_df: pd.DataFrame) -> dict:
    if history_df.empty:
        return {
            "total": 0,
            "avg_marks": 0,
            "max_marks": 0,
            "min_marks": 0,
            "unique_students": 0,
            "grade_distribution": {},
        }

    return {
        "total": len(history_df),
        "avg_marks": round(history_df["final_marks"].mean(), 1),
        "max_marks": round(history_df["final_marks"].max(), 1),
        "min_marks": round(history_df["final_marks"].min(), 1),
        "unique_students": history_df["student_name"].nunique(),
        "grade_distribution": history_df["grade"].value_counts().to_dict(),
    }
