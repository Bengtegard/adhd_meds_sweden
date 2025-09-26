# layouts.py

import dash
from dash import html, dcc
from config import BG_COLOR, TEXT_COLOR, COUNTY_MAP

# ============================================================================
# STYLE DEFINITIONS
# ============================================================================

story_style = {
    'fontFamily': 'monospace',
    'backgroundColor': BG_COLOR,
    'color': TEXT_COLOR,
    'lineHeight': '1.6',
    'margin': '0',
    'padding': '0'
}

section_style = {
    'maxWidth': '800px',
    'margin': '0 auto',
    'padding': '60px 40px',
    'backgroundColor': BG_COLOR,
    'color': TEXT_COLOR
}

hero_style = {
    'textAlign': 'center',
    'padding': '100px 40px 80px',
    'background': "#FFFFE0",
    'color': TEXT_COLOR,
    'marginBottom': '0'
}

chart_section_style = {
    'backgroundColor': '#FFFFEF',
    'padding': '60px 0',
    'marginBottom': '0'
}

chart_container_style = {
    'maxWidth': '1100px',
    'margin': '0 auto',
    'padding': '0 40px'
}

controls_style = {
    'backgroundColor': '#FFFFEF',
    'padding': '30px',
    'borderRadius': '12px',
    'marginBottom': '30px',
    'display': 'flex',
    'gap': '30px',
    'alignItems': 'center',
    'flexWrap': 'wrap',
    'color': TEXT_COLOR
}

# ============================================================================
# APP LAYOUT
# ============================================================================

# Define medication options for dropdowns
medication_options = [
    {'label': 'All medications', 'value': 'All medications'},
    {'label': '── Individual Medications ──', 'value': 'separator', 'disabled': True},
    {'label': 'Methylphenidate', 'value': 'Methylphenidate'},
    {'label': 'Lisdexamfetamine', 'value': 'Lisdexamfetamine'},
    {'label': 'Dextroamphetamine', 'value': 'Dextroamphetamine'},
    {'label': 'Atomoxetine', 'value': 'Atomoxetine'},
    {'label': 'Guanfacine', 'value': 'Guanfacine'}
]

# Define county options for dropdown
county_options = (
    [{'label': 'All counties', 'value': 'All counties'},
     {'label': '── Individual Counties ──', 'value': 'separator', 'disabled': True}]
    + [{'label': short_name, 'value': short_name} for short_name in COUNTY_MAP.values()]
)

