# ============================================================================
# CALLBACKS FOR DASH APP
# ============================================================================
# This file contains all @app.callback functions for updating figures,
# animations, heatmaps, and interactive components etc.
# ============================================================================

import dash
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

from config import (
    BG_COLOR,
    TEXT_COLOR,
    FACET_COLORS,
    FACET_TITLE_MAP,
    GENDER_COLORS,
    bengtegard_template,
)
from src.layouts import get_chart_container_style, get_controls_style

# Import data processing functions
from src.data_processing import (
    load_processed_csv,
    load_and_process_all_data,
    create_cumulative_data,
    load_geojson,
)

# Import visualization helpers
from src.visualizations import (
    plot_gender_ratios,
    prepare_choropleth_data,
    get_national_trend_context,
    apply_responsive_layout,
)

# ============================================================================
# LOAD AND PROCESS DATA
# ============================================================================

# Load raw CSV
df_raw = load_processed_csv()

# Process national and regional datasets
df_grouped_national, df_grouped_regional = load_and_process_all_data(df_raw)

# Load GeoJson map of Sweden counties
geojson_counties = load_geojson()

# ============================================================================
# 1. LINE CHART ANIMATION
# ============================================================================


def register_callbacks(app, df_grouped_national, df_grouped_regional, geojson_counties):

    # ============================================================================
    # UPDATE CHART AREA AND SIDEBARS DYNAMICALLY
    # ============================================================================

    @app.callback(
        Output("line-chart-container", "style"),
        Output("choropleth-chart-container", "style"),
        Output("heatmap-chart-container", "style"),
        Output("ratio-chart-container", "style"),
        Input("breakpoint", "widthBreakpoint"),
    )
    def update_all_chart_containers(breakpoint):
        """Dynamically adjust all chart container CSS for responsiveness."""

        # Base styles
        default_style = get_chart_container_style(breakpoint)

        if breakpoint == "desktop":
            line_style = get_chart_container_style(breakpoint, maxWidth="1100px")
        else:
            line_style = default_style

        if breakpoint == "desktop":
            ratio_style = get_chart_container_style(breakpoint, maxWidth="900px")
        elif breakpoint == "large":
            ratio_style = get_chart_container_style(breakpoint, maxWidth="1000px")
        else:
            ratio_style = default_style

        choropleth_style = default_style
        heatmap_style = default_style

        return line_style, choropleth_style, heatmap_style, ratio_style

    @app.callback(
        Output("line-controls-style", "style"),
        Output("choropleth-controls-style", "style"),
        Output("heatmap-controls-style", "style"),
        Input("breakpoint", "widthBreakpoint"),
    )
    def update_all_controls_style(breakpoint):
        style = get_controls_style(breakpoint)
        return style, style, style

    @app.callback(
        Output("line-animation", "figure"),
        [
            Input("medication-dropdown", "value"),
            Input("sex-checklist", "value"),
            Input("age-checklist", "value"),
            Input("breakpoint", "widthBreakpoint"),
        ],
        [
            State("breakpoint", "width"),
            State("breakpoint", "height"),
        ],
    )
    def update_line_chart(
        selected_medication, selected_genders, selected_ages, bp, width, height
    ):
        """Update main line animation chart based on user selections."""

        # Handle 'separator' selection
        if selected_medication == "separator":
            selected_medication = "All medications"

        # Filter data
        df_filtered = df_grouped_national[
            (df_grouped_national["medication_category"] == selected_medication)
            & (df_grouped_national["sex"].isin(selected_genders))
            & (df_grouped_national["age_group"].isin(selected_ages))
        ]

        # Prepare cumulative data for animation
        df_anim = create_cumulative_data(df_filtered)

        def make_simple_label(row):
            if row["sex"] == "Boys":
                return "Boys"
            elif row["sex"] == "Girls":
                return "Girls"
            else:
                return "Both"

        # Assign lables
        df_anim["Label"] = df_anim.apply(make_simple_label, axis=1)

        # Calulcate change from 2006 for hover
        df_anim["multiplier"] = df_anim.groupby(
            ["Label", "age_group", "medication_category"]
        )["patients_per_1000"].transform(
            lambda x: (x / x.iloc[0]).round(2) if any(x > 0) else float("nan")
        )

        # Assign colors to labels
        label_colors = {
            "Boys": GENDER_COLORS["Boys"],
            "Girls": GENDER_COLORS["Girls"],
            "Both": GENDER_COLORS["Both sexes"],
        }

        # Set y-axis range with 10% padding
        y_max = df_anim["patients_per_1000"].max()
        y_range = [0, y_max * 1.1]

        # Create line figure
        line_fig = px.line(
            df_anim,
            x="year",
            y="patients_per_1000",
            color="Label",
            line_shape="spline",
            facet_row="age_group",
            animation_frame="Year",
            animation_group="Label",
            markers=True,
            title=f"ADHD Medication Prescriptions in Sweden - {selected_medication}",
            color_discrete_map=label_colors,
            range_x=[2006, 2024],
            range_y=y_range,
            custom_data=["sex", "age_group", "multiplier"],
        )

        # Layout and annotations
        line_fig.update_layout(
            legend_title_text="Sex",
            xaxis_title="Year",
            template="bengtegard",
            hovermode="x",
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=BG_COLOR,
            font_color=TEXT_COLOR,
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 250, "redraw": False},
                                    "transition": {"duration": 240, "easing": "linear"},
                                },
                            ],
                            "method": "animate",
                            "label": "▶",
                        },
                        {
                            "args": [
                                [None],
                                {
                                    "mode": "immediate",
                                    "frame": {"duration": 0, "redraw": False},
                                    "transition": {"duration": 0},
                                },
                            ],
                            "method": "animate",
                            "label": "❚❚",
                        },
                    ],
                    "direction": "left",
                    "showactive": True,
                    "type": "buttons",
                    "x": 0.1,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top",
                }
            ],
        )

        hover_template = (
            "<b>Sex:</b> %{customdata[0]}<br>"
            "<b>Age group:</b> %{customdata[1]}<br>"
            "<b>Patients per 1,000:</b> %{y:.1f}<br>"
            "<b>Compared to 2006:</b> x%{customdata[2]:.1f} higher"
            "<extra></extra>"
        )

        hover_font_size = 10 if len(selected_ages) > 2 else 12

        # Update initial traces
        for trace in line_fig.data:
            trace.update(
                cliponaxis=False,
                connectgaps=True,
                line_shape="spline",
                line=dict(smoothing=1.3),
                hovertemplate=hover_template,
                hoverlabel=dict(
                    font=dict(
                        size=hover_font_size,
                        color=label_colors.get(trace.name, "white"),
                    ),
                    bgcolor=BG_COLOR,
                    bordercolor=BG_COLOR,  # optional
                ),
            )

        # Update all animation frames
        for frame in line_fig.frames:
            for trace in frame.data:
                trace.update(
                    hovertemplate=hover_template,
                    hoverlabel=dict(
                        font=dict(
                            size=hover_font_size,
                            color=label_colors.get(trace.name, "white"),
                        ),
                        bgcolor=BG_COLOR,
                        bordercolor=BG_COLOR,
                    ),
                )

        # Update axes
        line_fig.update_yaxes(
            # showspikes=True,
            title_text="",
            tick0=0,
            dtick=15,
            range=y_range,
        )
        line_fig.update_xaxes(
            showspikes=True,
            spikecolor="#72B0AB",
            range=[2005.5, 2024.5],  # Add padding before 2006 and after 2024
        )
        # Customize facet titles
        for a in line_fig.layout.annotations:
            if a.text.startswith("age_group="):
                age_group = a.text.split("=")[1]
                a.text = FACET_TITLE_MAP[age_group]
                a.font.color = FACET_COLORS[age_group]

        # Add y-axis label annotation
        line_fig.add_annotation(
            x=-0.08,
            y=0.5,
            text="Patients per 1000 inhabitants",
            showarrow=False,
            textangle=-90,
            xref="paper",
            yref="paper",
            font=dict(size=14, color=TEXT_COLOR),
        )

        line_fig = apply_responsive_layout(
            line_fig,
            bp,
            width,
            height,
            chart_type="line",
        )

        return line_fig

    # ============================================================================
    # 2. STATIC BAR CHART
    # ============================================================================
    @app.callback(
        Output("bar-chart", "figure"),
        [
            Input("show-bar-chart-btn", "n_clicks"),
            Input("breakpoint", "widthBreakpoint"),
        ],
        [
            State("breakpoint", "width"),
            State("breakpoint", "height"),
        ],
    )
    def barplot_20_vs_24(n_clicks, bp, width, height):
        """
        Create a grouped bar plot showing ADHD medication use among 5–24-year-olds
        by sex (Boys/Girls) for years 2020 and 2024.
        """
        if not n_clicks:
            raise dash.exceptions.PreventUpdate

        # Filter dataframe
        df_bar_2024 = df_grouped_national[
            (df_grouped_national["medication_category"] == "All medications")
            & (df_grouped_national["sex"].isin(["Boys", "Girls"]))
            & (df_grouped_national["year"].isin([2020, 2024]))
        ].copy()

        df_bar_2024["year"] = df_bar_2024["year"].astype(str)

        # Create the figure
        bar_plot = px.bar(
            df_bar_2024,
            x="age_group",
            y="patients_per_1000",
            custom_data=["sex", "year"],
            color="year",
            facet_col="sex",
            barmode="group",
            color_discrete_map={"2020": "#E8896B", "2024": "#1B9E77"},
            labels={
                "age_group": "Age Group",
                "patients_per_1000": "Patients per 1000 inhabitants",
                "sex": "Sex",
                "year": "Year",
            },
        )

        hover_template = (
            "<b>Sex:</b> %{customdata[0]}<br>"
            "<b>Year:</b> %{customdata[1]}<br>"
            "<b>Patients per 1,000:</b> %{y:.1f}<br><extra></extra>"
        )

        # Update layout to match Swedish style
        bar_plot.update_layout(
            template=bengtegard_template,
            title=dict(
                text="ADHD Medication Use Among Individuals Aged 5–24, by Sex: 2020 vs 2024",
                x=0.5,
                xanchor="center",
            ),
            yaxis_title="Patients per 1000 inhabitants",
            xaxis_title="Boys/Young men",
            xaxis2_title="Girls/Young women",
            legend=dict(
                title="Year",
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
            ),
            hovermode="x",
            showlegend=True,
            margin=dict(l=60, r=40, t=100, b=60),
        )

        # Remove facet titles (Sex labels)
        bar_plot.for_each_annotation(lambda a: a.update(text=""))

        # Update axes styling
        bar_plot.update_xaxes(
            showgrid=False, zeroline=False, linecolor=TEXT_COLOR, linewidth=1
        )

        bar_plot.update_yaxes(
            range=[0, 105],
            showgrid=True,
            gridwidth=0.5,
            gridcolor="#e6e6e6",
            zeroline=False,
            linecolor=TEXT_COLOR,
            linewidth=1,
        )

        bar_plot.update_traces(width=0.36, hovertemplate=hover_template)

        bar_plot = apply_responsive_layout(
            bar_plot,
            bp,
            width,
            height,
            chart_type="bar",
        )

        return bar_plot

    # Show/hide the chart when button is clicked
    @app.callback(
        Output("bar-chart", "style"),
        Input("show-bar-chart-btn", "n_clicks"),
        State("bar-chart", "style"),
    )
    def toggle_bar_chart(n_clicks, current_style):
        if n_clicks and n_clicks > 0:
            # Toggle display
            if current_style and current_style.get("display") == "block":
                return {"display": "none"}
            else:
                return {"display": "block"}
        return {"display": "none"}

    # ============================================================================
    # 3. COUNTY-LEVEL HEATMAP
    # ============================================================================

    @app.callback(
        [Output("county-heatmap", "figure"), Output("county-heatmap-note", "style")],
        [
            Input("heatmap-medication-dropdown", "value"),
            Input("heatmap-county-dropdown", "value"),
            Input("heatmap-sex-radio", "value"),
            Input("heatmap-age-radio", "value"),
            Input("breakpoint", "widthBreakpoint"),
        ],
        [
            State("breakpoint", "width"),
            State("breakpoint", "height"),
        ],
    )
    def update_heatmap(
        selected_medication,
        selected_county,
        selected_gender,
        selected_age,
        bp,
        width,
        height,
    ):
        """Update county-level heatmap for selected medication, sex, and age."""

        if selected_medication == "separator":
            selected_medication = "All medications"

        df_heat = df_grouped_regional[
            (df_grouped_regional["medication_category"] == selected_medication)
            & (df_grouped_regional["sex"] == selected_gender)
            & (df_grouped_regional["age_group"] == selected_age)
        ].copy()

        df_heat["year"] = df_heat["year"].astype(str)

        # Calculate multiplier from first available year (with data > 0) for each county
        df_heat["multiplier"] = df_heat.groupby("county")[
            "patients_per_1000"
        ].transform(
            lambda x: (x / x[x > 0].iloc[0]).round(2) if len(x[x > 0]) > 0 else 0
        )

        # Heatmap is the default (all counties)
        if selected_county == "All counties":
            heatmap_fig = px.density_heatmap(
                df_heat,
                x="year",
                y="county",
                z="patients_per_1000",
                labels={"patients_per_1000": "Patients per 1,000"},
                nbinsx=len(df_heat["year"].unique()),
                text_auto=False,
                color_continuous_scale="Viridis",
            )

            heatmap_fig.update_layout(
                title={
                    "text": f"ADHD Prescriptions in Sweden by County<br><sup>{selected_medication}, {selected_gender}, Age {selected_age}</sup>",
                    "x": 0.5,
                    "xanchor": "center",
                },
                xaxis_title="Year",
                yaxis_title="County",
                template="bengtegard",
                paper_bgcolor=BG_COLOR,
                plot_bgcolor=BG_COLOR,
                font_color=TEXT_COLOR,
                coloraxis_colorbar=dict(title="Patients per 1000"),
            )
            heatmap_fig.update_coloraxes(
                colorbar_tickfont_size=10,
                colorbar_tickfont_color=TEXT_COLOR,
            )

            # Update axes and add a custom hovertemplate
            heatmap_fig.update_xaxes(
                tickmode="array",
                tickvals=df_heat["year"].unique(),
                ticktext=df_heat["year"].unique(),
            )
            heatmap_fig.update_yaxes(title_standoff=4, automargin=True)
            heatmap_fig.update_traces(
                hovertemplate=(
                    "<b>Year:</b> %{x}<br>"
                    "<b>County:</b> %{y}<br>"
                    "<b>Patients per 1,000:</b> %{z}<extra></extra>"
                ),
                hoverlabel=dict(bgcolor=TEXT_COLOR),
            )

            # Apply breakpoints configuration
            heatmap_fig = apply_responsive_layout(heatmap_fig, bp, width, height)

            note_style = {
                "fontSize": "11px",
                "color": TEXT_COLOR,
                "fontStyle": "italic",
                "marginTop": "10px",
                "marginLeft": "20px",
                "display": "none",
            }

        # Line chart if single county
        else:
            df_single = df_heat[df_heat["county"] == selected_county]
            heatmap_fig = px.line(
                df_single,
                x="year",
                y="patients_per_1000",
                color="age_group",
                markers=True,
                color_discrete_map=FACET_COLORS,
                title=f"ADHD Prescriptions in {selected_county}<br><sub>{selected_medication} | {selected_gender} | Age {selected_age}</sub>",
            )
            heatmap_fig.update_layout(
                hovermode="x",
                xaxis_title="Year",
                yaxis_title="Patients per 1000 inhabitants",
                template="bengtegard",
                paper_bgcolor=BG_COLOR,
                plot_bgcolor=BG_COLOR,
                font_color=TEXT_COLOR,
                legend_title_text="Age Group",
            )
            # Update axes and add a custom hovertemplate
            heatmap_fig.update_xaxes(
                showspikes=True,
                tickmode="array",
                tickvals=df_single["year"].unique(),
                ticktext=df_single["year"].unique(),
            )
            heatmap_fig.update_yaxes(showspikes=True, tick0=0, dtick=10)

            for trace in heatmap_fig.data:
                trace.update(
                    hovertemplate=(
                        "<b>Year:</b> %{x}<br>"
                        "<b>Patients per 1,000:</b> %{y:.1f}<extra></extra>"
                    ),
                    hoverlabel=dict(
                        font=dict(color=FACET_COLORS.get(trace.name, "white")),
                        bgcolor=BG_COLOR,
                        bordercolor=BG_COLOR,
                    ),
                )
            # Add multiplier annotation at the end of the line
            last_point = df_single.iloc[-1]
            heatmap_fig.add_annotation(
                x=last_point["year"],
                y=last_point["patients_per_1000"],
                text=f"x{last_point['multiplier']:.1f}",
                showarrow=False,
                xshift=10,  # Shift text to the right of the point
                font=dict(size=14, color=FACET_COLORS.get(last_point["age_group"])),
                xanchor="left",
            )

            # Apply breakpoints configuration
            heatmap_fig = apply_responsive_layout(heatmap_fig, bp, width, height)

            # Show note only when a specific county is selected
            note_style = {
                "fontSize": "11px",
                "color": TEXT_COLOR,
                "fontStyle": "italic",
                "marginTop": "10px",
                "marginLeft": "20px",
                "display": "block" if selected_county != "All counties" else "none",
            }

        return heatmap_fig, note_style

    # ============================================================================
    # 4. GENDER RATIO PLOT
    # ============================================================================

    @app.callback(
        Output("sex-ratio-plot", "figure"),
        [
            Input("ratio-medication-dropdown", "value"),
            Input("breakpoint", "widthBreakpoint"),
        ],
        [
            State("breakpoint", "width"),
            State("breakpoint", "height"),
        ],
    )
    def update_gender_ratio(selected_medication, bp, width, height):
        """Update the sex ratio chart based on medication selection."""

        if selected_medication == "separator":
            selected_medication = "All medications"

        df_filtered = df_grouped_national[
            df_grouped_national["medication_category"] == selected_medication
        ]
        fig = plot_gender_ratios(df_filtered)

        fig.update_layout(
            title=f"Boys-to-Girls ADHD Prescription Ratio by Age Group - {selected_medication}"
        )
        fig = apply_responsive_layout(
            fig,
            bp,
            width,
            height,
            chart_type="ratio",
        )

        return fig

    # ============================================================================
    # 5. CHOROPLETH MAP
    # ============================================================================

    @app.callback(
        [Output("choropleth-map", "figure"), Output("choropleth-stats", "children")],
        [
            Input("choropleth-year-slider", "value"),
            Input("choropleth-sex-radio", "value"),
            Input("choropleth-age-radio", "value"),
            Input("breakpoint", "widthBreakpoint"),
        ],
        [
            State("breakpoint", "width"),
            State("breakpoint", "height"),
        ],
    )
    def update_choropleth(year, sex, age_group, bp, width, height):
        """Update choropleth map and statistics based on selections."""

        if geojson_counties is None:
            fig = go.Figure()
            fig.add_annotation(
                text="GeoJSON file not found.",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                xanchor="center",
                yanchor="middle",
                showarrow=False,
                font_size=16,
            )
            fig.update_layout(
                template="bengtegard",
                paper_bgcolor=BG_COLOR,
                font_color=TEXT_COLOR,
            )
            stats = html.Div([html.H4("GeoJSON file missing", style={"color": "red"})])
            return fig, stats

        df_map = prepare_choropleth_data(df_grouped_regional, year, age_group, sex)
        if df_map.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for selected parameters",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                xanchor="center",
                yanchor="middle",
                showarrow=False,
                font_size=16,
            )
            fig.update_layout(
                template="bengtegard",
                paper_bgcolor=BG_COLOR,
                font_color=TEXT_COLOR,
            )
            stats = html.Div([html.H4("No data available", style={"color": "red"})])
            return fig, stats

        # Max for color scale
        max_all = df_grouped_regional[
            df_grouped_regional["medication_category"] == "All medications"
        ]["patients_per_1000"].max()
        color_scale_max = max_all * 1.1

        # National trend context
        trend_context = get_national_trend_context(
            df_grouped_national, year, age_group, sex
        )

        # Create choropleth figure
        map_fig = px.choropleth(
            df_map,
            geojson=geojson_counties,
            locations="county_geo",
            featureidkey="properties.name",
            color="patients_per_1000",
            color_continuous_scale="Plasma",
            range_color=[0, color_scale_max],
            labels={"patients_per_1000": "Patients per 1000"},
            hover_name="county",
            hover_data={"county_geo": False, "patients_per_1000": ":.1f"},
        )

        # Layout, annotations, and stats
        map_fig.update_geos(
            fitbounds="locations",
            projection_type="natural earth",
            visible=False,
            bgcolor=BG_COLOR,
        )
        map_fig.update_traces(
            marker_line_width=1,
            marker_line_color="white",
            hovertemplate="<b>%{hovertext}</b>"
            "<br><b>Patients per 1000:</b> %{z:.1f}<extra></extra>",
            hoverlabel=dict(bgcolor=BG_COLOR, font=dict(color=TEXT_COLOR)),
        )
        map_fig.update_layout(
            dragmode=False,
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=BG_COLOR,
            font_color=TEXT_COLOR,
            transition={"duration": 900, "easing": "cubic-in-out"},
            template=bengtegard_template,
            title={
                "text": f"ADHD Prescription Rates by County ({sex}, Age {age_group})<br>{year}",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            coloraxis_colorbar=dict(
                title="Patients per 1000",
                tickfont=dict(size=10, color=TEXT_COLOR),
                thickness=11,
                len=0.7,
                x=0.8,
                tickmode="linear",
                tick0=0,
                dtick=20,
                # tickformat=".1f",
            ),
        )
        map_fig.add_annotation(
            text=trend_context,
            xref="paper",
            yref="paper",
            x=0.04,
            y=0.94,
            showarrow=False,
            font=dict(size=14, color=TEXT_COLOR),
            bgcolor=BG_COLOR,
            bordercolor=BG_COLOR,
        )

        # Statistics summary
        if len(df_map) > 0:
            highest_county = df_map.loc[df_map["patients_per_1000"].idxmax(), "county"]
            highest_rate = df_map["patients_per_1000"].max()
            lowest_county = df_map.loc[df_map["patients_per_1000"].idxmin(), "county"]
            lowest_rate = df_map["patients_per_1000"].min()
            std_rate = df_map["patients_per_1000"].std()

            stats = html.Div(
                [
                    html.H4(
                        f"Statistics for {year}",
                        style={"marginBottom": 15, "color": TEXT_COLOR},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong("Highest Rate: "),
                                    f"{highest_county} ({highest_rate:.1f} per 1000)",
                                ],
                                style={"marginBottom": 5, "color": TEXT_COLOR},
                            ),
                            html.Div(
                                [
                                    html.Strong("Lowest Rate: "),
                                    f"{lowest_county} ({lowest_rate:.1f} per 1000)",
                                ],
                                style={"marginBottom": 5, "color": TEXT_COLOR},
                            ),
                            html.Div(
                                [
                                    html.Strong("Standard Deviation: "),
                                    f"{std_rate:.1f}",
                                ],
                                style={"marginBottom": 5, "color": TEXT_COLOR},
                            ),
                        ]
                    ),
                ]
            )
        else:
            stats = html.Div(
                [html.H4("No data available", style={"color": TEXT_COLOR})]
            )
        map_fig = apply_responsive_layout(map_fig, bp, width, height, chart_type="map")

        return map_fig, stats

    # ============================================================================
    # 6. CHOROPLETH ANIMATION CONTROLS
    # ============================================================================
    @app.callback(
        [
            Output("choropleth-year-slider", "value"),
            Output("choropleth-interval", "disabled"),
            Output("choropleth-animation-state", "data"),
        ],
        [
            Input("choropleth-play-btn", "n_clicks"),
            Input("choropleth-pause-btn", "n_clicks"),
            Input("choropleth-interval", "n_intervals"),
        ],
        [
            State("choropleth-animation-state", "data"),
            State("choropleth-year-slider", "value"),
        ],
    )
    def control_and_animate_choropleth(
        play_clicks, pause_clicks, n_intervals, animation_state, current_year
    ):
        """Combined play/pause controls and animation for choropleth."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return (
                current_year,
                True,
                animation_state or {"playing": False, "current_year": current_year},
            )

        # Find out which button was clicked
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # Handle play button
        if trigger_id == "choropleth-play-btn":
            start_year = 2006 if current_year >= 2024 else current_year
            return start_year, False, {"playing": True, "current_year": start_year}

        # Handle pause button
        elif trigger_id == "choropleth-pause-btn":
            return current_year, True, {"playing": False, "current_year": current_year}

        # Handle animation interval
        elif trigger_id == "choropleth-interval":
            if not animation_state.get("playing", False):
                return current_year, True, animation_state

            next_year = current_year + 1
            if next_year > 2024:
                # Stop animation at 2024
                return 2024, True, {"playing": False, "current_year": 2024}
            return next_year, False, animation_state

        return current_year, True, animation_state
