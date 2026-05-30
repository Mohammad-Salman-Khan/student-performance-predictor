import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Performance Predictor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from model.predict import predict_marks
from utils.visualization import (
    create_gauge_chart,
    create_feature_importance_chart,
    create_history_chart,
    create_radar_chart,
    create_performance_distribution,
    create_comparison_chart,
)
from utils.history import (
    save_prediction,
    load_history,
    clear_history,
    delete_prediction,
    get_history_stats,
)
from utils.validators import validate_student_name, validate_all_features
from config.settings import FEATURE_DEFINITIONS, FEATURE_NAMES


def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.markdown(
        """
        <script>
        const toggleTheme = (mode) => {
            document.documentElement.setAttribute('data-theme', mode);
        };
        </script>
        """,
        unsafe_allow_html=True,
    )


def inject_theme_script():
    st.markdown(
        """
        <script>
        const currentTheme = window.parent.document.documentElement.getAttribute('data-theme');
        if (!currentTheme) {
            window.parent.document.documentElement.setAttribute('data-theme', 'dark');
        }
        </script>
        """,
        unsafe_allow_html=True,
    )


def render_landing_page():
    st.markdown(
        """
        <div class="hero-section">
            <h1>🎓 Student Performance<br>Predictor AI</h1>
            <p>Leverage machine learning to predict academic outcomes,<br>
            identify improvement areas, and track performance trends.</p>
            <div class="hero-features">
                <div class="hero-feature">
                    <div class="icon">🤖</div>
                    <h4>AI-Powered</h4>
                    <p>Random Forest model with 7 features for accurate predictions</p>
                </div>
                <div class="hero-feature">
                    <div class="icon">📊</div>
                    <h4>Rich Analytics</h4>
                    <p>Interactive dashboards, radar charts, and trend analysis</p>
                </div>
                <div class="hero-feature">
                    <div class="icon">💡</div>
                    <h4>Smart Insights</h4>
                    <p>Personalized improvement suggestions based on weak areas</p>
                </div>
                <div class="hero-feature">
                    <div class="icon">📈</div>
                    <h4>Track History</h4>
                    <p>Save, compare, and export all your predictions</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_predict_tab():
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            "<h3>📋 Student Details</h3>",
            unsafe_allow_html=True,
        )

        student_name = st.text_input(
            "👤 Student Name",
            placeholder="e.g. John Doe",
            help="Enter the full name of the student",
            key="predict_name",
        )

        features = {}
        cols = st.columns(2)

        for i, name in enumerate(FEATURE_NAMES):
            definition = FEATURE_DEFINITIONS[name]
            with cols[i % 2]:
                features[name] = st.number_input(
                    f"{definition['icon']} {definition['label']}",
                    min_value=definition["min"],
                    max_value=definition["max"],
                    value=definition["default"],
                    step=definition["step"],
                    help=definition["help"],
                    key=f"feature_{name}",
                )

        predict_clicked = st.button("🔮 Predict Final Marks", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if "prediction" not in st.session_state:
            st.session_state.prediction = None

        if predict_clicked:
            is_valid_name, name_result = validate_student_name(student_name)
            feature_errors = validate_all_features(features)

            if not is_valid_name:
                st.error(name_result)
            elif feature_errors:
                for err in feature_errors:
                    st.warning(err)
            else:
                with st.spinner("🧠 Analyzing student data..."):
                    result = predict_marks(**features)

                    st.session_state.prediction = result
                    st.session_state.last_features = features
                    st.session_state.last_name = name_result

                    save_prediction(
                        student_name=name_result,
                        features=features,
                        final_marks=result["final_marks"],
                        grade=result["grade"],
                        performance_category=result["performance_category"],
                        confidence_score=result["confidence"]["score"],
                    )

        if st.session_state.prediction:
            result = st.session_state.prediction
            features = st.session_state.get("last_features", {})
            student_name = st.session_state.get("last_name", "Student")

            grade_class = f"grade-{result['grade'].replace('-', '')}"

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            rcol1, rcol2, rcol3 = st.columns([1, 1, 1])
            with rcol1:
                st.markdown(
                    "<p style='color:var(--text-secondary);margin-bottom:0;font-size:0.9rem;'>Predicted Marks</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<h1 style='color:#00d2ff;font-size:3.5rem;font-weight:900;margin:-0.2rem 0;'>"
                    f"{result['final_marks']}<span style='font-size:1.5rem;'>%</span></h1>",
                    unsafe_allow_html=True,
                )
            with rcol2:
                st.markdown(
                    "<p style='color:var(--text-secondary);margin-bottom:0;font-size:0.9rem;'>Grade</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="grade-badge {grade_class}">{result["grade"]}</div>',
                    unsafe_allow_html=True,
                )
            with rcol3:
                conf = result["confidence"]
                conf_class = f"confidence-{conf['level'].lower()}"
                st.markdown(
                    "<p style='color:var(--text-secondary);margin-bottom:0;font-size:0.9rem;'>Confidence</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<h2 class='{conf_class}' style='font-weight:800;margin:0;'>{conf['level']}</h2>"
                    f"<p style='color:var(--text-muted);font-size:0.85rem;'>{conf['score']}%</p>",
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            progress_val = result["final_marks"] / 100
            st.progress(progress_val)

            st.markdown(
                f"<p style='color:var(--text-secondary);font-size:0.9rem;text-align:center;'>"
                f"<strong>Performance: </strong>{result['performance_category']}</p>",
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3>💡 Improvement Suggestions</h3>", unsafe_allow_html=True)

            if result.get("suggestions"):
                for s in result["suggestions"][:4]:
                    severity = s.get("severity", "low")
                    st.markdown(
                        f'<div class="suggestion-card suggestion-{severity}">'
                        f'<strong style="color:var(--text-primary);">{s["icon"]} {s["label"]}:</strong> '
                        f'<span style="color:var(--text-secondary);font-size:0.9rem;">{s["message"]}</span>'
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    "<p style='color:var(--text-muted);'>No improvement suggestions — keep up the great work!</p>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                gauge_fig = create_gauge_chart(result["final_marks"])
                st.plotly_chart(gauge_fig, use_container_width=True, key="gauge")
                st.markdown("</div>", unsafe_allow_html=True)

            with chart_col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                imp_fig = create_feature_importance_chart(result["feature_importance"])
                st.plotly_chart(imp_fig, use_container_width=True, key="importance")
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            radar_fig = create_radar_chart(features)
            st.plotly_chart(radar_fig, use_container_width=True, key="radar")
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                "<div style='text-align:center;padding:3rem 0;color:var(--text-muted);'>"
                "<h2 style='font-size:3.5rem;margin-bottom:1rem;'>🔮</h2>"
                "<p style='font-size:1.3rem;font-weight:500;'>Ready to Predict</p>"
                "<p style='font-size:0.95rem;'>Enter student details on the left and click <strong>Predict</strong></p>"
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard_tab():
    history = load_history()

    if history.empty:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center;padding:2rem;color:var(--text-muted);'>"
            "<h2 style='font-size:2.5rem;'>📊</h2>"
            "<p>No data yet. Make some predictions first!</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    stats = get_history_stats(history)

    st.markdown(
        "<h3 style='color:var(--text-primary);margin-bottom:1rem;'>📈 Performance Overview</h3>",
        unsafe_allow_html=True,
    )

    metrics_cols = st.columns(5)
    with metrics_cols[0]:
        st.metric("Total Predictions", stats["total"])
    with metrics_cols[1]:
        st.metric("Avg Marks", f'{stats["avg_marks"]}%')
    with metrics_cols[2]:
        st.metric("Highest", f'{stats["max_marks"]}%')
    with metrics_cols[3]:
        st.metric("Lowest", f'{stats["min_marks"]}%')
    with metrics_cols[4]:
        st.metric("Unique Students", stats["unique_students"])

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        history_chart = create_history_chart(history)
        if history_chart:
            st.plotly_chart(history_chart, use_container_width=True, key="dash_history")
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        dist_chart = create_performance_distribution(history)
        if dist_chart:
            st.plotly_chart(dist_chart, use_container_width=True, key="dash_dist")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("prediction"):
        result = st.session_state.prediction
        features = st.session_state.get("last_features", {})

        st.markdown('<div class="card">', unsafe_allow_html=True)
        comp_chart = create_comparison_chart(
            features,
            result["final_marks"],
            history,
        )
        if comp_chart:
            st.plotly_chart(comp_chart, use_container_width=True, key="dash_compare")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='color:var(--text-primary);margin-bottom:1rem;'>📋 All Prediction Records</h3>",
        unsafe_allow_html=True,
    )

    display_df = history.copy()
    display_df["#"] = range(1, len(display_df) + 1)
    display_df = display_df[
        ["#", "student_name", *FEATURE_NAMES, "final_marks",
         "grade", "performance_category", "confidence_score", "timestamp"]
    ]

    col_map = {
        "#": "#",
        "student_name": "Student",
        **{name: FEATURE_DEFINITIONS[name]["label"].split("(")[0].strip() for name in FEATURE_NAMES},
        "final_marks": "Final Marks",
        "grade": "Grade",
        "performance_category": "Category",
        "confidence_score": "Confidence",
        "timestamp": "Time",
    }
    display_df = display_df.rename(columns=col_map)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Final Marks": st.column_config.ProgressColumn(
                "Final Marks",
                format="%.1f",
                min_value=0,
                max_value=100,
            ),
            "Confidence": st.column_config.ProgressColumn(
                "Confidence",
                format="%.0f",
                min_value=0,
                max_value=100,
            ),
        },
    )

    csv = history.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download History CSV",
        data=csv,
        file_name="prediction_history.csv",
        mime="text/csv",
        use_container_width=True,
    )


def render_history_tab():
    history = load_history()

    st.markdown(
        "<h3 style='color:var(--text-primary);margin-bottom:1rem;'>📜 Prediction History</h3>",
        unsafe_allow_html=True,
    )

    if history.empty:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center;padding:2rem;color:var(--text-muted);'>"
            "<h2 style='font-size:2.5rem;'>📭</h2>"
            "<p>No predictions saved yet.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    stats = get_history_stats(history)
    scol1, scol2, scol3, scol4 = st.columns(4)
    with scol1:
        st.metric("Total Records", stats["total"])
    with scol2:
        st.metric("Avg Marks", f'{stats["avg_marks"]}%')
    with scol3:
        st.metric("Best Grade", max(history["grade"].unique()) if not history.empty else "N/A")
    with scol4:
        st.metric("Students", stats["unique_students"])

    st.markdown("<br>", unsafe_allow_html=True)

    history = history.reset_index(drop=True)
    display_df = history.copy()
    display_df["#"] = range(1, len(display_df) + 1)
    display_df = display_df[
        ["#", "timestamp", "student_name", *FEATURE_NAMES,
         "final_marks", "grade", "performance_category", "confidence_score"]
    ]

    col_map = {
        "#": "#",
        "timestamp": "Time",
        "student_name": "Student",
        **{name: FEATURE_DEFINITIONS[name]["label"].split("(")[0].strip() for name in FEATURE_NAMES},
        "final_marks": "Final Marks",
        "grade": "Grade",
        "performance_category": "Category",
        "confidence_score": "Conf",
    }
    display_df = display_df.rename(columns=col_map)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Final Marks": st.column_config.ProgressColumn(
                "Final Marks",
                format="%.1f",
                min_value=0,
                max_value=100,
            ),
        },
    )

    if not history.empty:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h4 style='color:var(--text-primary);'>🗑️ Delete Records</h4>",
            unsafe_allow_html=True,
        )

        delete_options = [
            f"#{i + 1} - {row['student_name']} ({row['final_marks']}%)"
            for i, row in history.iterrows()
        ]
        selected = st.selectbox(
            "Select a record to delete",
            options=["-- Select --"] + delete_options,
        )

        if selected != "-- Select --":
            idx = delete_options.index(selected)
            if st.button("🗑️ Delete Selected Record", use_container_width=True):
                if delete_prediction(idx):
                    st.success("Record deleted!")
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear All History", use_container_width=True):
            clear_history()
            st.success("All history cleared!")
            st.rerun()

        csv = history.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="prediction_history.csv",
            mime="text/csv",
        )


def render_about_tab():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        """
        <h3>🧠 About This Project</h3>
        <p style="color:var(--text-secondary);line-height:1.7;">
        <strong>Student Performance Predictor</strong> is an AI-powered application that predicts
        student academic outcomes based on <strong>7 key features</strong>:
        study hours, attendance, previous marks, sleep hours, assignment completion rate,
        practice test scores, and stress level.
        </p>
        <br>
        <h4>🤖 Machine Learning Model</h4>
        <p style="color:var(--text-secondary);line-height:1.7;">
        Uses a <strong>Random Forest Regressor</strong> trained on 5,000 synthetic student records.
        The model achieves ~3-4 MAE marks with an R² score above 0.90, providing reliable
        predictions with confidence scoring.
        </p>
        <br>
        <h4>🛠️ Tech Stack</h4>
        <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">
            <span style="background:var(--card-bg);padding:0.3rem 0.8rem;border-radius:50px;
                  border:1px solid var(--card-border);font-size:0.85rem;color:var(--text-secondary);">🐍 Python</span>
            <span style="background:var(--card-bg);padding:0.3rem 0.8rem;border-radius:50px;
                  border:1px solid var(--card-border);font-size:0.85rem;color:var(--text-secondary);">🌐 Streamlit</span>
            <span style="background:var(--card-bg);padding:0.3rem 0.8rem;border-radius:50px;
                  border:1px solid var(--card-border);font-size:0.85rem;color:var(--text-secondary);">🧮 Scikit-Learn</span>
            <span style="background:var(--card-bg);padding:0.3rem 0.8rem;border-radius:50px;
                  border:1px solid var(--card-border);font-size:0.85rem;color:var(--text-secondary);">📊 Plotly</span>
            <span style="background:var(--card-bg);padding:0.3rem 0.8rem;border-radius:50px;
                  border:1px solid var(--card-border);font-size:0.85rem;color:var(--text-secondary);">🐼 Pandas</span>
            <span style="background:var(--card-bg);padding:0.3rem 0.8rem;border-radius:50px;
                  border:1px solid var(--card-border);font-size:0.85rem;color:var(--text-secondary);">🎨 Plotly</span>
        </div>
        <br>
        <h4>📂 Project Structure</h4>
        <pre style="background:var(--input-bg);padding:1rem;border-radius:12px;font-size:0.8rem;
             color:var(--text-secondary);line-height:1.5;overflow-x:auto;">
student-performance-predictor/
  app.py              # Main Streamlit app
  config/settings.py   # App settings & constants
  data/synthetic_data.py  # Training data generator
  model/
    train.py           # Random Forest trainer
    predict.py         # Prediction engine
  utils/
    visualization.py   # Plotly charts
    history.py         # CSV history manager
    validators.py      # Input validation
  assets/style.css     # Theming engine
  .streamlit/config.toml  # Deployment config
        </pre>
        <br>
        <p style="text-align:center;color:var(--text-muted);font-size:0.9rem;">
        Built with ❤️ using Python, Streamlit & Scikit-Learn
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    load_css()

    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    theme_icon = "☀️" if st.session_state.theme == "dark" else "🌙"
    theme_label = "Light" if st.session_state.theme == "dark" else "Dark"

    theme_col1, theme_col2, theme_col3 = st.columns([1, 0.2, 0.2])
    with theme_col3:
        if st.button(f"{theme_icon} {theme_label}", help="Toggle dark/light mode"):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()

    theme_data_attr = st.session_state.theme
    st.markdown(
        f'<script>window.parent.document.documentElement.setAttribute("data-theme", "{theme_data_attr}");</script>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-header">
            <h1>🎓 Student Performance Predictor</h1>
            <p>AI-powered academic analytics — predict, analyze, and improve</p>
            <div class="badge-container">
                <span class="badge">🤖 Random Forest</span>
                <span class="badge">📊 7 Features</span>
                <span class="badge">🎯 90%+ Accuracy</span>
                <span class="badge">💡 Smart Insights</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-header">'
            '<h3>⚙️ Navigation</h3>'
            "</div>",
            unsafe_allow_html=True,
        )

        tab_selection = st.radio(
            "Go to",
            ["🏠 Home", "🔮 Predict", "📊 Dashboard", "📜 History", "ℹ️ About"],
            label_visibility="collapsed",
            index=0,
        )

        st.markdown("---")

        history = load_history()
        if not history.empty:
            stats = get_history_stats(history)
            st.markdown(
                f'<p style="color:var(--text-secondary);text-align:center;font-size:0.85rem;">'
                f"📈 Total: <strong>{stats['total']}</strong> · "
                f"Avg: <strong>{stats['avg_marks']}%</strong></p>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            f'<p style="color:var(--text-muted);text-align:center;font-size:0.75rem;">'
            f"v2.0 · Built with Streamlit</p>",
            unsafe_allow_html=True,
        )

    tab_map = {
        "🏠 Home": 0,
        "🔮 Predict": 1,
        "📊 Dashboard": 2,
        "📜 History": 3,
        "ℹ️ About": 4,
    }
    active_tab = tab_map.get(tab_selection, 0)

    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔮 Predict", "📊 Dashboard", "📜 History & About"])

    with tab1:
        render_landing_page()

    with tab2:
        render_predict_tab()

    with tab3:
        render_dashboard_tab()

    with tab4:
        hist_tab, about_tab = st.tabs(["📜 History", "ℹ️ About"])

        with hist_tab:
            render_history_tab()

        with about_tab:
            render_about_tab()


if __name__ == "__main__":
    main()
