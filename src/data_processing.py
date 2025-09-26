# src/data_processing.py
"""Data processing functions for ADHD medication dashboard."""

import pandas as pd
import os
import json
from typing import Tuple

from config import (
    MED_NAME_MAP, GENDER_MAP, COUNTY_MAP, FILES_AND_AGES, 
    VALID_AGE_GROUPS, VALID_GENDERS, RAW_DATA_PATH, PROCESSED_CSV
)

def load_processed_csv(path=PROCESSED_CSV) -> pd.DataFrame:
    return pd.read_csv(path)

def load_geojson(file_path='swedish_provinces.geojson'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            geojson_counties = json.load(f)
        return geojson_counties
    except FileNotFoundError:
        print("GeoJSON not found")
        return None

def import_adhd_excel(region_filter="all", data_path=RAW_DATA_PATH):
    """
    Import and combine the ADHD Excel files into a long format DataFrame.
    
    Parameters:
    region_filter: "riket" for national data only, "regional" for counties only, "all" for both.
    data_path: Path to the directory containing Excel files.
    
    Returns:
    pd.DataFrame: Combined data in long format
    """
    all_data = []
    
    for filename, age_group in FILES_AND_AGES.items():
        file_path = os.path.join(data_path, filename)
        try:
            # Header row is second row in the sheet
            df_temp = pd.read_excel(file_path, header=1)
            all_data.append(df_temp)
        except FileNotFoundError:
            print(f"File {filename} does not exist at {file_path}")
    
    if not all_data:
        return None
    
    # Combine all age-group DataFrames
    df_all = pd.concat(all_data, ignore_index=True)
    
    # Apply region filter
    if region_filter == "riket":
        df_all = df_all[df_all["Region"] == "Riket"]
    elif region_filter == "regional":
        df_all = df_all[df_all["Region"] != "Riket"]
    
    # Filter for valid age groups and genders
    df_all = df_all[
        (df_all["Kön"].isin(VALID_GENDERS)) &
        (df_all["Ålder"].isin(VALID_AGE_GROUPS))
    ].copy()
    
    # Identify year columns (all columns that are purely digits)
    year_cols = [c for c in df_all.columns if str(c).isdigit()]
    
    # Melt to long format: one row per year
    df_long = df_all.melt(
        id_vars=["Mått", "Läkemedel", "Region", "Kön", "Ålder"],
        value_vars=year_cols,
        var_name="year",
        value_name="patients_per_1000",
    )
    
    # Clean up and rename columns
    df_long = df_long.rename(columns={
        "Kön": "gender",
        "Ålder": "age_group",
        "Region": "county",
        "Mått": "measure",
        "Läkemedel": "medication"
    })
    
    # Convert year to integer
    df_long["year"] = df_long["year"].astype(int)
    
    return df_long


def process_national_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process national data by filtering, translating, and mapping values.
    
    Parameters:
    df: Raw dataframe from data fetcher
    
    Returns:
    pd.DataFrame: Processed national data
    """
    # Filter for national data
    df_national = df[
        (df['Region'] == 'Riket') &
        (df['Ålder'].isin(VALID_AGE_GROUPS)) &
        (df['Kön'].isin(VALID_GENDERS))
    ].copy()
    
    # Translate column names to English
    df_national = df_national.rename(columns={
        'År': 'year',
        'Kön': 'gender',
        'Region': "county",
        'Ålder': 'age_group',
        'Läkemedel': 'medication',
        'Patienter/1000 invånare': 'patients_per_1000'
    })
    
    # Map medications to individual names
    df_national["medication_name"] = df_national["medication"].map(MED_NAME_MAP)
    
    # Map gender values to English
    df_national['gender'] = df_national['gender'].map(GENDER_MAP)
    
    return df_national


def process_regional_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process regional data by filtering, translating, and mapping values.
    
    Parameters:
    df: Raw dataframe from data fetcher
    
    Returns:
    pd.DataFrame: Processed regional data
    """
    # Filter to include all counties (exclude national)
    df_regional = df[
        (df['Region'] != 'Riket') &
        (df['Ålder'].isin(VALID_AGE_GROUPS)) &
        (df['Kön'].isin(VALID_GENDERS))
    ].copy()
    
    # Translate column names to English
    df_regional = df_regional.rename(columns={
        'År': 'year',
        'Kön': 'gender',
        'Ålder': 'age_group',
        'Läkemedel': 'medication',
        'Patienter/1000 invånare': 'patients_per_1000',
        'Region': 'county'
    })
    
    # Map ATC codes to individual ADHD medication names
    df_regional["medication_name"] = df_regional["medication"].map(MED_NAME_MAP)
    
    # Map gender values to English
    df_regional['gender'] = df_regional['gender'].map(GENDER_MAP)
    
    return df_regional


def create_grouped_national_data(df_national: pd.DataFrame, data_path=RAW_DATA_PATH) -> pd.DataFrame:
    """
    Create grouped national dataset combining individual medications and all medications.
    
    Parameters:
    df_national: Processed national dataframe
    data_path: Path to raw data files
    
    Returns:
    pd.DataFrame: Grouped national data
    """
    # Individual medications for national data
    df_individual_nat = (
        df_national
        .dropna(subset=["medication_name"])
        .copy()
    )
    df_individual_nat["medication_category"] = df_individual_nat["medication_name"]
    
    # Import "All ADHD medications" data
    df_all_adhd_national = import_adhd_excel(region_filter="riket", data_path=data_path)
    
    if df_all_adhd_national is not None:
        # Map gender
        df_all_adhd_national["gender"] = df_all_adhd_national["gender"].map(GENDER_MAP)
        # Add medication category
        df_all_adhd_national["medication_category"] = "All medications"
    else:
        df_all_adhd_national = pd.DataFrame()
    
    # Combine dataframes
    columns_keep = ["year", "county", "gender", "age_group", "medication_category", "patients_per_1000"]
    
    df_grouped = pd.concat([
        df_individual_nat[columns_keep],
        df_all_adhd_national[columns_keep] if not df_all_adhd_national.empty else pd.DataFrame(columns=columns_keep)
    ], ignore_index=True)
    
    return df_grouped


def create_grouped_regional_data(df_regional: pd.DataFrame, data_path=RAW_DATA_PATH) -> pd.DataFrame:
    """
    Create grouped regional dataset combining individual medications and all medications.
    
    Parameters:
    df_regional: Processed regional dataframe
    data_path: Path to raw data files
    
    Returns:
    pd.DataFrame: Grouped regional data
    """
    # Individual medications for regional data
    df_individual_reg = (
        df_regional
        .dropna(subset=["medication_name"])  # keep only the 5 ADHD meds
        .copy()
    )
    df_individual_reg["medication_category"] = df_individual_reg["medication_name"]
    
    # Import the "All ADHD medications" regional data
    df_all_adhd_regional = import_adhd_excel(region_filter="regional", data_path=data_path)
    
    if df_all_adhd_regional is not None:
        df_all_adhd_regional["gender"] = df_all_adhd_regional["gender"].map(GENDER_MAP)
        df_all_adhd_regional["medication_category"] = "All medications"
        
        # Fix county names
        df_all_adhd_regional['county'] = df_all_adhd_regional['county'].map(COUNTY_MAP).fillna(df_all_adhd_regional['county'])
    else:
        df_all_adhd_regional = pd.DataFrame()
    
    # Columns to keep
    columns_keep = ['year', 'county', 'gender', 'age_group', 'medication_category', 'patients_per_1000']
    
    # Combine the DataFrames
    df_grouped_regional = pd.concat([
        df_individual_reg[columns_keep],
        df_all_adhd_regional[columns_keep] if not df_all_adhd_regional.empty else pd.DataFrame(columns=columns_keep)
    ], ignore_index=True)
    
    return df_grouped_regional


def create_cumulative_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create cumulative data frames for animation.
    
    Parameters:
    df: Input dataframe
    
    Returns:
    pd.DataFrame: Cumulative data for animation
    """
    cumulative_frames = []
    years = sorted(df['year'].unique())
    
    for year in years:
        frame_data = df[df['year'] <= year].copy()
        frame_data['Year'] = year  # this is the animation frame
        cumulative_frames.append(frame_data)
    
    return pd.concat(cumulative_frames, ignore_index=True)


def make_label(row: pd.Series) -> str:
    """
    Combine gender + age group into readable labels.
    
    Parameters:
    row: DataFrame row
    
    Returns:
    str: Formatted label
    """
    g = row["gender"]
    a = row["age_group"]
    
    if a == "20-24":
        if g == "Boys":
            return "Young men 20-24"
        elif g == "Girls":
            return "Young women 20-24"
        elif g == "Both genders":
            return "Both genders 20-24"
    
    return f"{g} {a}"


def load_and_process_all_data(raw_df: pd.DataFrame, data_path=RAW_DATA_PATH) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main function to load and process all data for the dashboard.
    
    Parameters:
    raw_df: Raw dataframe from adhd_data_fetcher
    data_path: Path to raw data files
    
    Returns:
    Tuple[pd.DataFrame, pd.DataFrame]: (df_grouped_national, df_grouped_regional)
    """
    print("Processing national data...")
    df_national = process_national_data(raw_df)
    df_grouped_national = create_grouped_national_data(df_national, data_path)
    
    print("Processing regional data...")
    df_regional = process_regional_data(raw_df)
    df_grouped_regional = create_grouped_regional_data(df_regional, data_path)
    
    print("Data processing completed!")
    print(f"National data shape: {df_grouped_national.shape}")
    print(f"Regional data shape: {df_grouped_regional.shape}")
    
    return df_grouped_national, df_grouped_regional