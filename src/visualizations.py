# src/visualizations.py
import pandas as pd
import plotly.express as px
from config import BG_COLOR, TEXT_COLOR, FACET_COLORS, TEXT_COLOR

# ----------------------
# DATA VISUALIZATION FUNCTIONS
# ----------------------

def plot_gender_ratios(df):
    """Calculate Boys/Girls prescription ratios and plot by age group."""
    gender_only = df[df['gender'].isin(['Boys', 'Girls'])].copy()

    # Pivot for ratio calculation
    pivot = gender_only.pivot_table(
        index=['year', 'age_group'],
        columns='gender',
        values='patients_per_1000',
        fill_value=0
    ).reset_index()
    # Avoid division by zero
    pivot['Boys_Girls_Ratio'] = pivot['Boys'] / pivot['Girls'].replace(0, 0.001)

    # Define age order
    age_order = ["5-9", "10-14", "15-19", "20-24"]
    pivot['age_group'] = pd.Categorical(pivot['age_group'], categories=age_order, ordered=True)

    # Create figure
    fig = px.line(
        pivot,
        x='year',
        y='Boys_Girls_Ratio',
        color='age_group',
        markers=True,
        color_discrete_map=FACET_COLORS,
        category_orders={"age_group": age_order},
        title='Boys-to-Girls ADHD Prescription Ratio by Age Group'
    )
    fig.add_hline(y=1, line_dash="dot", line_color=TEXT_COLOR)
    fig.update_layout(
        yaxis_title='Boys / Girls Ratio',
        xaxis_title='Year',
        legend_title_text='Age Group',
        height=700,
        width=1000,
        template='bengtegard',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font_color=TEXT_COLOR
    )
    return fig

def prepare_choropleth_data(df, year, age_group, gender):
    """Prepare data for choropleth map"""
    df_filtered = df[
        (df['year'] == year) &
        (df['age_group'] == age_group) &
        (df['gender'] == gender) &
        (df['medication_category'] == "All medications")
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
        "Halland": "Halland"
    }
    df_filtered['county_geo'] = df_filtered['county'].map(county_name_map)
    df_filtered = df_filtered.dropna(subset=['county_geo'])
    df_filtered['patients_per_1000'] = pd.to_numeric(df_filtered['patients_per_1000'], errors='coerce')
    df_filtered = df_filtered.dropna(subset=['patients_per_1000'])
    return df_filtered

def calculate_national_average(df_regional, year, age_group, gender):
    """Calculate simple national average for a given year/demographic."""
    df_filtered = df_regional[
        (df_regional['year'] == year) &
        (df_regional['age_group'] == age_group) &
        (df_regional['gender'] == gender) &
        (df_regional['medication_category'] == "All medications")
    ].copy()
    df_filtered = df_filtered.dropna(subset=['patients_per_1000'])
    if df_filtered.empty:
        return None
    return df_filtered['patients_per_1000'].mean()

def get_national_trend_context(df_regional, current_year, age_group, gender):
    """Get simple context about national trends for display"""
    current_avg = calculate_national_average(df_regional, current_year, age_group, gender)
    baseline_avg = calculate_national_average(df_regional, 2006, age_group, gender)
    if None in [current_avg, baseline_avg]:
        return "Insufficient data"
    total_change = ((current_avg - baseline_avg) / baseline_avg) * 100
    percentage = current_avg / 10
    return f"National average: {percentage:.1f}% (+{total_change:.0f}% since 2006)"

