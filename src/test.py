
from data_processing import load_processed_csv, load_and_process_all_data

# Load CSV
df_raw = load_processed_csv()

# Process all
df_national, df_regional = load_and_process_all_data(df_raw)
