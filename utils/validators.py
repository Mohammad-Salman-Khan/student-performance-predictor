import re
from config.settings import FEATURE_DEFINITIONS


def validate_student_name(name: str) -> tuple:
    if not name or not name.strip():
        return False, "Student name cannot be empty."
    if len(name.strip()) < 2:
        return False, "Student name must be at least 2 characters."
    if len(name.strip()) > 100:
        return False, "Student name is too long (max 100 characters)."
    if not re.match(r"^[a-zA-Z\s.\-']+$", name.strip()):
        return False, "Student name can only contain letters, spaces, dots, hyphens, and apostrophes."
    return True, name.strip()


def validate_feature(feature_name: str, value: float) -> tuple:
    definition = FEATURE_DEFINITIONS.get(feature_name)
    if not definition:
        return False, f"Unknown feature: {feature_name}"

    if value < definition["min"] or value > definition["max"]:
        return (
            False,
            f"{definition['label']} must be between {definition['min']} and {definition['max']}.",
        )
    return True, value


def validate_all_features(features: dict) -> list:
    errors = []
    for name, value in features.items():
        valid, msg = validate_feature(name, value)
        if not valid:
            errors.append(msg)
    return errors
