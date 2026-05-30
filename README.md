# 🎓 Student Performance Predictor

An AI-powered application that predicts student final marks based on study hours, attendance, and previous marks. Built with **Python**, **Scikit-Learn**, and **Streamlit**.

## ✨ Features

- **Beautiful UI** — Gradient dark theme with glassmorphism cards, animated headers, and responsive layout
- **Student Input** — Enter name, study hours, attendance, and previous marks
- **AI Prediction** — Uses a trained Random Forest Regressor to predict final marks
- **Interactive Charts** — Gauge charts, feature importance bars, and history trends via Plotly
- **Grade Classification** — Automatically assigns A–F grades based on predicted marks
- **Prediction History** — Automatically saves every prediction with timestamps to CSV
- **Progress Bars** — Visual progress indicators for predicted marks
- **Download History** — Export all predictions as a CSV file

## 🗂️ Project Structure

```
student-performance-predictor/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── assets/
│   └── style.css           # Custom CSS styling
├── data/
│   └── synthetic_data.py   # Generates synthetic student data for training
├── model/
│   ├── __init__.py
│   ├── train.py            # Trains and saves the Random Forest model
│   ├── predict.py          # Prediction logic and grade mapping
│   └── student_model.pkl   # Trained model (generated on first run)
├── utils/
│   ├── __init__.py
│   ├── visualization.py    # Plotly chart creation (gauge, feature importance, history)
│   └── history.py          # Save / load / clear prediction history to CSV
└── history/
    └── predictions.csv     # Auto-saved prediction records
```

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/student-performance-predictor.git
cd student-performance-predictor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

The app will:
1. Train a Random Forest model using synthetic data (automatically on first run)
2. Launch the Streamlit interface in your default browser

## 🧠 How It Works

### Data Generation
`data/synthetic_data.py` creates 2,000 student records using a linear formula with injected noise:

```
final_marks = 10 + 4.5×study_hours + 0.35×attendance + 0.30×previous_marks + noise
```

### Model Training
`model/train.py` trains a **Random Forest Regressor** with:
- 100 estimators
- Max depth of 10
- 80/20 train-test split
- Performance: ~3–5 MAE marks

### Prediction
`model/predict.py` loads the saved model, makes a prediction, clips it to 0–100, and maps it to a grade:
- **A** — ≥ 90
- **B** — ≥ 80
- **C** — ≥ 70
- **D** — ≥ 60
- **F** — < 60

## 🖥️ Usage Guide

1. Enter the **student name** in the text field
2. Adjust **Study Hours**, **Attendance**, and **Previous Marks** using the number inputs
3. Click **"Predict Final Marks"**
4. View:
   - Predicted marks with grade badge
   - Progress bar showing performance level
   - Gauge chart with color-coded ranges
   - Feature importance chart
5. Check the **Prediction History** table at the bottom
6. Use the **sidebar** to clear history or view statistics
7. **Download** history as CSV anytime

## 📦 Dependencies

| Package        | Version |
|----------------|---------|
| streamlit      | 1.35.0  |
| scikit-learn   | 1.5.0   |
| pandas         | 2.2.2   |
| numpy          | 1.26.4  |
| matplotlib     | 3.9.0   |
| plotly         | 5.22.0  |

## 🔮 Future Enhancements

- Add more features (extracurricular activities, parental support, etc.)
- Support for multiple ML models with comparison
- User authentication and multi-user history
- Real dataset integration
- Deployment to Streamlit Cloud / Hugging Face Spaces

## 📄 License

MIT
