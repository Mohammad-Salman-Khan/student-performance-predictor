import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


from model.predict import predict_marks
from utils.visualization import (
    create_gauge_chart,
    create_feature_importance_chart,
    create_history_chart,
)
from utils.history import save_prediction, load_history, clear_history


def main():
    load_css()

    st.markdown(
        """
        <div class="main-header">
            <h1>🎓 Student Performance Predictor</h1>
            <p>Predict final marks using AI — based on study habits, attendance & past performance</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-header"><h3>⚙️ Controls</h3></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        if st.button("🗑️ Clear History", use_container_width=True):
            clear_history()
            st.success("History cleared!")
            st.rerun()

        st.markdown("---")

        history = load_history()
        if not history.empty:
            st.markdown(
                f'<p style="color:rgba(255,255,255,0.5);text-align:center;font-size:0.9rem;">'
                f"Total Predictions: <strong>{len(history)}</strong></p>",
                unsafe_allow_html=True,
            )

            avg_marks = history["final_marks"].mean()
            st.metric("📊 Avg Predicted Marks", f"{avg_marks:.1f}")

    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown(
            "<h3 style='color:white;margin-bottom:1.5rem;'>📋 Input Details</h3>",
            unsafe_allow_html=True,
        )

        student_name = st.text_input(
            "👤 Student Name",
            placeholder="e.g. John Doe",
            help="Enter the full name of the student",
        )

        study_hours = st.number_input(
            "📚 Study Hours (per day)",
            min_value=0.0,
            max_value=12.0,
            value=6.0,
            step=0.5,
            help="Average number of hours the student studies per day",
        )

        attendance = st.number_input(
            "🏫 Attendance (%)",
            min_value=50.0,
            max_value=100.0,
            value=85.0,
            step=0.5,
            help="Attendance percentage of the student",
        )

        previous_marks = st.number_input(
            "📝 Previous Marks (%)",
            min_value=20.0,
            max_value=100.0,
            value=70.0,
            step=0.5,
            help="Average marks from previous exams",
        )

        predict_clicked = st.button("🔮 Predict Final Marks", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if "prediction" not in st.session_state:
            st.session_state.prediction = None

        if predict_clicked:
            if not student_name.strip():
                st.error("Please enter a student name.")
            else:
                with st.spinner("🧠 Analyzing student data..."):
                    result = predict_marks(
                        study_hours=study_hours,
                        attendance=attendance,
                        previous_marks=previous_marks,
                    )

                    st.session_state.prediction = result

                    save_prediction(
                        student_name=student_name.strip(),
                        study_hours=study_hours,
                        attendance=attendance,
                        previous_marks=previous_marks,
                        final_marks=result["final_marks"],
                        grade=result["grade"],
                    )

        if st.session_state.prediction:
            result = st.session_state.prediction
            grade_class = f"grade-{result['grade']}"

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            col_marks, col_grade = st.columns([1, 1])

            with col_marks:
                st.markdown(
                    f"<h3 style='color:rgba(255,255,255,0.5);margin-bottom:0;'>Predicted Final Marks</h3>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<h1 style='color:#00d2ff;font-size:4rem;font-weight:800;margin:-0.3rem 0;'>"
                    f"{result['final_marks']}</h1>",
                    unsafe_allow_html=True,
                )

            with col_grade:
                st.markdown(
                    f"<h3 style='color:rgba(255,255,255,0.5);margin-bottom:0;'>Grade</h3>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="grade-badge {grade_class}">{result["grade"]}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            progress_val = result["final_marks"] / 100
            st.progress(progress_val)

            cols = st.columns(3)
            with cols[0]:
                st.metric("Study Hours", f"{study_hours:.1f}h")
            with cols[1]:
                st.metric("Attendance", f"{attendance:.1f}%")
            with cols[2]:
                st.metric("Previous Marks", f"{previous_marks:.1f}%")

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            gauge_fig = create_gauge_chart(result["final_marks"])
            st.plotly_chart(gauge_fig, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            imp_fig = create_feature_importance_chart(
                result["feature_importance"]
            )
            st.plotly_chart(imp_fig, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(
                "<div style='text-align:center;padding:3rem 0;color:rgba(255,255,255,0.3);'>"
                "<h2 style='font-size:3rem;margin-bottom:1rem;'>🔮</h2>"
                "<p style='font-size:1.2rem;'>Enter student details and click Predict</p>"
                "<p style='font-size:0.9rem;'>to see the results here</p>"
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        "<h2 style='color:white;text-align:center;margin-bottom:1.5rem;'>📈 Prediction History</h2>",
        unsafe_allow_html=True,
    )

    history = load_history()

    if not history.empty:
        display_df = history.copy()
        display_df["#"] = range(1, len(display_df) + 1)
        display_df = display_df[
            ["#", "student_name", "study_hours", "attendance",
             "previous_marks", "final_marks", "grade", "timestamp"]
        ]
        display_df.columns = [
            "#", "Student", "Study Hrs", "Attend %",
            "Prev Marks", "Final Marks", "Grade", "Time"
        ]

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

        history_chart = create_history_chart(history)
        if history_chart:
            st.plotly_chart(history_chart, use_container_width=True)

        csv = history.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download History CSV",
            data=csv,
            file_name="prediction_history.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.markdown(
            "<p style='text-align:center;color:rgba(255,255,255,0.3);padding:2rem 0;'>"
            "No predictions yet. Start by entering student data above!</p>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:rgba(255,255,255,0.3);font-size:0.8rem;'>"
        "Built with ❤️ using Streamlit & Scikit-Learn</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
