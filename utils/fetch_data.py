# utils/fetch_data.py

from .adhd_data_fetcher import fetch_adhd_medication_data, save_to_json, convert_json_to_csv

# Fetch data for age groups between 5-24
data = fetch_adhd_medication_data(age_groups=[2,3,4,5])

save_to_json(data, "adhd_medication_2006-2024.json")

convert_json_to_csv(
    input_json="adhd_medication_2006-2024.json",
    output_csv="adhd_medication_2006-2024.csv")



