# ============================================================================
# LAYOUT MODULE
# ============================================================================
# This file defines the complete HTML/CSS structure and styling for the
# Dash application. Includes section styles, component layout, and all
# interactive controls for the ADHD medication dashboard.
# ============================================================================

from dash import html, dcc
from config import BG_COLOR, TEXT_COLOR, COUNTY_MAP

# ============================================================================
# STYLE DEFINITIONS
# ============================================================================

story_style = {
    "fontFamily": "Satoshi, sans-serif",
    "backgroundColor": BG_COLOR,
    "color": TEXT_COLOR,
    "lineHeight": "1.6",
    "margin": "0",
    "padding": "0",
    "width": "100%",
    "boxSizing": "border-box",
}

section_style = {
    "maxWidth": "800px",
    "margin": "0 auto",
    "padding": "60px 40px",
    "backgroundColor": BG_COLOR,
    "color": TEXT_COLOR,
}

hero_style = {
    "textAlign": "center",
    "padding": "85px 40px 80px",
    "background": "#FFFFE0",
    "color": TEXT_COLOR,
    "marginBottom": "0",
    "margin": "0",
    "width": "100%",
    "boxSizing": "border-box",
}

chart_section_style = {
    "backgroundColor": "#FFFFEF",
    "padding": "60px 0",
    "marginBottom": "0",
    "boxSizing": "border_box",
    "width": "100%",
}

chart_container_style = {"maxWidth": "1100px", "margin": "0 auto", "padding": "0 40px"}

controls_style = {
    "backgroundColor": "#FFFFEF",
    "padding": "30px",
    "borderRadius": "12px",
    "marginBottom": "30px",
    "display": "flex",
    "gap": "30px",
    "alignItems": "center",
    "flexWrap": "wrap",
    "color": TEXT_COLOR,
}

conclusion_section_style = {
    "width": "100%",
    "backgroundColor": TEXT_COLOR,
    "padding": "30px 20px",
    "boxSizing": "border-box",
}

conclusion_references_style = {
    "fontFamily": "Satoshi, sans-serif",
    "fontSize": "14px",
    "color": "#FFFFFF",
    "fontStyle": "bold",
    "textAlign": "left",
    "lineHeight": "1.6",
    "maxWidth": "900px",
    "width": "100%",
    "boxSizing": "border-box",
    "margin": "0 auto",
}


# ============================================================================
# APP LAYOUT
# ============================================================================

# Define medication options for dropdowns
medication_options = [
    {"label": "All medications", "value": "All medications"},
    {"label": "── Individual Medications ──", "value": "separator", "disabled": True},
    {"label": "Methylphenidate", "value": "Methylphenidate"},
    {"label": "Lisdexamfetamine", "value": "Lisdexamfetamine"},
    {"label": "Dextroamphetamine", "value": "Dextroamphetamine"},
    {"label": "Atomoxetine", "value": "Atomoxetine"},
    {"label": "Guanfacine", "value": "Guanfacine"},
]

# Define county options for dropdown
county_options = [
    {"label": "All counties", "value": "All counties"},
    {"label": "── Individual Counties ──", "value": "separator", "disabled": True},
] + [{"label": short_name, "value": short_name} for short_name in COUNTY_MAP.values()]


