# ============================================================================
# CALLBACKS FOR DASH APP
# ============================================================================
# This file contains all @app.callback functions for updating figures,
# animations, heatmaps, and interactive components.
# ============================================================================

import dash
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import json

from config import BG_COLOR, TEXT_COLOR, FACET_COLORS, FACET_TITLE_MAP,GENDER_COLORS, bengtegard_template

# Import data processing functions
from data_processing import (
    load_processed_csv,
    load_and_process_all_data,
    create_cumulative_data,
    make_label,
    load_geojson
)

# Import visualization helpers
from visualizations import (
    plot_gender_ratios,
    prepare_choropleth_data,
    get_national_trend_context
)

# ============================================================================
# LOAD AND PROCESS DATA
# ============================================================================

# Load raw CSV
df_raw = load_processed_csv()

# Process national and regional datasets
df_grouped, df_grouped_regional = load_and_process_all_data(df_raw)

# Load GeoJson map of Sweden counties
geojson_counties = load_geojson()

# ============================================================================
# 1. LINE CHART ANIMATION
# ============================================================================


def register_callbacks(app, df_grouped, df_grouped_regional, geojson_counties):
    @app.callback(
        Output('line-animation', 'figure'),
        [
            Input('medication-dropdown', 'value'),
            Input('gender-checklist', 'value'),
            Input('age-checklist', 'value')
        ]
    )
    def update_line_chart(selected_medication, selected_genders, selected_ages):
        """Update main line animation chart based on user selections."""
        
        # Handle 'separator' selection
        if selected_medication == 'separator':
            selected_medication = 'All medications'
        
        # Filter data
        df_filtered = df_grouped[
            (df_grouped['medication_category'] == selected_medication) &
            (df_grouped['gender'].isin(selected_genders)) &
            (df_grouped['age_group'].isin(selected_ages))
        ]
        
        # Prepare cumulative data for animation
        df_anim = create_cumulative_data(df_filtered)
        df_anim["Label"] = df_anim.apply(make_label, axis=1)

        # Assign colors to labels
        label_colors = {}
        for label in df_anim['Label'].unique():
            if label.startswith("Boys") or label.startswith("Young men"):
                label_colors[label] = GENDER_COLORS["Boys"]
            elif label.startswith("Girls") or label.startswith("Young women"):
                label_colors[label] = GENDER_COLORS["Girls"]
            elif label.startswith("Both"):
                label_colors[label] = GENDER_COLORS["Both genders"]

        # Set y-axis range with 10% padding
        y_max = df_anim["patients_per_1000"].max()
        y_range = [0, y_max * 1.1]

        # Create line figure
        line_fig = px.line(
            df_anim,
            x="year",
            y="patients_per_1000",
            height=800,
            width=1000,
            color="Label",
            line_shape="spline",
            line_dash="Label",
            facet_row="age_group",
            animation_frame="Year",
            animation_group="Label",
            markers=True,
            title=f"ADHD Medication Prescriptions in Sweden - {selected_medication}",
            color_discrete_map=label_colors,
            range_x=[2006, 2024],
            range_y=y_range
        )

        # Layout and annotations
        line_fig.update_layout(
            legend_title_text="Gender",
            xaxis_title="Year",
            template="bengtegard",
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=BG_COLOR,
            font_color=TEXT_COLOR,
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 250, "redraw": False},
                                        "transition": {"duration": 240, "easing": "linear"}}],
                        "method": "animate",
                        "label": "▶"
                    },
                    {
                        "args": [[None], {"mode": "immediate", "frame": {"duration": 0, "redraw": False},
                                        "transition": {"duration": 0}}],
                        "method": "animate",
                        "label": "❚❚"
                    }
                ],
                "direction": "left",
                "showactive": True,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }]
        )

        # Update traces and y-axis
        line_fig.update_traces(cliponaxis=False, connectgaps=True, line_shape="spline", 
        line=dict(smoothing=1.3))
        line_fig.update_yaxes(title_text='', tick0=0, dtick=15, range=y_range)

        # Customize facet titles
        for a in line_fig.layout.annotations:
            if a.text.startswith("age_group="):
                age_group = a.text.split("=")[1]
                a.text = FACET_TITLE_MAP[age_group]
                a.font.color = FACET_COLORS[age_group]

        # Add y-axis label annotation
        line_fig.add_annotation(
            x=-0.08, y=0.5,
            text="Patients per 1000 inhabitants",
            showarrow=False,
            textangle=-90,
            xref="paper",
            yref="paper",
            font=dict(size=14, color=TEXT_COLOR)
        )

        return line_fig

    # ============================================================================
    # 2. COUNTY-LEVEL HEATMAP
    # ============================================================================

    @app.callback(
        Output('county-heatmap', 'figure'),
        [
            Input('heatmap-medication-dropdown', 'value'),
            Input('heatmap-county-dropdown', 'value'),
            Input('heatmap-gender-radio', 'value'),
            Input('heatmap-age-radio', 'value')
        ]
    )
    def update_heatmap(selected_medication, selected_county, selected_gender, selected_age):
        """Update county-level heatmap for selected medication, gender, and age."""
        
        if selected_medication == 'separator':
            selected_medication = 'All medications'

        df_heat = df_grouped_regional[
            (df_grouped_regional['medication_category'] == selected_medication) &
            (df_grouped_regional['gender'] == selected_gender) &
            (df_grouped_regional['age_group'] == selected_age)
        ].copy()

        df_heat["year"] = df_heat["year"].astype(str)

        # Heatmap if all counties
        if selected_county == "All counties":
            heatmap_fig = px.density_heatmap(
                df_heat,
                x="year",
                y="county",
                z="patients_per_1000",
                nbinsx=len(df_heat["year"].unique()),
                text_auto=False,
                color_continuous_scale="YlGnBu"
            )

            heatmap_fig.update_layout(
                title={"text": f"ADHD Prescriptions in Sweden by County<br><sup>{selected_medication}, {selected_gender}, Age {selected_age}</sup>",
                    "x": 0.5, "xanchor": "center"},
                xaxis_title="Year",
                yaxis_title="County",
                height=800,
                width=1000,
                template='bengtegard',
                paper_bgcolor=BG_COLOR,
                plot_bgcolor=BG_COLOR,
                font_color=TEXT_COLOR,
                coloraxis_colorbar=dict(title="Patients per 1000")
            )

            heatmap_fig.update_xaxes(tickmode="array", tickvals=df_heat["year"].unique(), ticktext=df_heat["year"].unique())
            heatmap_fig.update_yaxes(title_standoff=4, automargin=True)
        # Line chart if single county
        else:
            df_single = df_heat[df_heat['county'] == selected_county]
            heatmap_fig = px.line(
                df_single,
                x="year",
                y="patients_per_1000",
                color="age_group",
                markers=True,
                title=f"ADHD Prescriptions Over Time for {selected_county} ({selected_medication}, {selected_gender})"
            )
            heatmap_fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Patients per 1000",
                height=700,
                width=1000,
                template='bengtegard',
                paper_bgcolor=BG_COLOR,
                plot_bgcolor=BG_COLOR,
                font_color=TEXT_COLOR
            )
            heatmap_fig.update_xaxes(tickmode="array", tickvals=df_single["year"].unique(), ticktext=df_single["year"].unique())
            heatmap_fig.update_yaxes(tick0=0, dtick=5)

        return heatmap_fig

    # ============================================================================
    # 3. GENDER RATIO PLOT
    # ============================================================================

    @app.callback(
        Output('gender-ratio-plot', 'figure'),
        Input('ratio-medication-dropdown', 'value')
    )
    def update_gender_ratio(selected_medication):
        """Update the gender ratio chart based on medication selection."""
        
        if selected_medication == 'separator':
            selected_medication = 'All medications'
        
        df_filtered = df_grouped[df_grouped['medication_category'] == selected_medication]
        fig = plot_gender_ratios(df_filtered)

        fig.update_layout(title=f'Boys-to-Girls ADHD Prescription Ratio by Age Group - {selected_medication}')
        return fig

    # ============================================================================
    # 4. CHOROPLETH MAP
    # ============================================================================

    @app.callback(
        [Output('choropleth-map', 'figure'),
        Output('choropleth-stats', 'children')],
        [
            Input('choropleth-year-slider', 'value'),
            Input('choropleth-gender-radio', 'value'),
            Input('choropleth-age-radio', 'value')
        ]
    )
    def update_choropleth(year, gender, age_group):
        """Update choropleth map and statistics based on selections."""
        
        if geojson_counties is None:
            fig = go.Figure()
            fig.add_annotation(text="GeoJSON file not found.", xref="paper", yref="paper",
                            x=0.5, y=0.5, xanchor='center', yanchor='middle',
                            showarrow=False, font_size=16)
            fig.update_layout(height=700, template='bengtegard', paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
            stats = html.Div([html.H4("GeoJSON file missing", style={'color': 'red'})])
            return fig, stats

        df_map = prepare_choropleth_data(df_grouped_regional, year, age_group, gender)
        if df_map.empty:
            fig = go.Figure()
            fig.add_annotation(text="No data available for selected parameters",
                            xref="paper", yref="paper",
                            x=0.5, y=0.5, xanchor='center', yanchor='middle',
                            showarrow=False, font_size=16)
            fig.update_layout(height=700, template='bengtegard', paper_bgcolor=BG_COLOR, font_color=TEXT_COLOR)
            stats = html.Div([html.H4("No data available", style={'color': 'red'})])
            return fig, stats

        # Max for color scale
        max_all = df_grouped_regional[df_grouped_regional['medication_category'] == 'All medications']['patients_per_1000'].max()
        color_scale_max = max_all * 1.1

        # National trend context
        trend_context = get_national_trend_context(df_grouped_regional, year, age_group, gender)

        # Create choropleth figure
        map_fig = px.choropleth(
            df_map,
            geojson=geojson_counties,
            locations='county_geo',
            featureidkey="properties.name",
            color='patients_per_1000',
            color_continuous_scale=px.colors.sequential.OrRd,
            range_color=[0, color_scale_max],
            labels={'patients_per_1000': 'Patients per 1000'},
            hover_name='county',
            hover_data={'county_geo': False, 'patients_per_1000': ':.1f'},
        )

        # Layout, annotations, and stats
        map_fig.update_geos(fitbounds="locations", projection_type="natural earth", visible=False, bgcolor=BG_COLOR)
        map_fig.update_traces(marker_line_width=1, marker_line_color="white",
                            hovertemplate="<b>%{hovertext}</b><br>Patients per 1000: %{z:.1f}<extra></extra>")
        map_fig.update_layout(
            height=600, width=900, margin={"r":0,"t":50,"l":0,"b":0},
            paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR, font_color=TEXT_COLOR,
            transition={'duration': 900, 'easing': 'cubic-in-out'},
            template=bengtegard_template,
            title={
                'text': f'ADHD Prescription Rates by County ({gender}, Age {age_group})<br>{year}',
                'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
            },
            coloraxis_colorbar=dict(title="Patients per 1000", thickness=11, len=0.7, x=0.8, tickmode="linear", tick0=0, dtick=20, tickformat=".1f")
        )
        map_fig.add_annotation(text=trend_context, xref="paper", yref="paper", x=0.04, y=0.94,
                            showarrow=False, font=dict(size=14, color=TEXT_COLOR),
                            bgcolor=BG_COLOR, bordercolor=BG_COLOR)

        # Statistics summary
        if len(df_map) > 0:
            highest_county = df_map.loc[df_map['patients_per_1000'].idxmax(), 'county']
            highest_rate = df_map['patients_per_1000'].max()
            lowest_county = df_map.loc[df_map['patients_per_1000'].idxmin(), 'county']
            lowest_rate = df_map['patients_per_1000'].min()
            std_rate = df_map['patients_per_1000'].std()

            stats = html.Div([
                html.H4(f"Statistics for {year}", style={'marginBottom': 15, 'color': TEXT_COLOR}),
                html.Div([html.Div([html.Strong("Highest Rate: "), f"{highest_county} ({highest_rate:.1f} per 1000)"],
                                style={'marginBottom': 5, 'color': TEXT_COLOR}),
                        html.Div([html.Strong("Lowest Rate: "), f"{lowest_county} ({lowest_rate:.1f} per 1000)"],
                                style={'marginBottom': 5, 'color': TEXT_COLOR}),
                        html.Div([html.Strong("Standard Deviation: "), f"{std_rate:.1f}"],
                                style={'marginBottom': 5, 'color': TEXT_COLOR})])
            ])
        else:
            stats = html.Div([html.H4("No data available", style={'color': TEXT_COLOR})])

        return map_fig, stats

    # ============================================================================
    # 5. CHOROPLETH ANIMATION CONTROLS
    # ============================================================================

    @app.callback(
        [Output('choropleth-interval', 'disabled'),
        Output('choropleth-animation-state', 'data')],
        [Input('choropleth-play-btn', 'n_clicks'),
        Input('choropleth-pause-btn', 'n_clicks')],
        [State('choropleth-animation-state', 'data'),
        State('choropleth-year-slider', 'value')]
    )
    def control_choropleth_animation(play_clicks, pause_clicks, current_state, current_year):
        """Play/pause controls for choropleth animation."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return True, current_state

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'choropleth-play-btn':
            return False, {'playing': True, 'current_year': 2006}
        elif button_id == 'choropleth-pause-btn':
            return True, {'playing': False, 'current_year': current_year}
        return True, current_state

    @app.callback(
        Output('choropleth-year-slider', 'value'),
        [Input('choropleth-interval', 'n_intervals')],
        [State('choropleth-animation-state', 'data'),
        State('choropleth-year-slider', 'value')]
    )
    def animate_choropleth_year(n_intervals, animation_state, current_year):
        """Automatically increment year for choropleth animation."""
        if not animation_state.get('playing', False):
            return current_year

        next_year = current_year + 1
        if next_year > 2024:
            return 2024
        return next_year