# Define the layout
def create_layout():
    layout = html.Div([
        
        # Hero Section
        html.Div([
            html.H1("The Evolution of ADHD Treatment in Sweden", 
                style={'fontSize': '48px', 'fontWeight': '700', 'marginBottom': '20px', 'color': TEXT_COLOR}),
            html.P("A Demographic Analysis", 
                style={'fontSize': '24px', 'fontWeight': '300', 'marginBottom': '30px', 'color': TEXT_COLOR}),
            html.P("How have ADHD medication prescription patterns changed across different demographics in Sweden from 2006 to 2024?", 
                style={'fontSize': '18px', 'maxWidth': '600px', 'margin': '0 auto', 'color': TEXT_COLOR})
        ], style=hero_style),
        
        # Introduction Section #!!! At least one time per year....
        html.Div([
            html.H2("Understanding the Data", style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '30px', 'color': TEXT_COLOR}),
            html.P(["This project uses open data from", html.I(" the Swedish National Board of Health and Welfare (Socialstyrelsen) "), "Statistikdatabas för läkemedel, which records all prescription medications dispensed in Sweden since 2006. Data were extracted via Socialstyrelsen's API using a custom Python module, allowing separate retrieval of prescription data for each ADHD medication. The analysis tracks the annual number of individuals filling ADHD prescriptions as a proxy for diagnosis and treatment rates, examining whether growth in medication use varies across developmental periods and between genders."], 
                style={'fontSize': '18px', 'marginBottom': '25px', 'color': TEXT_COLOR}),
            html.P([
            "Five ADHD medications are ",
            html.A(
                "currently approved in Sweden",
                href="https://www.lakemedelsverket.se/sv/behandling-och-forskrivning/behandlingsrekommendationer/sok-behandlingsrekommendationer/lakemedel-vid-adhd--behandlingsrekommendation",
                target="_blank",
                style={'color': TEXT_COLOR, 'textDecoration': 'underline'}
            ),
            ": three central nervous system stimulants (methylphenidate, dextroamphetamine, lisdexamfetamine) and two non-stimulants (atomoxetine, guanfacine). The dataset allows separate analysis for each medication, though active ingredients may appear under multiple brand names."
        ],
        style={'fontSize': '18px', 'color': TEXT_COLOR})
        ,
            html.P("All rates are expressed as patients per 1,000 inhabitants, enabling comparisons across time and counties. Some demographic subgroups may exceed 1,000 patients per 1,000 inhabitants due to population and age-group definitions (Socialstyrelsen, 2025).", 
                style={'fontSize': '18px', 'color': TEXT_COLOR})
        ], style=section_style),
        
        # Interactive Chart Section
        html.Div([
            html.Div([
                html.H2("Prescription Trends Over Time", 
                    style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '20px', 'textAlign': 'center', 'color': TEXT_COLOR}),
                html.P("Use the controls on the left to explore different medications and demographics. The chart shows the number of individuals using ADHD medications — those who have filled at least one ADHD prescription in a given year, regardless of prior prescriptions. Each person is counted once per year, allowing you to track trends and changes in medication use over time.", 
                    style={'fontSize': '18px', 'textAlign': 'center', 'marginBottom': '40px', 'color': TEXT_COLOR}),
                html.Div([
                    # Sidebar with all controls stacked vertically
                    html.Div([
                        # Medication settings
                        html.Div([
                            html.Label("Medication:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.Dropdown(
                                id='medication-dropdown',
                                options=medication_options,
                                value='All medications',
                                style={
                                    'minWidth': '200px',
                                    'boxShadow': 'none',
                                    'backgroundColor': BG_COLOR, 
                                    'color': TEXT_COLOR
                                }
                            )
                        ], style={'marginBottom': '20px'}),

                        # Gender settings
                        html.Div([
                            html.Label("Gender Selection:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.Checklist(
                                id='gender-checklist',
                                options=[
                                    {'label': 'Boys/Young men', 'value': 'Boys'},
                                    {'label': 'Girls/Young women', 'value': 'Girls'},
                                    {'label': 'Both Genders', 'value': 'Both genders'}
                                ],
                                value=['Both genders'],
                                inline=False,
                                inputStyle={"margin-right": "8px"},
                                style={
                                    'color': TEXT_COLOR,
                                    'accent-color': "#4ADFB2"}
                            )
                        ], style={'marginBottom': '20px'}),

                        # Age settings
                        html.Div([
                            html.Label("Age Groups:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.Checklist(
                                id='age-checklist',
                                options=[
                                    {'label': '5-9', 'value': '5-9'},
                                    {'label': '10-14', 'value': '10-14'},
                                    {'label': '15-19', 'value': '15-19'},
                                    {'label': '20-24', 'value': '20-24'}
                                ],
                                value=['10-14'],
                                inline=False,
                                inputStyle={"margin-right": "8px"},
                                style={
                                    'color': TEXT_COLOR,
                                    'accent-color': '#4ADFB2'}
                            )
                        ])
                    ], style={
                        'flex': '0 0 220px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'flex-start',
                        'paddingRight': '20px',
                        'marginTop': '160px'
                    }),

                    # Line chart (right side)
                    html.Div([
                        dcc.Graph(
                            id='line-animation',
                            style={
                                'backgroundColor': BG_COLOR, 
                                'borderRadius': '12px', 
                                'boxShadow': '0 4px 12px rgba(0,0,0,0.3)'
                            }
                        )
                    ], style={'flex': '1'})
                ], style={'display': 'flex', 'alignItems': 'flex-start'})
                
            ], style=chart_container_style)
        ], style=chart_section_style),

        # Interactive Choropleth Map Section
        html.Div([
            html.Div([
                html.H2("Geographic Distribution of ADHD Prescriptions", 
                    style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '20px', 'textAlign': 'center', 'color': TEXT_COLOR}),
                html.P("Explore how ADHD prescription rates vary across Swedish counties. The map shows total ADHD prescriptions using a fixed continuous color scale for consistent comparison over time. Subtle differences within a single year may be less visible. Filter by demographics and age group, and click play to watch changes over time.", 
                    style={'fontSize': '18px', 'textAlign': 'center', 'marginBottom': '40px', 'color': TEXT_COLOR}),
                
                html.Div([
                    # Choropleth controls sidebar (left side)
                    html.Div([
                        
                        # Gender selection for choropleth (single choice)
                        html.Div([
                            html.Label("Gender Selection:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.RadioItems(
                                id='choropleth-gender-radio',
                                options=[
                                    {'label': 'Boys/Young men', 'value': 'Boys'},
                                    {'label': 'Girls/Young women', 'value': 'Girls'},
                                    {'label': 'Both genders', 'value': 'Both genders'}
                                ],
                                value='Both genders',
                                inline=False,
                                inputStyle={"margin-right": "8px"},
                                style={'color': TEXT_COLOR, 'accent-color': "#4ADFB2"}
                            )
                        ], style={'marginBottom': '20px'}),

                        # Age settings for choropleth
                        html.Div([
                            html.Label("Age Groups:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.RadioItems(
                                id='choropleth-age-radio',
                                options=[
                                    {'label': '5-9', 'value': '5-9'},
                                    {'label': '10-14', 'value': '10-14'},
                                    {'label': '15-19', 'value': '15-19'},
                                    {'label': '20-24', 'value': '20-24'}
                                ],
                                value='10-14',
                                inline=False,
                                inputStyle={"margin-right": "8px"},
                                style={'color': TEXT_COLOR, 'accent-color': '#4ADFB2'}
                            )
                        ], style={'marginBottom': '30px'}),
                        
                        # Animation controls
                        html.Div([
                            html.Label("Animation:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            html.Div([
                                html.Button('▶', id='choropleth-play-btn', n_clicks=0,
                                        style={'marginRight': '8px', 'padding': '6px 12px', 'fontSize': '12px', 'backgroundColor': '#4ADFB2', 'color': BG_COLOR, 'border': 'none', 'borderRadius': '4px'}),
                                html.Button('❚❚', id='choropleth-pause-btn', n_clicks=0,
                                        style={'marginRight': '7px', 'padding': '6px 12px', 'fontSize': '11px', 'backgroundColor': TEXT_COLOR, 'color': 'white', 'border': 'none', 'borderRadius': '4px'}),
                            ])
                        ], style={'marginBottom': '20px'})
                        
                    ], style={
                        'flex': '0 0 220px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'flex-start',
                        'paddingRight': '20px',
                        'marginTop': '130px'
                    }),

                    # Choropleth map and controls (right side)
                    html.Div([
                        # Year slider
                        html.Div([
                            html.Label(f"Year: ", style={'fontWeight': 'bold', 'marginBottom': '10px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.Slider(
                                id='choropleth-year-slider',
                                min=2006,
                                max=2024,
                                step=1,
                                value=2006,
                                marks={year: {'label': str(year), 'style': {'color': TEXT_COLOR}} for year in range(2006, 2025, 3)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ], style={'marginBottom': '30px'}),
                        
                        # Map
                        dcc.Graph(
                            id='choropleth-map',
                            style={'backgroundColor': BG_COLOR, 'borderRadius': '12px', 'boxShadow': '0 4px 12px rgba(0,0,0,0.3)'}
                        ),
                        
                        # Statistics summary
                        html.Div(id='choropleth-stats', style={
                            'marginTop': '20px', 
                            'padding': '15px', 
                            'backgroundColor': '#FFFFEF', 
                            'borderRadius': '8px',
                            'color': TEXT_COLOR
                        })
                    ], style={'flex': '1'})
                ], style={'display': 'flex', 'alignItems': 'flex-start'})
                
            ], style=chart_container_style)
        ], style=chart_section_style),
        
        # Interval component for choropleth animation
        dcc.Interval(
            id='choropleth-interval',
            interval=1000,
            n_intervals=0,
            disabled=True
        ),
        
        # Store for animation state
        dcc.Store(id='choropleth-animation-state', data={'playing': False, 'current_year': 2006}),

        # Analysis Section
        html.Div([
            html.H2("Key Observations", style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '30px', 'color': TEXT_COLOR}),
            html.P("The data reveals several important trends in Swedish ADHD treatment patterns:", 
                style={'fontSize': '18px', 'marginBottom': '25px', 'color': TEXT_COLOR}),
            
            html.Ul([
                html.Li("Prescription rates have increased significantly across all age groups since 2006", style={'marginBottom': '15px', 'fontSize': '16px', 'color': TEXT_COLOR}),
                html.Li("Young adults (20-24) show the steepest growth in recent years", style={'marginBottom': '15px', 'fontSize': '16px', 'color': TEXT_COLOR}),
                html.Li("Gender patterns vary considerably by age group and medication type", style={'marginBottom': '15px', 'fontSize': '16px', 'color': TEXT_COLOR}),
                html.Li("Methylphenidate remains the most commonly prescribed ADHD medication", style={'marginBottom': '15px', 'fontSize': '16px', 'color': TEXT_COLOR}),
                html.Li("Individual medication analysis reveals distinct prescription patterns for different active ingredients", style={'marginBottom': '15px', 'fontSize': '16px', 'color': TEXT_COLOR})
            ], style={'color': TEXT_COLOR, 'paddingLeft': '30px'})
        ], style=section_style),
        
        # County Heatmap Section
        html.Div([
            html.Div([
                html.H2("County-level Prescription Patterns", 
                    style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '20px', 'textAlign': 'center', 'color': TEXT_COLOR}),
                html.P("Explore how ADHD prescription rates vary across Swedish counties over time. Use the controls below to filter the data by different medications and demographics.", 
                    style={'fontSize': '18px', 'textAlign': 'center', 'marginBottom': '40px', 'color': TEXT_COLOR}),
                
                html.Div([
                    # Heatmap controls sidebar (left side)
                    html.Div([
                        # Medication settings for heatmap
                        html.Div([
                            html.Label("Medication:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.Dropdown(
                                id='heatmap-medication-dropdown',
                                options=medication_options,
                                value='All medications',
                                style={
                                    'minWidth': '200px',
                                    'boxShadow': 'none',
                                    'backgroundColor': BG_COLOR, 
                                    'color': TEXT_COLOR
                                }
                            )
                        ], style={'marginBottom': '20px'}),
                        # County settings for heatmap (converts to line)
                        html.Div([
                            html.Label("County:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.Dropdown(
                                id='heatmap-county-dropdown',
                                options=county_options,
                                value='All counties',
                                style={
                                    'minWidth': '200px',
                                    'boxShadow': 'none',
                                    'backgroundColor': BG_COLOR, 
                                    'color': TEXT_COLOR
                                }
                            )
                        ], style={'marginBottom': '20px'}),   

                        # Gender selection for heatmap (single choice)
                        html.Div([
                            html.Label(
                                "Gender Selection:",
                                style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}
                            ),
                            dcc.RadioItems(
                                id='heatmap-gender-radio',
                                options=[
                                    {'label': 'Boys/Young men', 'value': 'Boys'},
                                    {'label': 'Girls/Young women', 'value': 'Girls'},
                                    {'label': 'Both genders', 'value': 'Both genders'}
                                ],
                                value='Both genders',  # default selected
                                inline=False,
                                inputStyle={"margin-right": "8px"},
                                style={'color': TEXT_COLOR, 'accent-color': "#4ADFB2"}
                            )
                        ], style={'marginBottom': '20px'}),

                        # Age settings for heatmap
                        html.Div([
                            html.Label("Age Groups:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                            dcc.RadioItems(
                                id='heatmap-age-radio',
                                options=[
                                    {'label': '5-9', 'value': '5-9'},
                                    {'label': '10-14', 'value': '10-14'},
                                    {'label': '15-19', 'value': '15-19'},
                                    {'label': '20-24', 'value': '20-24'}
                                ],
                                value='10-14',
                                inline=False,
                                inputStyle={"margin-right": "8px"},
                                style={
                                    'color': TEXT_COLOR,
                                    'accent-color': '#4ADFB2'}
                            )
                        ])
                    ], style={
                        'flex': '0 0 220px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'flex-start',
                        'paddingRight': '20px',
                        'marginTop': '160px'
                    }),

                    # county heatmap chart (right side)
                    html.Div([
                        dcc.Graph(
                            id='county-heatmap',
                            style={'backgroundColor': BG_COLOR, 'borderRadius': '12px', 'boxShadow': '0 4px 12px rgba(0,0,0,0.3)'}
                        )
                    ], style={'flex': '1'})
                ], style={'display': 'flex', 'alignItems': 'flex-start'})
                
            ], style=chart_container_style)
        ], style=chart_section_style),
        
        # Gender Ratio Section
        html.Div([
            html.Div([
                html.H2("Gender Disparities in Treatment", 
                    style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '20px', 'textAlign': 'center', 'color': TEXT_COLOR}),
                html.P("The Boys-to-Girls prescription ratio reveals important patterns about gender differences in ADHD diagnosis and treatment. A ratio above one indicates more boys receive prescriptions, while below one indicates more girls.", 
                    style={'fontSize': '18px', 'textAlign': 'center', 'marginBottom': '40px', 'color': TEXT_COLOR, 'maxWidth': '700px', 'margin': '0 auto 40px'}),
                
                # Gender ratio controls
                html.Div([
                    html.Label("Medication for Ratio Analysis:", style={'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '8px', 'display': 'block', 'color': TEXT_COLOR}),
                    dcc.Dropdown(
                        id='ratio-medication-dropdown',
                        options=medication_options,
                        value='All medications',
                        style={'maxWidth': '300px', 'margin': '0 auto', 'backgroundColor': BG_COLOR, 'color': TEXT_COLOR}
                    )
                ], style={'textAlign': 'center', 'marginBottom': '30px', 'backgroundColor': '#FFFFEF', 'padding': '20px', 'borderRadius': '8px'}),
                
                # Gender ratio chart
                dcc.Graph(
                    id='gender-ratio-plot',
                    style={'backgroundColor': BG_COLOR, 'borderRadius': '12px', 'boxShadow': '0 4px 12px rgba(0,0,0,0.3)'}
                )
                
            ], style=chart_container_style)
        ], style=chart_section_style),
        
        # Conclusion Section
        html.Div([
            html.H2("Implications and Future Directions", style={'fontSize': '32px', 'fontWeight': '600', 'marginBottom': '30px', 'color': TEXT_COLOR}),
            html.P("The evolution of ADHD treatment in Sweden reflects broader changes in diagnostic practices, treatment guidelines, and societal awareness. The significant increase in prescriptions across all demographics suggests both improved recognition of ADHD symptoms and potentially changing diagnostic criteria.", 
                style={'fontSize': '18px', 'marginBottom': '25px', 'color': TEXT_COLOR}),
            html.P("Individual medication analysis provides insights into prescribing preferences and treatment patterns, while the combined view shows overall healthcare utilization trends. Understanding these patterns is crucial for healthcare planning, resource allocation, and ensuring equitable access to ADHD treatment.", 
                style={'fontSize': '18px', 'marginBottom': '40px', 'color': TEXT_COLOR}),
            
            html.Div([
                html.P("Data Source: Swedish National Board of Health and Welfare", style={'fontSize': '14px', 'color': TEXT_COLOR, 'fontStyle': 'italic', 'textAlign': 'center', 'opacity': '0.8'}),
                html.P([
                    html.B("References"),
                    html.Br(),
                "Socialstyrelsen. Tolka: Läkemedelsdata. Accessed August 8 2025. ", "sdb.socialstyrelsen.se/pages/listinfo.aspx?amne=lak&id=TOLKA&sprak=", 
                ],
                style={'fontSize': '14px', 'color': TEXT_COLOR, 'fontStyle': 'italic', 'textAlign': 'center', 'opacity': '0.8'})
            ], style={'borderTop': f'1px solid {"#F7DFB8"}', 'paddingTop': '30px'})
        ], style=section_style)
        
    ], style=story_style)

    return layout