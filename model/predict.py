import numpy as np
import pandas as pd
from model.train import load_model


def predict_marks(
    study_hours: float,
    attendance: float,
    previous_marks: float,
) -> dict:
    model = load_model()

    features = pd.DataFrame(
        [[study_hours, attendance, previous_marks]],
        columns=["study_hours", "attendance", "previous_marks"],
    )
    prediction = model.predict(features)[0]
    prediction = round(float(np.clip(prediction, 0, 100)), 1)

    feature_importance = dict(
        zip(
            ["study_hours", "attendance", "previous_marks"],
            model.feature_importances_.tolist(),
        )
    )

    grade = _get_grade(prediction)

    return {
        "final_marks": prediction,
        "grade": grade,
        "feature_importance": feature_importance,
    }


def _get_grade(marks: float) -> str:
    if marks >= 90:
        return "A"
    if marks >= 80:
        return "B"
    if marks >= 70:
        return "C"
    if marks >= 60:
        return "D"
    return "F"


if __name__ == "__main__":
    result = predict_marks(
        study_hours=6.0,
        attendance=85.0,
        previous_marks=75.0,
    )
    print(result)
