# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================
# This file contains helper functions for creating and processing visualizations
# including gender ratio charts, choropleth data preparation, and national
# trend context calculations for the dashboard.
# ============================================================================


import pandas as pd
import plotly.express as px
import plotly.io as pio
from config import BG_COLOR, TEXT_COLOR, FACET_COLORS, TEXT_COLOR


def apply_responsive_layout(
    fig, breakpoint, width=None, height=None, chart_type="line"
):
    """
    Adjust figure layout based on breakpoint and optionally width/height.
    chart_type: 'line', 'bar', 'ratio' or 'map'

    KEY FIX: Ratio charts need more right margin for legend placement
    """
    fig.update_layout(autosize=True)  # Changed from False - lets it adapt

    # Define configs per breakpoint
    if breakpoint == "mobile":
        h = {"bar": 300, "ratio": 350}.get(chart_type, min(height or 400, 400))
        font_size = 8
        # Ratio charts: legend below (horizontal), more bottom margin
        if chart_type == "ratio":
            margin = dict(l=40, r=20, t=40, b=80)  # More bottom space for legend
            legend_config = dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=7),
            )
        elif chart_type == "bar":
            margin = dict(l=60, r=40, t=100, b=60)
            legend_config = dict(
                title="Year",
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
            )
        else:
            margin = dict(l=40, r=20, t=40, b=40)
            legend_config = dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=7),
            )

    elif breakpoint == "tablet":
        h = {"bar": 400, "ratio": 450}.get(chart_type, min(height or 500, 500))
        font_size = 10
        # Ratio charts need MORE right margin for legend
        if chart_type == "ratio":
            margin = dict(l=50, r=100, t=50, b=50)  # Extra right space
            legend_config = dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02,  # Position outside chart area
                font=dict(size=9),
            )
        elif chart_type == "bar":
            margin = dict(l=60, r=40, t=100, b=60)
            legend_config = dict(
                title="Year",
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
            )
        else:
            margin = dict(l=50, r=30, t=50, b=50)
            legend_config = dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02,
                font=dict(size=8),
            )

    elif breakpoint == "desktop":
        h = {"bar": 500, "ratio": 550, "map": 550}.get(
            chart_type, min(height or 650, 650)
        )
        font_size = 12
        # Ratio charts need MORE right margin
        if chart_type == "ratio":
            margin = dict(l=65, r=80, t=60, b=65)  # Extra right space
            legend_config = dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02,
                font=dict(size=10),
            )
        elif chart_type == "bar":
            margin = dict(l=60, r=40, t=100, b=60)
            legend_config = dict(
                title="Year",
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
            )
        else:
            margin = dict(l=65, r=40, t=60, b=65)
            legend_config = dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02,
                font=dict(size=10),
            )

    elif breakpoint == "large":
        h = {"bar": 550, "ratio": 650, "map": 700}.get(
            chart_type, min(height or 800, 800)
        )
        font_size = 12
        # Large screens have enough space
        if chart_type == "ratio":
            margin = dict(l=70, r=130, t=70, b=70)
            legend_config = dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02,
                font=dict(size=11),
            )
        elif chart_type == "bar":
            margin = dict(l=60, r=40, t=100, b=60)
            legend_config = dict(
                title="Year",
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
            )
        else:
            margin = dict(l=75, r=50, t=70, b=50)
            legend_config = dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02,
                font=dict(size=8),
            )

    else:
        # Fallback
        h = min(height or 600, 600)
        font_size = 12
        margin = dict(l=60, r=40, t=60, b=60)
        legend_config = dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            font=dict(size=10),
        )

    # Apply layout updates
    fig.update_layout(
        height=h,
        font=dict(size=font_size),
        margin=margin,
        legend=legend_config,
        showlegend=True,
    )

    return fig


