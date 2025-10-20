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
        height=700,
        width=1000,
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
