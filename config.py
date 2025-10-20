# ============================================================================
# CONFIG
# ============================================================================
# Configuration file for the ADHD medication dashboard application.
# Stores all global settings, color palettes, templates, and mappings.
# ============================================================================

import plotly.graph_objects as go
import plotly.io as pio
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed")
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_CSV = os.path.join(PROCESSED_DATA_PATH, "adhd_medication_2006-2024.csv")

# Mapping ATC codes to medication names
MED_NAME_MAP = {
    "N06BA04 Metylfenidat": "Methylphenidate",
    "N06BA12 Lisdexamfetamin": "Lisdexamfetamine",
    "N06BA02 Dexamfetamin": "Dextroamphetamine",
    "N06BA09 Atomoxetin": "Atomoxetine",
    "C02AC02 Guanfacin": "Guanfacine",
}

# Gender mapping
GENDER_MAP = {"Män": "Boys", "Kvinnor": "Girls", "Båda könen": "Both sexes"}

# County name mapping (Excel format -> Regional format)
COUNTY_MAP = {
    "Blekinge län": "Blekinge",
    "Dalarnas län": "Dalarna",
    "Gotlands län": "Gotland",
    "Gävleborgs län": "Gävleborg",
    "Hallands län": "Halland",
    "Jämtlands län": "Jämtland Härjedalen",
    "Jönköpings län": "Jönköping",
    "Kalmar län": "Kalmar",
    "Kronobergs län": "Kronoberg",
    "Norrbottens län": "Norrbotten",
    "Skåne län": "Skåne",
    "Stockholms län": "Stockholm",
    "Södermanlands län": "Södermanland",
    "Uppsala län": "Uppsala",
    "Värmlands län": "Värmland",
    "Västerbottens län": "Västerbotten",
    "Västernorrlands län": "Västernorrland",
    "Västmanlands län": "Västmanland",
    "Västra Götalands län": "Västra Götaland",
    "Örebro län": "Örebro",
    "Östergötlands län": "Östergötland",
}

# Data file paths
FILES_AND_AGES = {
    "adhd_5-9.xlsx": "5-9",
    "adhd_10-14.xlsx": "10-14",
    "adhd_15-19.xlsx": "15-19",
    "adhd_20-24.xlsx": "20-24",
}

# Valid age groups and sexes
VALID_AGE_GROUPS = ["5-9", "10-14", "15-19", "20-24"]
VALID_GENDERS = ["Män", "Kvinnor", "Båda könen"]

# Data paths
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"

# ============================================================================
# VISUALIZATION STYLING CONFIGURATION
# ============================================================================

# Define colors and fonts from my theme
BG_COLOR = "#FFFFFA"
TEXT_COLOR = "#0D5C63"
BAR_PALETTE = ["#72B0AB", "#BCDDDC", "#FFEDD1", "#FDC1B4", "#FE9179", "#F1606C"]
GRADIENT_COLORS = [
    "#3B4D57",
    "#3C5A63",
    "#3D6670",
    "#3E7480",
    "#3F8290",
    "#40869F",
    "#4191AE",
    "#429DBD",
    "#43A9CC",
    "#44B5DB",
]

# Create a custom Plotly template
bengtegard_template = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Monospace", color=TEXT_COLOR, size=12),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        title=dict(
            font=dict(family="Monospace", color=TEXT_COLOR, size=16),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title=dict(font=dict(family="Monospace", color=TEXT_COLOR, size=14)),
            tickfont=dict(family="Monospace", color=TEXT_COLOR, size=10),
            gridcolor="lightgray",
            gridwidth=0.5,
            zerolinecolor="lightgray",
            zerolinewidth=0.5,
        ),
        yaxis=dict(
            title=dict(font=dict(family="Monospace", color=TEXT_COLOR, size=14)),
            tickfont=dict(family="Monospace", color=TEXT_COLOR, size=10),
            gridcolor="lightgray",
            gridwidth=0.5,
            zerolinecolor="lightgray",
            zerolinewidth=0.5,
        ),
        legend=dict(
            font=dict(family="Monospace", color=TEXT_COLOR),
            bgcolor=BG_COLOR,
            bordercolor=BG_COLOR,
        ),
    )
)

# Register template
pio.templates["bengtegard"] = bengtegard_template

# Color mappings for the dashboard
GENDER_COLORS = {
    "Boys": "#1B9E77",
    "Young men": "#1B9E77",
    "Girls": "#9467BD",
    "Young women": "#9467BD",
    "Both sexes": "#4ADFB2",
}

FACET_COLORS = {
    "5-9": "#D36A3F",  # Dark orange
    "10-14": "#1B9E77",  # Dark green
    "15-19": "#5D69B1",  # Dark teal
    "20-24": "#9467BD",  # Dark indigo
}

# Map Swedish ages to English
FACET_TITLE_MAP = {
    "5-9": "5–9 years",
    "10-14": "10–14 years",
    "15-19": "15–19 years",
    "20-24": "20–24 years",
}
