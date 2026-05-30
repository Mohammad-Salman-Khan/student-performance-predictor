import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from config.settings import FEATURE_DEFINITIONS, FEATURE_NAMES, PERFORMANCE_CATEGORIES


def _get_theme_kwargs(is_dark: bool = True):
    if is_dark:
        return {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "white", "family": "Inter, Arial, sans-serif"},
        }
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#1a1a2e", "family": "Inter, Arial, sans-serif"},
    }





def create_gauge_chart(marks: float, is_dark: bool = True) -> go.Figure:
    cat = next(
        (c for c in PERFORMANCE_CATEGORIES if c["min"] <= marks <= c["max"]),
        PERFORMANCE_CATEGORIES[-1],
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=marks,
            domain={"x": [0, 1], "y": [0, 1]},
            title={
                "text": f"<b>{cat['name']}</b>",
                "font": {"size": 20, "color": cat["color"]},
            },
            number={
                "font": {"size": 48, "color": cat["color"]},
                "suffix": "%",
            },
            delta={
                "reference": 50,
                "position": "top",
                "font": {"color": "rgba(255,255,255,0.4)"},
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "rgba(255,255,255,0.3)",
                    "tickfont": {"color": "rgba(255,255,255,0.5)"},
                },
                "bar": {"color": cat["color"]},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(255,77,77,0.2)"},
                    {"range": [40, 60], "color": "rgba(255,166,77,0.2)"},
                    {"range": [60, 75], "color": "rgba(255,204,0,0.2)"},
                    {"range": [75, 90], "color": "rgba(153,255,51,0.2)"},
                    {"range": [90, 100], "color": "rgba(51,204,51,0.2)"},
                ],
                "threshold": {
                    "line": {"color": cat["color"], "width": 6},
                    "thickness": 0.75,
                    "value": marks,
                },
            },
        )
    )

    layout = _get_theme_kwargs(is_dark)
    fig.update_layout(
        **layout,
        height=320,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def create_feature_importance_chart(importance: dict, is_dark: bool = True) -> go.Figure:
    df = pd.DataFrame(
        list(importance.items()), columns=["Feature", "Importance"]
    ).sort_values("Importance", ascending=True)

    df["Label"] = df["Feature"].map(
        lambda x: FEATURE_DEFINITIONS.get(x, {}).get("label", x.replace("_", " ").title())
    )

    text_color = "white" if is_dark else "#1a1a2e"

    fig = px.bar(
        df,
        x="Importance",
        y="Label",
        orientation="h",
        title="<b>What Drives Performance?</b>",
        color="Importance",
        color_continuous_scale="rdylgn",
        text_auto=".1%",
    )

    fig.update_traces(
        textfont=dict(color=text_color, size=12),
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.1%}<extra></extra>",
    )

    layout = _get_theme_kwargs(is_dark)
    fig.update_layout(
        **layout,
        height=max(250, len(importance) * 50),
        xaxis={
            "showgrid": True,
            "gridcolor": "rgba(255,255,255,0.05)",
            "tickformat": ".0%",
            "title": "Relative Importance",
            "title_font": {"color": text_color},
        },
        yaxis={"showgrid": False, "title": ""},
        coloraxis_showscale=False,
    )
    return fig


def create_history_chart(history_df: pd.DataFrame, is_dark: bool = True) -> go.Figure:
    if history_df.empty:
        return None

    text_color = "white" if is_dark else "#1a1a2e"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["final_marks"],
            mode="lines+markers",
            name="Predicted Marks",
            line=dict(color="#00d2ff", width=3),
            marker=dict(
                size=10,
                color=history_df["final_marks"],
                colorscale="rdylgn",
                showscale=True,
                colorbar=dict(
                    title="Marks",
                    titleside="right",
                    tickfont=dict(color=text_color),
                    titlefont=dict(color=text_color),
                ),
                line=dict(width=2, color=text_color),
            ),
            hovertemplate="<b>#%{x}</b><br>Marks: %{y:.1f}%<br>Student: %{customdata}<extra></extra>",
            customdata=history_df["student_name"],
        )
    )

    avg_mark = history_df["final_marks"].mean()
    fig.add_hline(
        y=avg_mark,
        line_dash="dash",
        line_color="rgba(255,255,255,0.3)",
        annotation_text=f"Avg: {avg_mark:.1f}%",
        annotation=dict(font=dict(color=text_color, size=12)),
    )

    layout = _get_theme_kwargs(is_dark)
    fig.update_layout(
        **layout,
        title="<b>Prediction Trends Over Time</b>",
        height=350,
        xaxis={
            "showgrid": False,
            "title": "Prediction #",
            "title_font": {"color": text_color},
            "tickfont": {"color": text_color},
        },
        yaxis={
            "range": [0, 100],
            "showgrid": True,
            "gridcolor": "rgba(255,255,255,0.05)",
            "title": "Final Marks (%)",
            "title_font": {"color": text_color},
            "tickfont": {"color": text_color},
        },
        hovermode="x unified",
        showlegend=False,
    )
    return fig


