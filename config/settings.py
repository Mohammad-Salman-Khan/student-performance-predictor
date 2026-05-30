FEATURE_DEFINITIONS = {
    "study_hours": {
        "label": "Study Hours (per day)",
        "icon": "📚",
        "min": 0.0,
        "max": 12.0,
        "default": 6.0,
        "step": 0.5,
        "help": "Average number of hours the student studies per day",
        "unit": "h",
    },
    "attendance": {
        "label": "Attendance (%)",
        "icon": "🏫",
        "min": 50.0,
        "max": 100.0,
        "default": 85.0,
        "step": 0.5,
        "help": "Attendance percentage of the student",
        "unit": "%",
    },
    "previous_marks": {
        "label": "Previous Marks (%)",
        "icon": "📝",
        "min": 20.0,
        "max": 100.0,
        "default": 70.0,
        "step": 0.5,
        "help": "Average marks from previous exams",
        "unit": "%",
    },
    "sleep_hours": {
        "label": "Sleep Hours (per night)",
        "icon": "😴",
        "min": 3.0,
        "max": 12.0,
        "default": 7.0,
        "step": 0.5,
        "help": "Average hours of sleep per night",
        "unit": "h",
    },
    "assignment_completion_rate": {
        "label": "Assignment Completion (%)",
        "icon": "📋",
        "min": 0.0,
        "max": 100.0,
        "default": 80.0,
        "step": 5.0,
        "help": "Percentage of assignments submitted on time",
        "unit": "%",
    },
    "practice_test_score": {
        "label": "Practice Test Score (%)",
        "icon": "🧪",
        "min": 0.0,
        "max": 100.0,
        "default": 65.0,
        "step": 5.0,
        "help": "Average score in practice/mock tests",
        "unit": "%",
    },
    "stress_level": {
        "label": "Stress Level (1-10)",
        "icon": "🧠",
        "min": 1.0,
        "max": 10.0,
        "default": 5.0,
        "step": 1.0,
        "help": "Self-reported stress level (1=very low, 10=very high)",
        "unit": "",
    },
}

FEATURE_NAMES = list(FEATURE_DEFINITIONS.keys())

PERFORMANCE_CATEGORIES = [
    {"name": "Excellent", "min": 90, "max": 100, "color": "#33cc33"},
    {"name": "Good", "min": 75, "max": 89, "color": "#99ff33"},
    {"name": "Average", "min": 60, "max": 74, "color": "#ffcc00"},
    {"name": "Below Average", "min": 40, "max": 59, "color": "#ffa64d"},
    {"name": "Poor", "min": 0, "max": 39, "color": "#ff4d4d"},
]

GRADE_MAP = {
    "A": (90, 100),
    "B": (80, 89),
    "C": (70, 79),
    "D": (60, 69),
    "F": (0, 59),
}

IMPROVEMENT_SUGGESTIONS = {
    "study_hours": {
        "low": "Increase your daily study hours. Aim for at least 6-8 hours of focused study per day.",
        "medium": "Your study hours are decent. Consider incorporating active recall and spaced repetition techniques.",
        "good": "Great study discipline! Maintain your current routine and focus on quality over quantity.",
    },
    "attendance": {
        "low": "Improve your attendance. Attending classes regularly is strongly correlated with better performance.",
        "medium": "Your attendance is reasonable. Try to minimize absences to stay consistent with coursework.",
        "good": "Excellent attendance! Keep showing up — consistency is key to academic success.",
    },
    "previous_marks": {
        "low": "Focus on strengthening your fundamentals. Consider tutoring or peer study groups.",
        "medium": "You have a solid foundation. Work on advanced topics to push your scores higher.",
        "good": "Strong prior performance indicates good understanding. Challenge yourself with advanced material.",
    },
    "sleep_hours": {
        "low": "You may be sleep-deprived. Aim for 7-9 hours of sleep to improve cognitive function and memory.",
        "medium": "Your sleep is adequate but could be optimized. Try maintaining a consistent sleep schedule.",
        "good": "Optimal sleep habits! Proper rest supports learning and retention.",
    },
    "assignment_completion_rate": {
        "low": "Complete more assignments on time. Use a planner or digital calendar to track deadlines.",
        "medium": "Good assignment submission rate. Try to aim for 100% to maximize your learning.",
        "good": "Perfect or near-perfect submission rate. This discipline will serve you well.",
    },
    "practice_test_score": {
        "low": "Take more practice tests to identify weak areas. Review mistakes thoroughly after each test.",
        "medium": "Decent practice scores. Focus on timed practice to simulate exam conditions.",
        "good": "Strong practice test performance indicates exam readiness. Keep refining your technique.",
    },
    "stress_level": {
        "low": "You handle stress well. Consider teaching stress management techniques to peers.",
        "medium": "Moderate stress is normal. Practice mindfulness or meditation to keep it manageable.",
        "high": "Your stress level is high. Consider speaking with a counselor, exercising, or taking breaks.",
    },
}

STRESS_THRESHOLD_HIGH = 7.0
STRESS_THRESHOLD_MEDIUM = 4.0

LOW_THRESHOLD = 0.33
HIGH_THRESHOLD = 0.66
