# ============================================================================
# MAIN APPLICATION FILE
# ============================================================================
# Entry point for the ADHD medication dashboard Dash application.
# Initializes the app, loads data, registers callbacks, and starts the server.
# ============================================================================

import sys
import os
import dash

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.layouts import create_layout
from src.callbacks import register_callbacks
from src.data_processing import (
    load_processed_csv,
    load_and_process_all_data,
    load_geojson,
)

# Initialize app
app = dash.Dash(__name__)

# Load data
df_raw = load_processed_csv()
df_grouped, df_grouped_regional = load_and_process_all_data(df_raw)
geojson_counties = load_geojson()

# Assign layout
app.layout = create_layout()

# Expose Flash server for gunicorn
server = app.server

# Register callbacks
register_callbacks(app, df_grouped, df_grouped_regional, geojson_counties)

if __name__ == "__main__":
    app.run(threaded=True)