def create_radar_chart(features: dict, is_dark: bool = True) -> go.Figure:
    text_color = "white" if is_dark else "#1a1a2e"

    categories = []
    values = []
    for name in FEATURE_NAMES:
        definition = FEATURE_DEFINITIONS.get(name, {})
        label = definition.get("icon", "") + " " + definition.get("label", name)
        categories.append(label)
        fmin = definition.get("min", 0)
        fmax = definition.get("max", 100)
        val = features.get(name, 0)
        normalized = (val - fmin) / (fmax - fmin) * 100 if fmax != fmin else 50
        values.append(round(normalized, 1))

    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name="Student Profile",
            line=dict(color="#00d2ff", width=3),
            fillcolor="rgba(0,210,255,0.15)",
            hovertemplate="<b>%{theta}</b><br>Score: %{r:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        **_get_theme_kwargs(is_dark),
        title="<b>Student Profile Radar</b>",
        height=400,
        margin=dict(l=60, r=60, t=50, b=40),
        polar={
            "radialaxis": {
                "visible": True,
                "range": [0, 100],
                "color": text_color,
                "gridcolor": "rgba(255,255,255,0.1)",
                "tickfont": {"color": text_color},
            },
            "angularaxis": {
                "color": text_color,
                "gridcolor": "rgba(255,255,255,0.1)",
                "tickfont": {"size": 10, "color": text_color},
            },
            "bgcolor": "rgba(255,255,255,0.02)",
        },
        showlegend=False,
    )
    return fig


def create_performance_distribution(history_df: pd.DataFrame, is_dark: bool = True) -> go.Figure:
    if history_df.empty:
        return None

    text_color = "white" if is_dark else "#1a1a2e"

    marks = history_df["final_marks"]
    bins = [0, 40, 60, 75, 90, 100]
    labels = ["Poor (0-39)", "Below Avg (40-59)", "Average (60-74)", "Good (75-89)", "Excellent (90-100)"]
    colors = ["#ff4d4d", "#ffa64d", "#ffcc00", "#99ff33", "#33cc33"]

    counts = []
    for i in range(len(bins) - 1):
        if i == len(bins) - 2:
            count = ((marks >= bins[i]) & (marks <= bins[i + 1])).sum()
        else:
            count = ((marks >= bins[i]) & (marks < bins[i + 1])).sum()
        counts.append(count)

    df = pd.DataFrame({"Category": labels, "Count": counts, "Color": colors})

    fig = px.bar(
        df,
        x="Category",
        y="Count",
        color="Category",
        color_discrete_sequence=colors,
        text="Count",
        title="<b>Performance Distribution</b>",
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(color=text_color, size=14),
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    )

    layout = _get_theme_kwargs(is_dark)
    fig.update_layout(
        **layout,
        height=350,
        xaxis={
            "title": "",
            "tickfont": {"color": text_color, "size": 11},
            "gridcolor": "rgba(255,255,255,0.05)",
        },
        yaxis={
            "title": "Number of Predictions",
            "title_font": {"color": text_color},
            "tickfont": {"color": text_color},
            "gridcolor": "rgba(255,255,255,0.05)",
            "showgrid": True,
        },
        showlegend=False,
        bargap=0.3,
    )
    return fig


def create_comparison_chart(
    current_features: dict,
    current_marks: float,
    history_df: pd.DataFrame,
    is_dark: bool = True,
) -> go.Figure:
    text_color = "white" if is_dark else "#1a1a2e"

    fig = go.Figure()

    if not history_df.empty:
        avg_marks = history_df["final_marks"].mean()
        max_marks = history_df["final_marks"].max()
        min_marks = history_df["final_marks"].min()

        fig.add_trace(
            go.Scatter(
                x=["Average", "Best", "Worst", "Current"],
                y=[avg_marks, max_marks, min_marks, current_marks],
                mode="lines+markers+text",
                name="Marks Comparison",
                line=dict(color="rgba(255,255,255,0.3)", width=2, dash="dot"),
                marker=dict(
                    size=[12, 12, 12, 18],
                    color=["rgba(255,255,255,0.5)", "#33cc33", "#ff4d4d", "#00d2ff"],
                    line=dict(width=2, color=text_color),
                ),
                text=[f"{avg_marks:.1f}", f"{max_marks:.1f}", f"{min_marks:.1f}", f"{current_marks:.1f}"],
                textposition="top center",
                textfont=dict(color=text_color, size=12),
                hovertemplate="<b>%{x}</b><br>Marks: %{y:.1f}%<extra></extra>",
            )
        )
    else:
        fig.add_trace(
            go.Bar(
                x=["Current"],
                y=[current_marks],
                name="Current Prediction",
                marker_color="#00d2ff",
                text=f"{current_marks:.1f}",
                textposition="outside",
                textfont=dict(color=text_color, size=14),
            )
        )

    layout = _get_theme_kwargs(is_dark)
    fig.update_layout(
        **layout,
        title="<b>How You Compare</b>",
        height=350,
        xaxis={
            "title": "",
            "tickfont": {"color": text_color, "size": 13},
        },
        yaxis={
            "range": [0, 105],
            "title": "Marks (%)",
            "title_font": {"color": text_color},
            "tickfont": {"color": text_color},
            "gridcolor": "rgba(255,255,255,0.05)",
            "showgrid": True,
        },
        hovermode="x",
        showlegend=False,
    )
    return fig
