
from data_processing import load_processed_csv, load_and_process_all_data

# Load CSV
df_raw = load_processed_csv()

# Process all
df_national, df_regional = load_and_process_all_data(df_raw)




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
            return True, current_state, current_year

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'choropleth-play-btn':
            # If we're at the end (2024) or past it, reset to 2006
            start_year = 2006 if current_year >= 2024 else current_year
            return False, {'playing': True, 'current_year': start_year}, start_year
        elif button_id == 'choropleth-pause-btn':
            return True, {'playing': False, 'current_year': current_year}, current_year
        return True, current_state, current_year

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