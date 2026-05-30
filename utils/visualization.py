import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def create_gauge_chart(marks: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=marks,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Final Marks", "font": {"size": 24}},
            delta={"reference": 50, "position": "top"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "darkblue"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 40], "color": "#ff4d4d"},
                    {"range": [40, 60], "color": "#ffa64d"},
                    {"range": [60, 75], "color": "#ffff4d"},
                    {"range": [75, 90], "color": "#99ff33"},
                    {"range": [90, 100], "color": "#33cc33"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 90,
                },
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white", "family": "Arial"},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def create_feature_importance_chart(importance: dict) -> go.Figure:
    df = pd.DataFrame(
        list(importance.items()), columns=["Feature", "Importance"]
    )
    df["Feature"] = df["Feature"].str.replace("_", " ").str.title()

    fig = px.bar(
        df,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Feature Importance",
        color="Importance",
        color_continuous_scale="viridis",
        text_auto=".2%",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white", "family": "Arial"},
        height=250,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis={"showgrid": False},
        yaxis={"showgrid": False},
    )
    return fig


def create_history_chart(history_df: pd.DataFrame) -> go.Figure:
    if history_df.empty:
        return None

    fig = px.line(
        history_df,
        x=history_df.index,
        y="final_marks",
        title="Prediction History",
        markers=True,
        line_shape="spline",
    )

    fig.update_traces(
        line=dict(color="#00d2ff", width=3),
        marker=dict(size=8, color="#00d2ff", line=dict(width=2, color="white")),
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white", "family": "Arial"},
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis={
            "showgrid": False,
            "title": "Prediction #",
            "title_font": {"color": "white"},
        },
        yaxis={
            "range": [0, 100],
            "showgrid": True,
            "gridcolor": "rgba(255,255,255,0.1)",
            "title": "Final Marks",
            "title_font": {"color": "white"},
        },
    )
    return fig
