import numpy as np
import pandas as pd
from model.train import load_model
from config.settings import (
    FEATURE_NAMES,
    FEATURE_DEFINITIONS,
    PERFORMANCE_CATEGORIES,
    IMPROVEMENT_SUGGESTIONS,
    STRESS_THRESHOLD_HIGH,
    STRESS_THRESHOLD_MEDIUM,
    LOW_THRESHOLD,
    HIGH_THRESHOLD,
)


def predict_marks(
    study_hours: float,
    attendance: float,
    previous_marks: float,
    sleep_hours: float,
    assignment_completion_rate: float,
    practice_test_score: float,
    stress_level: float,
) -> dict:
    model = load_model()

    features = pd.DataFrame(
        [[study_hours, attendance, previous_marks, sleep_hours,
          assignment_completion_rate, practice_test_score, stress_level]],
        columns=FEATURE_NAMES,
    )

    predictions = []
    for tree in model.estimators_:
        predictions.append(tree.predict(features)[0])

    std = np.std(predictions)
    prediction = np.mean(predictions)
    prediction = round(float(np.clip(prediction, 0, 100)), 1)

    confidence = _compute_confidence(std)

    feature_importance = dict(
        zip(FEATURE_NAMES, model.feature_importances_.tolist())
    )

    performance_category = _get_performance_category(prediction)
    grade = _get_grade(prediction)
    suggestions = _generate_suggestions(features.iloc[0].to_dict())

    return {
        "final_marks": prediction,
        "confidence": confidence,
        "grade": grade,
        "performance_category": performance_category,
        "feature_importance": feature_importance,
        "suggestions": suggestions,
        "std": round(float(std), 2),
    }


def _compute_confidence(std: float) -> dict:
    max_std = 15.0
    score = max(0, min(100, 100 - (std / max_std) * 100))
    score = round(score, 1)
    if score >= 80:
        level = "High"
    elif score >= 50:
        level = "Medium"
    else:
        level = "Low"
    return {"score": score, "level": level}


def _get_performance_category(marks: float) -> str:
    for cat in PERFORMANCE_CATEGORIES:
        if cat["min"] <= marks <= cat["max"]:
            return cat["name"]
    return "Poor"


def _get_grade(marks: float) -> str:
    if marks >= 90:
        return "A"
    if marks >= 80:
        return "B"
    if marks >= 75:
        return "B-"
    if marks >= 70:
        return "C"
    if marks >= 60:
        return "D"
    return "F"


def _generate_suggestions(features: dict) -> list:
    suggestions = []
    feature_scores = {}

    for name, value in features.items():
        definition = FEATURE_DEFINITIONS.get(name, {})
        fmin = definition.get("min", 0)
        fmax = definition.get("max", 100)
        normalized = (value - fmin) / (fmax - fmin) if fmax != fmin else 0.5
        feature_scores[name] = normalized

    for name, normalized in feature_scores.items():
        suggestions_data = IMPROVEMENT_SUGGESTIONS.get(name, {})
        if name == "stress_level":
            if normalized > 0.7:
                suggestions.append({
                    "feature": name,
                    "icon": FEATURE_DEFINITIONS[name]["icon"],
                    "label": FEATURE_DEFINITIONS[name]["label"],
                    "value": features[name],
                    "severity": "high",
                    "message": suggestions_data.get(
                        "high",
                        "Your stress level is high. Consider relaxation techniques.",
                    ),
                })
        elif name == "sleep_hours":
            if normalized < 0.3 or normalized > 0.8:
                tag = "low" if normalized < 0.3 else "medium"
                suggestions.append({
                    "feature": name,
                    "icon": FEATURE_DEFINITIONS[name]["icon"],
                    "label": FEATURE_DEFINITIONS[name]["label"],
                    "value": features[name],
                    "severity": "medium" if normalized < 0.3 else "low",
                    "message": suggestions_data.get(
                        tag,
                        "Optimize your sleep for better performance.",
                    ),
                })
        else:
            if normalized < LOW_THRESHOLD:
                suggestions.append({
                    "feature": name,
                    "icon": FEATURE_DEFINITIONS[name]["icon"],
                    "label": FEATURE_DEFINITIONS[name]["label"],
                    "value": features[name],
                    "severity": "high",
                    "message": suggestions_data.get(
                        "low",
                        f"Improve your {FEATURE_DEFINITIONS[name]['label'].lower()}.",
                    ),
                })

    top_features = sorted(
        feature_scores.items(), key=lambda x: x[1]
    )[:3]

    for name, _ in top_features:
        if not any(s["feature"] == name for s in suggestions):
            normalized = feature_scores[name]
            suggestions_data = IMPROVEMENT_SUGGESTIONS.get(name, {})
            if normalized < LOW_THRESHOLD:
                tag = "low"
            elif normalized < HIGH_THRESHOLD:
                tag = "medium"
            else:
                tag = "good"
            if tag != "good":
                suggestions.append({
                    "feature": name,
                    "icon": FEATURE_DEFINITIONS[name]["icon"],
                    "label": FEATURE_DEFINITIONS[name]["label"],
                    "value": features[name],
                    "severity": "low" if tag == "medium" else "high",
                    "message": suggestions_data.get(
                        tag,
                        f"Work on improving your {FEATURE_DEFINITIONS[name]['label'].lower()}.",
                    ),
                })

    suggestions = sorted(suggestions, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["severity"]])

    return suggestions[:5]


if __name__ == "__main__":
    result = predict_marks(
        study_hours=6.0,
        attendance=85.0,
        previous_marks=75.0,
        sleep_hours=7.0,
        assignment_completion_rate=80.0,
        practice_test_score=65.0,
        stress_level=5.0,
    )
    import json
    print(json.dumps(result, indent=2, default=str))
