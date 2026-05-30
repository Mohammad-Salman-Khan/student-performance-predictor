<div align="center">

# 🎓 Student Performance Predictor AI

**An ML-powered application that predicts student academic outcomes with interactive analytics**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.5%2B-F7931E?style=flat-square&logo=scikit-learn)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.22%2B-3F4F75?style=flat-square&logo=plotly)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

### 🚀 [Live Demo](https://student-performance-predictor.streamlit.app) · 📖 [Documentation](#-features) · 🐛 [Report Bug](https://github.com/yourusername/student-performance-predictor/issues)

</div>

## ✨ Features

### 🤖 AI-Powered Predictions
- **Random Forest Regressor** trained on 5,000 synthetic student records
- **7 input features**: Study Hours, Attendance, Previous Marks, Sleep Hours, Assignment Completion Rate, Practice Test Score, Stress Level
- **Confidence scoring** with standard deviation across trees
- **Personalized improvement suggestions** based on weak areas

### 📊 Rich Interactive Dashboard
- **Gauge chart** with color-coded performance categories (Excellent → Poor)
- **Feature importance** visualization showing what drives results
- **Radar chart** for holistic student profile analysis
- **Trend analysis** of prediction history
- **Performance distribution** bar chart
- **Student comparison** against historical averages

### 🎨 Beautiful UI/UX
- **Dark & Light mode** toggle with CSS variable theming
- **Glassmorphism design** with backdrop filters
- **Animated gradient headers** with shimmer effects
- **Responsive layout** optimized for desktop and mobile
- **Professional landing page** with feature highlights

### 📁 Data Management
- **Automatic saving** of every prediction to CSV
- **Individual record deletion** with dropdown selector
- **Bulk clear** all history
- **CSV download** for external analysis
- **Performance statistics** in sidebar and dashboard

## 🖼️ Screenshots

<div align="center">
  <table>
    <tr>
      <td><strong>🏠 Landing Page</strong></td>
      <td><strong>🔮 Prediction Interface</strong></td>
    </tr>
    <tr>
      <td><em>(Screenshot of landing page with hero section and feature cards)</em></td>
      <td><em>(Screenshot of prediction form with 7 inputs and results panel)</em></td>
    </tr>
    <tr>
      <td><strong>📊 Analytics Dashboard</strong></td>
      <td><strong>📜 History Management</strong></td>
    </tr>
    <tr>
      <td><em>(Screenshot of dashboard with charts and metrics)</em></td>
      <td><em>(Screenshot of history table with delete controls)</em></td>
    </tr>
  </table>
</div>

## 🗂️ Project Structure

```
student-performance-predictor/
├── app.py                       # Main Streamlit application (entry point)
├── requirements.txt             # Python package dependencies
├── README.md                    # This documentation
├── .gitignore                   # Git ignore rules
├── .streamlit/
│   └── config.toml              # Streamlit deployment configuration
├── assets/
│   └── style.css                # Complete theming engine (dark/light mode)
├── config/
│   └── settings.py              # Feature definitions, categories, suggestions
├── data/
│   └── synthetic_data.py        # Generates 5,000 training records
├── model/
│   ├── train.py                 # Random Forest model training pipeline
│   ├── predict.py               # Prediction engine with confidence scoring
│   └── student_model.pkl        # Trained model artifact (auto-generated)
├── utils/
│   ├── visualization.py         # Plotly chart generators (7 chart types)
│   ├── history.py               # CSV history manager with CRUD operations
│   └── validators.py            # Input validation utilities
└── history/
    └── predictions.csv          # Auto-saved prediction records
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/student-performance-predictor.git
cd student-performance-predictor
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the application
```bash
streamlit run app.py
```

The app will:
1. Automatically train a Random Forest model on first run (5,000 samples)
2. Open in your default browser at `http://localhost:8501`

## 🎯 Usage Guide

### Making a Prediction
1. Navigate to the **🔮 Predict** tab
2. Enter the **Student Name**
3. Adjust the **7 feature sliders/inputs**:
   - **📚 Study Hours** (0–12 per day)
   - **🏫 Attendance** (50–100%)
   - **📝 Previous Marks** (20–100%)
   - **😴 Sleep Hours** (3–12 per night)
   - **📋 Assignment Completion** (0–100%)
   - **🧪 Practice Test Score** (0–100%)
   - **🧠 Stress Level** (1–10)
4. Click **🔮 Predict Final Marks**
5. View results with:
   - Predicted marks & grade badge
   - Confidence level (High/Medium/Low)
   - Personalized improvement suggestions
   - Gauge chart & feature importance
   - Student profile radar chart

### Exploring the Dashboard
- **📊 Dashboard** tab shows:
  - Key performance metrics (total, avg, min, max)
  - Trend analysis over time
  - Performance distribution
  - Student comparison chart
  - Full data table with progress bars

### Managing History
- **📜 History** tab allows:
  - View all saved predictions
  - Delete individual records
  - Clear all history
  - Download CSV export

## 🧠 Machine Learning Details

### Model Architecture
| Parameter | Value |
|-----------|-------|
| Algorithm | Random Forest Regressor |
| Estimators | 200 |
| Max Depth | 15 |
| Min Samples Split | 5 |
| Min Samples Leaf | 2 |
| Training Samples | 5,000 (synthetic) |
| Train/Test Split | 80/20 |

### Features & Weights
The model analyzes **7 features** with learned importance weights:
1. **Study Hours** — highest impact on performance
2. **Practice Test Score** — strong predictor of exam readiness
3. **Assignment Completion Rate** — reflects discipline
4. **Attendance** — consistency matters
5. **Previous Marks** — prior academic foundation
6. **Sleep Hours** — moderate impact (too little or too much hurts)
7. **Stress Level** — inverse relationship with performance

### Performance
- **Mean Absolute Error**: ~3–4 marks
- **R² Score**: > 0.90
- **Confidence**: Based on prediction standard deviation across trees

### Grade Boundaries
| Grade | Range | Category |
|-------|-------|----------|
| A | 90–100% | Excellent |
| B | 75–89% | Good |
| C | 60–74% | Average |
| D | 40–59% | Below Average |
| F | 0–39% | Poor |

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Push the repository to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy with:
   - **Main file**: `app.py`
   - **Python version**: 3.11+
   - **Packages**: auto-installed from `requirements.txt`

### Local Deployment
```bash
streamlit run app.py --server.port 8501 --server.enableCORS false
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t student-performance-predictor .
docker run -p 8501:8501 student-performance-predictor
```

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [Python](https://python.org) | Core programming language |
| [Streamlit](https://streamlit.io) | Web application framework |
| [Scikit-Learn](https://scikit-learn.org) | Random Forest ML model |
| [Plotly](https://plotly.com) | Interactive data visualization |
| [Pandas](https://pandas.pydata.org) | Data manipulation & CSV handling |
| [NumPy](https://numpy.org) | Numerical computations |
| [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS) | Custom theming engine |

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
  <p>Built with ❤️ using Python, Streamlit & Scikit-Learn</p>
  <p>
    <a href="https://github.com/yourusername">GitHub</a> ·
    <a href="https://linkedin.com/in/yourusername">LinkedIn</a> ·
    <a href="https://yourportfolio.com">Portfolio</a>
  </p>
</div>