# Define the layout
def create_layout():
    layout = html.Div(
        [
            # Hero Section
            html.Div(
                [
                    html.H1(
                        "The Rise of ADHD Medication in Sweden",
                        style={
                            "fontSize": "48px",
                            "fontWeight": "700",
                            "marginBottom": "20px",
                            "color": TEXT_COLOR,
                        },
                    ),
                    html.P(
                        "A Demographic Analysis",
                        style={
                            "fontSize": "24px",
                            "fontWeight": "300",
                            "marginBottom": "30px",
                            "color": TEXT_COLOR,
                        },
                    ),
                    html.P(
                        "How have ADHD medication consumption evolved among children and young adults in Sweden from 2006 to 2024?",
                        style={
                            "fontSize": "18px",
                            "maxWidth": "600px",
                            "margin": "0 auto",
                            "fontWeight": "500",
                            "color": TEXT_COLOR,
                        },
                    ),
                ],
                style=hero_style,
            ),
            # Background section
            html.Div(
                [
                    html.P(
                        [
                            "In 2019 Sweden ranked third worldwide in ADHD medication consumption, "
                            "with 99.27 defined daily doses per 1,000 children and adolescents per "
                            "day (DDD/TID). Only Canada (113.60 DDD/TID) and the United States "
                            "(110.28 DDD/TID) reported higher levels, while Norway (74.75 DDD/TID) and "
                            "Denmark (72.71 DDD/TID) followed behind",
                            html.Sup("[1]", style={"fontSize": "13px"}),
                            ". What makes Sweden particularly "
                            "noteworthy is that it leads all countries outside North America, with "
                            "nearly 100 daily doses prescribed per 1,000 young people. This "
                            "positions Sweden as an important case study for understanding ADHD "
                            "treatment practices within a Nordic welfare state context",
                        ],
                        style={"fontSize": "17px", "color": TEXT_COLOR},
                    ),
                    html.P(
                        [
                            "Sweden has since 2006 shown a dramatic increase in the number of "
                            "children and adolescents diagnosed with Attention-Deficit/"
                            "Hyperactivity Disorder (ADHD) according to data published by the "
                            "National Board of Health and Welfare in 2024",
                            html.Sup("[2]", style={"fontSize": "13px"}),
                            ". The global prevalence of ADHD is approximately 5.9% in children "
                            "and adolescents and 2.5% – 2.8% in adults, with rates broadly "
                            "similar worldwide but consistently higher in males than females",
                            html.Sup("[3]", style={"fontSize": "13px"}),
                            ". This contrasts with the proportion of children diagnosed with "
                            "ADHD in Sweden in 2022, where the estimated prevalence among those "
                            "aged 10–17 was 7.7% overall — 10.5% for boys and 6% for girls",
                            html.Sup("[4]", style={"fontSize": "13px"}),
                            ".",
                        ],
                        style={"fontSize": "17px", "color": TEXT_COLOR},
                    ),
                    html.P(
                        [
                            "A Swedish twin study of nearly 20,000 nine-year-olds found no "
                            "significant increase in children meeting ADHD diagnostic criteria "
                            "between 2004 and 2014",
                            html.Sup("[5]", style={"fontSize": "13px"}),
                            ". While small increases appeared in normal and subthreshold "
                            "ADHD-like traits, there was no rise in severe cases. The authors "
                            "suggest that the growing number of diagnoses likely reflects changes in "
                            "diagnostic practices, increased awareness, and better healthcare "
                            "access rather than a true increase in ADHD itself. ",
                            "Engström (2025) further argues that discussions about ADHD should be understood within the broader trend of rising psychiatric diagnoses, including conditions such as depression and anxiety, where medication has become the dominant—and often the only—form of treatment. This reflects a wider process of medicalization, in which symptoms perceived as deviant or problematic are increasingly explained as medical disorders. Private health providers may therefore also contribute to the rise in ADHD diagnoses, as they offer expensive, fast-tracked, guaranteed diagnoses",
                            html.Sup("[6]", style={"fontSize": "13px"}),
                            ".",
                        ],
                        style={"fontSize": "17px", "color": TEXT_COLOR},
                    ),
                    html.P(
                        [
                            "While actual ADHD prevalence is believed to be stable over time, diagnoses continue to rise steadily. According to a 2024 analysis by the Swedish National Board of Health and Welfare, prevalence shows no signs of slowing — projections suggest it could reach 15% of boys and 11% of girls in the near future",
                            html.Sup("[4]", style={"fontsize": "13px"}),
                            ". It's unclear whether this rise reflects better identification of people who truly have ADHD, or whether diagnoses are exceeding actual prevalence — making it increasingly important to understand what's driving this development. ",
                            "This dashboard is designed to make these trends easy to explore interactively. Most reports are static, but here you can actively engage with the data — select different demographics, hover over charts to see relevant measures, and press play to animate changes over time. Key observations are summarized below the charts, but these are by no means exhaustive. Dive into the data yourself and start exploring.",
                        ],
                        style={"fontSize": "17px", "color": TEXT_COLOR},
                    ),
                ],
                style={
                    "maxWidth": "1200px",
                    "margin": "0 auto",
                    "padding": "0 20px",
                    "marginBottom": "15px",
                    "marginTop": "50px",
                    "fontWeight": "400",
                },
            ),
            # Understanding the data section
            html.Div(
                [
                    html.H2(
                        "Understanding the Data",
                        style={
                            "fontSize": "32px",
                            "fontWeight": "600",
                            "marginBottom": "30px",
                            "textAlign": "center",
                            "color": TEXT_COLOR,
                        },
                    ),
                    html.P(
                        [
                            "This project uses open data from",
                            html.I(
                                " the Swedish National Board of Health and Welfare (Socialstyrelsen) "
                            ),
                            html.A(
                                "Statistikdatabas för läkemedel",
                                href="https://www.socialstyrelsen.se/statistik-och-data/statistik/statistikdatabasen",
                                target="_blank",
                                style={
                                    "color": TEXT_COLOR,
                                    "textDecoration": "underline",
                                },
                            ),
                            ", a database that records all prescription medications dispensed in Sweden since 2006. Data were extracted via Socialstyrelsen's API using a custom Python module, allowing separate retrieval of prescription data for each ADHD medication. The analysis tracks the annual number of individuals filling ADHD prescriptions from 2006 to 2024 as a proxy for diagnosis and treatment rates, examining whether growth in medication use varies across four age groups (5-9, 10-14, 15-19, 20-24) and between sexes.",
                        ],
                        style={
                            "fontSize": "17px",
                            "marginBottom": "25px",
                            "color": TEXT_COLOR,
                        },
                    ),
                    html.P(
                        [
                            "Five ADHD medications are ",
                            html.A(
                                "currently approved in Sweden",
                                href="https://www.lakemedelsverket.se/sv/behandling-och-forskrivning/behandlingsrekommendationer/sok-behandlingsrekommendationer/lakemedel-vid-adhd--behandlingsrekommendation",
                                target="_blank",
                                style={
                                    "color": TEXT_COLOR,
                                    "textDecoration": "underline",
                                },
                            ),
                            ": three central nervous system stimulants (methylphenidate, dextroamphetamine, lisdexamfetamine) and two non-stimulants (atomoxetine, guanfacine). The dataset allows separate analysis for each medication, though active ingredients may appear under multiple brand names.",
                        ],
                        style={"fontSize": "17px", "color": TEXT_COLOR},
                    ),
                    html.P(
                        "All rates are expressed as patients per 1,000 inhabitants, enabling comparisons across time and counties. Some demographic subgroups may exceed 1,000 patients per 1,000 inhabitants due to population and age-group definitions (Socialstyrelsen, 2025).",
                        style={"fontSize": "17px", "color": TEXT_COLOR},
                    ),
                ],
                style=section_style,
            ),
            # Interactive Chart Section
            html.Div(
                [
                    html.Div(
                        [
                            html.H2(
                                "Prescription Trends Over Time",
                                style={
                                    "fontSize": "32px",
                                    "fontWeight": "500",
                                    "marginBottom": "20px",
                                    "textAlign": "center",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.P(
                                "The line chart shows the number of individuals using ADHD medications — those who have filled at least one ADHD prescription in a given year, regardless of prior prescriptions. Each person is counted once per year, allowing you to track trends and changes in medication use over time. Use the controls on the left to explore different medications and demographics. Multiple demographic options can be selected simultaneously: age groups are displayed as separate faceted panels for easy comparison, and sex selection allows you to view data for girls, boys, or both together.",
                                style={
                                    "fontSize": "16px",
                                    "textAlign": "center",
                                    "marginBottom": "40px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Div(
                                [
                                    # Sidebar with all controls stacked vertically
                                    html.Div(
                                        [
                                            # Medication settings
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Medication:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.Dropdown(
                                                        id="medication-dropdown",
                                                        options=medication_options,
                                                        value="All medications",
                                                        style={
                                                            "minWidth": "200px",
                                                            "boxShadow": "none",
                                                            "backgroundColor": BG_COLOR,
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "20px"},
                                            ),
                                            # Sex settings
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Sex Selection:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.Checklist(
                                                        id="sex-checklist",
                                                        options=[
                                                            {
                                                                "label": "Boys/Young men",
                                                                "value": "Boys",
                                                            },
                                                            {
                                                                "label": "Girls/Young women",
                                                                "value": "Girls",
                                                            },
                                                            {
                                                                "label": "Both Sexes",
                                                                "value": "Both sexes",
                                                            },
                                                        ],
                                                        value=["Both sexes"],
                                                        inline=False,
                                                        inputStyle={
                                                            "margin-right": "8px"
                                                        },
                                                        style={
                                                            "color": TEXT_COLOR,
                                                            "accent-color": "#4ADFB2",
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "20px"},
                                            ),
                                            # Age settings
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Age Groups:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.Checklist(
                                                        id="age-checklist",
                                                        options=[
                                                            {
                                                                "label": "5-9",
                                                                "value": "5-9",
                                                            },
                                                            {
                                                                "label": "10-14",
                                                                "value": "10-14",
                                                            },
                                                            {
                                                                "label": "15-19",
                                                                "value": "15-19",
                                                            },
                                                            {
                                                                "label": "20-24",
                                                                "value": "20-24",
                                                            },
                                                        ],
                                                        value=["10-14"],
                                                        inline=False,
                                                        inputStyle={
                                                            "margin-right": "8px"
                                                        },
                                                        style={
                                                            "color": TEXT_COLOR,
                                                            "accent-color": "#4ADFB2",
                                                        },
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style={
                                            "flex": "0 0 220px",
                                            "display": "flex",
                                            "flexDirection": "column",
                                            "alignItems": "flex-start",
                                            "paddingRight": "20px",
                                            "marginTop": "200px",
                                        },
                                    ),
                                    # Line chart (right side)
                                    html.Div(
                                        [
                                            dcc.Graph(
                                                id="line-animation",
                                                style={
                                                    "backgroundColor": BG_COLOR,
                                                    "borderRadius": "12px",
                                                    "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
                                                },
                                            ),
                                            # Button to show bar chart
                                            html.Div(
                                                html.Button(
                                                    "Click to Compare 2020 vs 2024",
                                                    id="show-bar-chart-btn",
                                                    n_clicks=0,
                                                    style={
                                                        "width": "50%",
                                                        "padding": "10px",
                                                        "backgroundColor": "#1B9E77",
                                                        "color": "white",
                                                        "border": "none",
                                                        "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
                                                        "borderRadius": "4px",
                                                        "fontSize": "14px",
                                                        "fontWeight": "500",
                                                        "cursor": "pointer",
                                                        "marginTop": "30px",
                                                        "marginBottom": "20px",
                                                    },
                                                ),
                                                style={
                                                    "display": "flex",
                                                    "justifyContent": "center",
                                                },
                                            ),
                                            # Bar chart - hidden by default
                                            html.Div(
                                                dcc.Graph(
                                                    id="bar-chart",
                                                    style={
                                                        "display": "none",
                                                        "borderRadius": "12px",
                                                        "backgroundColor": BG_COLOR,
                                                    },
                                                ),
                                                style={
                                                    "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
                                                    "borderRadius": "12px",
                                                    "overflow": "hidden",
                                                },
                                            ),
                                        ],
                                        style={"flex": "1"},
                                    ),
                                ],
                                style={"display": "flex", "alignItems": "flex-start"},
                            ),
                        ],
                        style=chart_container_style,
                    )
                ],
                style=chart_section_style,
            ),
            # Sex Ratio Section
            html.Div(
                [
                    html.Div(
                        [
                            html.H2(
                                "Sex Disparities in Treatment",
                                style={
                                    "fontSize": "32px",
                                    "fontWeight": "600",
                                    "marginBottom": "20px",
                                    "textAlign": "center",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.P(
                                "The Boys-to-Girls prescription ratio reveals important patterns about sex differences in ADHD diagnosis and treatment. A ratio above one indicates more boys receive prescriptions, while below one indicates more girls.",
                                style={
                                    "fontSize": "16px",
                                    "textAlign": "center",
                                    "marginBottom": "40px",
                                    "color": TEXT_COLOR,
                                    "maxWidth": "700px",
                                    "margin": "0 auto 40px",
                                },
                            ),
                            # Sex ratio controls
                            html.Div(
                                [
                                    html.Label(
                                        "Medication for Ratio Analysis:",
                                        style={
                                            "fontSize": "16px",
                                            "fontWeight": "500",
                                            "marginBottom": "8px",
                                            "display": "block",
                                            "color": TEXT_COLOR,
                                        },
                                    ),
                                    dcc.Dropdown(
                                        id="ratio-medication-dropdown",
                                        options=medication_options,
                                        value="All medications",
                                        style={
                                            "maxWidth": "300px",
                                            "margin": "0 auto",
                                            "backgroundColor": BG_COLOR,
                                            "color": TEXT_COLOR,
                                        },
                                    ),
                                ],
                                style={
                                    "textAlign": "center",
                                    "marginBottom": "30px",
                                    "backgroundColor": "#FFFFEF",
                                    "padding": "20px",
                                    "borderRadius": "8px",
                                },
                            ),
                            # Sex ratio chart
                            dcc.Graph(
                                id="sex-ratio-plot",
                                style={
                                    "backgroundColor": BG_COLOR,
                                    "borderRadius": "12px",
                                    "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
                                },
                            ),
                        ],
                        style=chart_container_style,
                    )
                ],
                style=chart_section_style,
            ),
            # Analysis Section
            html.Div(
                [
                    html.H2(
                        "Key Observations",
                        style={
                            "fontSize": "32px",
                            "fontWeight": "600",
                            "marginBottom": "30px",
                            "color": TEXT_COLOR,
                        },
                    ),
                    html.Ul(
                        [
                            html.Li(
                                "Children and adolescents remain the group with the highest ADHD medication consumption, with boys aged 10-14 having the highest rate at 9.1% in 2024 (up from 6.6% in 2020).",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "Total ADHD medication use across both sexes peaked at 8.3% for ages 15–19 in 2024, up from 5.4% in 2020 - an increase of almost 54%.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "Among girls, prescriptions were most common in the 15-19 age group at 8.3% in 2024, compared to 4.7% in 2020.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "Young women (20-24) show the steepest growth in recent years at 5.2% in 2024, compared to 2.7% in 2020 - an increase of almost 95%.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "In 2024 girls aged 15-19 used ADHD medication slightly more (8.3%) than boys (8.2%), a historic first.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "The sex gap in ADHD medication use is narrowing, with girls aged 15–24 showing higher rates than boys in 2024. This effect is not seen for ages 5–14, where the gap remains.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "Methylphenidate remains the most commonly prescribed ADHD medication across all age groups and sexes.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                        ],
                        style={"color": TEXT_COLOR, "paddingLeft": "30px"},
                    ),
                ],
                style=section_style,
            ),
            # Interactive Choropleth Map Section
            html.Div(
                [
                    html.Div(
                        [
                            html.H2(
                                "Geographic Distribution of ADHD Prescriptions",
                                style={
                                    "fontSize": "32px",
                                    "fontWeight": "600",
                                    "marginBottom": "20px",
                                    "textAlign": "center",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.P(
                                "The map shows total ADHD prescriptions using a fixed color scale to ensure consistent comparison over time. Differences within a single year may be harder to distinguish. Filter by sex and age group, and click play to watch changes over time. Key statistics update dynamically during animation: highest and lowest rates, national average, and total increase since 2006.",
                                style={
                                    "fontSize": "16px",
                                    "textAlign": "center",
                                    "marginBottom": "40px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Div(
                                [
                                    # Choropleth controls sidebar (left side)
                                    html.Div(
                                        [
                                            # Sex selection for choropleth (single choice)
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Sex Selection:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.RadioItems(
                                                        id="choropleth-sex-radio",
                                                        options=[
                                                            {
                                                                "label": "Boys/Young men",
                                                                "value": "Boys",
                                                            },
                                                            {
                                                                "label": "Girls/Young women",
                                                                "value": "Girls",
                                                            },
                                                            {
                                                                "label": "Both Sexes",
                                                                "value": "Both sexes",
                                                            },
                                                        ],
                                                        value="Both sexes",
                                                        inline=False,
                                                        inputStyle={
                                                            "margin-right": "8px"
                                                        },
                                                        style={
                                                            "color": TEXT_COLOR,
                                                            "accent-color": "#4ADFB2",
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "20px"},
                                            ),
                                            # Age settings for choropleth
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Age Groups:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.RadioItems(
                                                        id="choropleth-age-radio",
                                                        options=[
                                                            {
                                                                "label": "5-9",
                                                                "value": "5-9",
                                                            },
                                                            {
                                                                "label": "10-14",
                                                                "value": "10-14",
                                                            },
                                                            {
                                                                "label": "15-19",
                                                                "value": "15-19",
                                                            },
                                                            {
                                                                "label": "20-24",
                                                                "value": "20-24",
                                                            },
                                                        ],
                                                        value="10-14",
                                                        inline=False,
                                                        inputStyle={
                                                            "margin-right": "8px"
                                                        },
                                                        style={
                                                            "color": TEXT_COLOR,
                                                            "accent-color": "#4ADFB2",
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "30px"},
                                            ),
                                            # Animation controls
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Animation:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Button(
                                                                "▶",
                                                                id="choropleth-play-btn",
                                                                n_clicks=0,
                                                                style={
                                                                    "marginRight": "8px",
                                                                    "padding": "6px 12px",
                                                                    "fontSize": "12px",
                                                                    "backgroundColor": "#4ADFB2",
                                                                    "color": BG_COLOR,
                                                                    "cursor": "pointer",
                                                                    "border": "none",
                                                                    "borderRadius": "4px",
                                                                },
                                                            ),
                                                            html.Button(
                                                                "❚❚",
                                                                id="choropleth-pause-btn",
                                                                n_clicks=0,
                                                                style={
                                                                    "marginRight": "7px",
                                                                    "padding": "6px 12px",
                                                                    "fontSize": "11px",
                                                                    "backgroundColor": TEXT_COLOR,
                                                                    "color": "white",
                                                                    "cursor": "pointer",
                                                                    "border": "none",
                                                                    "borderRadius": "4px",
                                                                },
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                                style={"marginBottom": "20px"},
                                            ),
                                        ],
                                        style={
                                            "flex": "0 0 220px",
                                            "display": "flex",
                                            "flexDirection": "column",
                                            "alignItems": "flex-start",
                                            "paddingRight": "20px",
                                            "marginTop": "200px",
                                        },
                                    ),
                                    # Choropleth map and controls (right side)
                                    html.Div(
                                        [
                                            # Year slider
                                            html.Div(
                                                [
                                                    html.Label(
                                                        f"Year: ",
                                                        style={
                                                            "fontWeight": "bold",
                                                            "marginBottom": "10px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.Slider(
                                                        id="choropleth-year-slider",
                                                        min=2006,
                                                        max=2024,
                                                        step=1,
                                                        value=2006,
                                                        marks={
                                                            year: {
                                                                "label": str(year),
                                                                "style": {
                                                                    "color": TEXT_COLOR
                                                                },
                                                            }
                                                            for year in range(
                                                                2006, 2025, 3
                                                            )
                                                        },
                                                        tooltip={
                                                            "placement": "bottom",
                                                            "always_visible": True,
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "30px"},
                                            ),
                                            # Map
                                            dcc.Graph(
                                                id="choropleth-map",
                                                style={
                                                    "backgroundColor": BG_COLOR,
                                                    "borderRadius": "12px",
                                                    "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
                                                },
                                            ),
                                            # Statistics summary
                                            html.Div(
                                                id="choropleth-stats",
                                                style={
                                                    "marginTop": "20px",
                                                    "padding": "15px",
                                                    "backgroundColor": "#FFFFEF",
                                                    "borderRadius": "8px",
                                                    "color": TEXT_COLOR,
                                                },
                                            ),
                                        ],
                                        style={"flex": "1"},
                                    ),
                                ],
                                style={"display": "flex", "alignItems": "flex-start"},
                            ),
                        ],
                        style=chart_container_style,
                    )
                ],
                style=chart_section_style,
            ),
            # Interval component for choropleth animation
            dcc.Interval(
                id="choropleth-interval", interval=1000, n_intervals=0, disabled=True
            ),
            # Store for animation state
            dcc.Store(
                id="choropleth-animation-state",
                data={"playing": False, "current_year": 2006},
            ),
            # County Heatmap Section
            html.Div(
                [
                    html.Div(
                        [
                            html.H2(
                                "County-level Prescription Patterns",
                                style={
                                    "fontSize": "32px",
                                    "fontWeight": "600",
                                    "marginBottom": "20px",
                                    "textAlign": "center",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.P(
                                "Explore how ADHD prescription rates vary across Swedish counties over time. Use the controls on the left to filter by medications and demographics. The visualization automatically adapts: selecting all counties shows a heatmap for regional comparison and hotspot identification, while selecting one county displays its trend over time in a line chart.",
                                style={
                                    "fontSize": "16px",
                                    "textAlign": "center",
                                    "marginBottom": "40px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Div(
                                [
                                    # Heatmap controls sidebar (left side)
                                    html.Div(
                                        [
                                            # Medication settings for heatmap
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Medication:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.Dropdown(
                                                        id="heatmap-medication-dropdown",
                                                        options=medication_options,
                                                        value="All medications",
                                                        style={
                                                            "minWidth": "200px",
                                                            "boxShadow": "none",
                                                            "backgroundColor": BG_COLOR,
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "20px"},
                                            ),
                                            # County settings for heatmap (converts to line)
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "County:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.Dropdown(
                                                        id="heatmap-county-dropdown",
                                                        options=county_options,
                                                        value="All counties",
                                                        style={
                                                            "minWidth": "200px",
                                                            "boxShadow": "none",
                                                            "backgroundColor": BG_COLOR,
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "20px"},
                                            ),
                                            # Sex selection for heatmap (single choice)
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Sex Selection:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.RadioItems(
                                                        id="heatmap-sex-radio",
                                                        options=[
                                                            {
                                                                "label": "Boys/Young men",
                                                                "value": "Boys",
                                                            },
                                                            {
                                                                "label": "Girls/Young women",
                                                                "value": "Girls",
                                                            },
                                                            {
                                                                "label": "Both sexes",
                                                                "value": "Both sexes",
                                                            },
                                                        ],
                                                        value="Both sexes",  # default selected
                                                        inline=False,
                                                        inputStyle={
                                                            "margin-right": "8px"
                                                        },
                                                        style={
                                                            "color": TEXT_COLOR,
                                                            "accent-color": "#4ADFB2",
                                                        },
                                                    ),
                                                ],
                                                style={"marginBottom": "20px"},
                                            ),
                                            # Age settings for heatmap
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Age Groups:",
                                                        style={
                                                            "fontSize": "16px",
                                                            "fontWeight": "500",
                                                            "marginBottom": "8px",
                                                            "display": "block",
                                                            "color": TEXT_COLOR,
                                                        },
                                                    ),
                                                    dcc.RadioItems(
                                                        id="heatmap-age-radio",
                                                        options=[
                                                            {
                                                                "label": "5-9",
                                                                "value": "5-9",
                                                            },
                                                            {
                                                                "label": "10-14",
                                                                "value": "10-14",
                                                            },
                                                            {
                                                                "label": "15-19",
                                                                "value": "15-19",
                                                            },
                                                            {
                                                                "label": "20-24",
                                                                "value": "20-24",
                                                            },
                                                        ],
                                                        value="10-14",
                                                        inline=False,
                                                        inputStyle={
                                                            "margin-right": "8px"
                                                        },
                                                        style={
                                                            "color": TEXT_COLOR,
                                                            "accent-color": "#4ADFB2",
                                                        },
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style={
                                            "flex": "0 0 220px",
                                            "display": "flex",
                                            "flexDirection": "column",
                                            "alignItems": "flex-start",
                                            "paddingRight": "20px",
                                            "marginTop": "160px",
                                        },
                                    ),
                                    # County heatmap chart (right side)
                                    html.Div(
                                        [
                                            dcc.Graph(
                                                id="county-heatmap",
                                                style={
                                                    "backgroundColor": BG_COLOR,
                                                    "borderRadius": "12px",
                                                    "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
                                                },
                                            ),
                                            html.P(
                                                id="county-heatmap-note",
                                                children="Note: The number displayed at the end of each line (e.g., 'x6', six times higher) indicates the change between the first and the last year for which data are available.",
                                                style={
                                                    "fontSize": "11px",
                                                    "color": TEXT_COLOR,
                                                    "fontStyle": "italic",
                                                    "marginTop": "10px",
                                                    "marginLeft": "20px",
                                                    "display": "none",  # Hidden by default
                                                },
                                            ),
                                        ],
                                        style={"flex": "1"},
                                    ),
                                ],
                                style={"display": "flex", "alignItems": "flex-start"},
                            ),
                        ],
                        style=chart_container_style,
                    )
                ],
                style=chart_section_style,
            ),
            # Analysis Section
            html.Div(
                [
                    html.H2(
                        "Key Observations",
                        style={
                            "fontSize": "32px",
                            "fontWeight": "600",
                            "marginBottom": "30px",
                            "color": TEXT_COLOR,
                        },
                    ),
                    html.Ul(
                        [
                            html.Li(
                                "Halland has the highest rate of ADHD medication use at 13.3% in 2024 among boys aged 10-14, while Västernorrland has the lowest at 6.0% — a 2.2-fold difference.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "Among girls/young women, the highest rates are seen in ages 15-19 in Gotland at 12.5%, while Västernorrland again has the lowest at 5.6% — also a 2.2-fold difference.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "Both groups above show a standard deviation of approximately 19 per 1,000, indicating substantial and widespread regional variation in prescribing practices across Swedish counties.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                            html.Li(
                                "Gotland has the highest ADHD medication use among both sexes for ages 15-19 at 11.6%, with Dalarna a close second at 11.4% and Halland in third place at 10.2%.",
                                style={
                                    "marginBottom": "15px",
                                    "fontSize": "17px",
                                    "color": TEXT_COLOR,
                                },
                            ),
                        ],
                        style={"color": TEXT_COLOR, "paddingLeft": "30px"},
                    ),
                ],
                style=section_style,
            ),
            # References + Resources
            html.Div(
                [
                    html.Div(
                        [
                            # Centered heading
                            html.Div(
                                html.B("References + Resources"),
                                style={
                                    "fontSize": "22px",
                                    "fontWeight": "bold",
                                    "textAlign": "center",
                                },
                            ),
                            html.Br(),
                            html.Br(),
                            # Literature references
                            html.P(
                                "[1] Chan, A.Y.L., Tian, H., & Bedoya, C.A. (2023). Attention-deficit/hyperactivity disorder medication consumption in 64 countries and regions from 2015 to 2019: a longitudinal study. The Lancet eClinicalMedicine, 77, 100-110."
                            ),
                            html.P(
                                "[2] Socialstyrelsen [National Board of Health and Welfare]. (2024). Nationella riktlinjer. Adhd och autism. [National Guidelines. Adhd and Autism]."
                            ),
                            html.P(
                                "[3] Faraone, S.V., et al. (2021). The World Federation of ADHD International Consensus Statement: 208 Evidence-Based Conclusions about the Disorder. World Psychiatry, 20(4), 456-504."
                            ),
                            html.P(
                                "[4] Socialstyrelsen [National Board of Health and Welfare]. (2023). Diagnostik och läkemedelsbehandling vid ADHD. Förekomst, trend och könsskillnader. [Diagnostics and Drug Treatment of ADHD. Prevalence, Trends and Sex Differences]."
                            ),
                            html.P(
                                "[5] Rydell, M., Lundström, S., Gillberg, C., Lichtenstein, P., & Larsson, H. (2018). Has the Attention Deficit Hyperactivity Disorder Phenotype Become More Common in Children Between 2004 and 2014? Trends Over 10 Years From a Swedish General Population Sample. Journal of Child Psychology and Psychiatry, 59, 863–871."
                            ),
                            html.P(
                                "[6] Engström, I. (2025). Explosive increase in diagnosis and treatment of ADHD in Sweden may be related to private health providers offering fast-track, guaranteed diagnoses. Acta Paediatrica, 114(9), 2095–2097."
                            ),
                            # Data sources
                            html.P(
                                [
                                    "Läkemedel [internet]. Stockholm: Socialstyrelsen; 2025. [cited: 2020-10-12]. Available from: ",
                                    html.A(
                                        "https://www.socialstyrelsen.se/statistik-och-data/statistik/statistikdatabasen",
                                        href="https://www.socialstyrelsen.se/statistik-och-data/statistik/statistikdatabasen",
                                        target="_blank",
                                        style={
                                            "color": "#B8E6F7",
                                            "textDecoration": "underline",
                                        },
                                    ),
                                ]
                            ),
                            html.P(
                                [
                                    "Socialstyrelsen (2025). Tolka: Läkemedelsdata. ",
                                    html.A(
                                        "sdb.socialstyrelsen.se/pages/listinfo.aspx?amne=lak&id=TOLKA&sprak=",
                                        href="https://sdb.socialstyrelsen.se/pages/listinfo.aspx?amne=lak&id=TOLKA&sprak=",
                                        target="_blank",
                                        style={
                                            "color": "#B8E6F7",
                                            "textDecoration": "underline",
                                        },
                                    ),
                                ],
                            ),
                            # Github section
                            html.P(
                                [
                                    "The data behind all graphs is based on open data from ",
                                    html.I(
                                        "The Swedish National Board of Health and Welfare (Socialstyrelsen)"
                                    ),
                                    ". Aggregated data were downloaded directly from Socialstyrelsen's webpage for the ",
                                    '"All ADHD medication"',
                                    " category to avoid double-counting patients across individual medication types. Individual medication data (by ATC codes) were extracted via Socialstyrelsen's official API with my custom Python module, ",
                                    html.A(
                                        "available on Github",
                                        href="https://github.com/Bengtegard/swedish-adhd-medication-data",
                                        target="_blank",
                                        style={"color": "#B8E6F7"},
                                    ),
                                    " (MIT License).",
                                ],
                                style={"marginTop": "40px"},
                            ),
                            html.P(
                                [
                                    "This dashboard is built using Dash and Plotly Express. The data and code behind this project ",
                                    html.A(
                                        "are available on Github",
                                        href="https://github.com/Bengtegard/adhd_meds_sweden.git",
                                        target="_blank",
                                        style={"color": "#B8E6F7"},
                                    ),
                                    " (MIT License). "
                                    "Feel free to contribute by sending a pull request on GitHub or re-use the code for your own dashboards.",
                                ]
                            ),
                        ],
                        style=conclusion_references_style,
                    )
                ],
                style=conclusion_section_style,
            ),
        ],
        style=story_style,
    )

    return layout