def plot_gender_ratios(df):
    """Calculate Boys/Girls prescription ratios and plot by age group."""
    gender_only = df[df["sex"].isin(["Boys", "Girls"])].copy()

    # Pivot for ratio calculation
    pivot = gender_only.pivot_table(
        index=["year", "age_group"],
        columns="sex",
        values="patients_per_1000",
        fill_value=0,
    ).reset_index()

    # Avoid division by zero
    pivot["Boys_Girls_Ratio"] = pivot["Boys"] / pivot["Girls"].replace(0, 0.001)

    # Define age order
    age_order = ["5-9", "10-14", "15-19", "20-24"]
    pivot["age_group"] = pd.Categorical(
        pivot["age_group"], categories=age_order, ordered=True
    )

    # Create figure
    fig = px.line(
        pivot,
        x="year",
        y="Boys_Girls_Ratio",
        color="age_group",
        markers=True,
        color_discrete_map=FACET_COLORS,
        category_orders={"age_group": age_order},
        custom_data=["age_group"],
        title="<b>Boys-to-Girls ADHD Prescription Ratio by Age Group</b>",
    )
    # Add reference line for when ratio = 1
    fig.add_hline(y=1, line_dash="dot", line_width=2.5, line_color="#F7A3A3")

    fig.update_layout(
        hovermode="x",
        yaxis_title="Boys / Girls Ratio",
        xaxis_title="Year",
        xaxis=dict(tick0=2006, dtick=2),
        legend_title_text="Age Group",
        template="bengtegard",
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font_color=TEXT_COLOR,
    )

    # Define hover template
    hover_template = (
        "<b>Age group:</b> %{customdata[0]}<br>"
        "<b>Boys/Girls Ratio:</b> %{y:.2f}<extra></extra>"
    )

    # Apply hover template and hoverlabel per trace
    for trace in fig.data:
        trace.update(
            hovertemplate=hover_template,
            hoverlabel=dict(
                font=dict(color=FACET_COLORS.get(trace.name, "white")),
                bgcolor=BG_COLOR,
                bordercolor=BG_COLOR,
            ),
            customdata=trace.customdata,
        )

    return fig


def prepare_choropleth_data(df, year, age_group, sex):
    """Prepare data for choropleth map"""
    df_filtered = df[
        (df["year"] == year)
        & (df["age_group"] == age_group)
        & (df["sex"] == sex)
        & (df["medication_category"] == "All medications")
    ].copy()
    county_name_map = {
        "Stockholm": "Stockholm",
        "Dalarna": "Dalarna",
        "Uppsala": "Uppsala",
        "Skåne": "Skåne",
        "Västra Götaland": "Västra Götaland",
        "Södermanland": "Södermanland",
        "Östergötland": "Östergötland",
        "Jönköping": "Jönköping",
        "Kalmar": "Kalmar",
        "Kronoberg": "Kronoberg",
        "Blekinge": "Blekinge",
        "Gotland": "Gotland",
        "Värmland": "Värmland",
        "Västmanland": "Västmanland",
        "Örebro": "Örebro",
        "Gävleborg": "Gävleborg",
        "Västernorrland": "Västernorrland",
        "Jämtland Härjedalen": "Jämtland",
        "Västerbotten": "Västerbotten",
        "Norrbotten": "Norrbotten",
        "Halland": "Halland",
    }
    df_filtered["county_geo"] = df_filtered["county"].map(county_name_map)
    df_filtered = df_filtered.dropna(subset=["county_geo"])
    df_filtered["patients_per_1000"] = pd.to_numeric(
        df_filtered["patients_per_1000"], errors="coerce"
    )
    df_filtered = df_filtered.dropna(subset=["patients_per_1000"])
    return df_filtered


def calculate_national_average(df_national, year, age_group, sex):
    """
    Get the national patients_per_1000 value for a given year, age group, and sex. This number is population-weighted by definition.
    """
    df_filtered = df_national[
        (df_national["year"] == year)
        & (df_national["age_group"] == age_group)
        & (df_national["sex"] == sex)
        & (df_national["medication_category"] == "All medications")
    ]

    if df_filtered.empty or df_filtered["patients_per_1000"].isna().all():
        return None

    return df_filtered["patients_per_1000"].iloc[0]


def get_national_trend_context(df_national, current_year, age_group, sex):
    """
    Compute context about the national trend for display.
    Uses national-level data (already population-weighted).
    """
    current_avg = calculate_national_average(df_national, current_year, age_group, sex)
    baseline_avg = calculate_national_average(df_national, 2006, age_group, sex)

    if None in [current_avg, baseline_avg]:
        return "Insufficient data"

    # Avoid division by zero
    if baseline_avg == 0:
        total_change = float("nan")
        return f"National average: {current_avg / 10:.1f}% (baseline = 0 in 2006)"

    total_change = ((current_avg - baseline_avg) / baseline_avg) * 100
    percentage = current_avg / 10  # convert per 1000 → percent of population

    sign = "+" if total_change >= 0 else ""
    return f"National average: {percentage:.1f}% ({sign}{total_change:.0f}% since 2006)"
