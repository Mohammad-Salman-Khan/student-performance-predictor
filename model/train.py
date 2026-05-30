import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from data.synthetic_data import generate_student_data

MODEL_DIR = os.path.join(os.path.dirname(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "student_model.pkl")


def train_model():
    print("Generating synthetic training data...")
    df = generate_student_data(n_samples=2000, seed=42)

    X = df[["study_hours", "attendance", "previous_marks"]]
    y = df["final_marks"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model Performance:")
    print(f"  Mean Absolute Error: {mae:.2f} marks")
    print(f"  R² Score: {r2:.4f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    return model


def load_model():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Training a new one...")
        return train_model()
    return joblib.load(MODEL_PATH)


if __name__ == "__main__":
    train_model()
