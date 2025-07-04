import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_owid_data():
    """Load the OWID CO2 dataset"""
    print("Loading OWID CO2 dataset...")
    df = pd.read_csv('data/raw/owid-co2-data.csv')
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    return df

def clean_owid_data(df):
    """Clean and prepare the OWID dataset"""
    print("Cleaning OWID dataset...")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Filter for recent years (1950 onwards) to focus on modern data
    df_clean = df_clean[df_clean['year'] >= 1950].copy()
    
    # Select key columns for analysis
    key_columns = [
        'country', 'year', 'iso_code', 'population', 'gdp',
        'co2', 'co2_per_capita', 'co2_per_gdp',
        'coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2',
        'consumption_co2', 'trade_co2',
        'cumulative_co2', 'share_global_co2',
        'energy_per_capita', 'energy_per_gdp',
        'methane', 'nitrous_oxide', 'total_ghg'
    ]
    
    # Keep only columns that exist in the dataset
    available_columns = [col for col in key_columns if col in df_clean.columns]
    df_clean = df_clean[available_columns]
    
    # Handle missing values
    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
    df_clean[numeric_columns] = df_clean[numeric_columns].fillna(0)
    
    # Remove rows where country is missing
    df_clean = df_clean.dropna(subset=['country'])
    
    # Add derived columns
    df_clean['total_fossil_co2'] = (
        df_clean['coal_co2'].fillna(0) + 
        df_clean['oil_co2'].fillna(0) + 
        df_clean['gas_co2'].fillna(0)
    )
    
    # Calculate percentage contributions
    df_clean['coal_share'] = np.where(
        df_clean['total_fossil_co2'] > 0,
        (df_clean['coal_co2'].fillna(0) / df_clean['total_fossil_co2']) * 100,
        0
    )
    df_clean['oil_share'] = np.where(
        df_clean['total_fossil_co2'] > 0,
        (df_clean['oil_co2'].fillna(0) / df_clean['total_fossil_co2']) * 100,
        0
    )
    df_clean['gas_share'] = np.where(
        df_clean['total_fossil_co2'] > 0,
        (df_clean['gas_co2'].fillna(0) / df_clean['total_fossil_co2']) * 100,
        0
    )
    
    print(f"Cleaned dataset has {len(df_clean)} rows and {len(df_clean.columns)} columns")
    return df_clean

def create_summary_statistics(df):
    """Create summary statistics for the cleaned dataset"""
    print("Creating summary statistics...")
    
    # Latest year data
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].copy()
    
    # Top emitters by total CO2
    top_emitters = latest_data.nlargest(10, 'co2')[['country', 'co2', 'co2_per_capita', 'share_global_co2']]
    
    # Top emitters per capita
    top_per_capita = latest_data.nlargest(10, 'co2_per_capita')[['country', 'co2_per_capita', 'co2', 'population']]
    
    # Global trends
    global_trends = df.groupby('year').agg({
        'co2': 'sum',
        'population': 'sum',
        'coal_co2': 'sum',
        'oil_co2': 'sum',
        'gas_co2': 'sum'
    }).reset_index()
    
    return {
        'latest_year': latest_year,
        'top_emitters': top_emitters,
        'top_per_capita': top_per_capita,
        'global_trends': global_trends,
        'total_countries': df['country'].nunique(),
        'year_range': f"{df['year'].min()} - {df['year'].max()}"
    }

def save_processed_data(df, summary_stats):
    """Save the processed data and summary statistics"""
    print("Saving processed data...")
    
    # Create processed directory if it doesn't exist
    os.makedirs('data/processed', exist_ok=True)
    
    # Save cleaned dataset
    df.to_csv('data/processed/cleaned_owid_co2_data.csv', index=False)
    
    # Save summary statistics
    summary_stats['top_emitters'].to_csv('data/processed/top_emitters.csv', index=False)
    summary_stats['top_per_capita'].to_csv('data/processed/top_per_capita.csv', index=False)
    summary_stats['global_trends'].to_csv('data/processed/global_trends.csv', index=False)
    
    # Save metadata
    metadata = {
        'processing_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_dataset': 'OWID CO2 Data',
        'total_countries': summary_stats['total_countries'],
        'year_range': summary_stats['year_range'],
        'latest_year': summary_stats['latest_year'],
        'columns': list(df.columns)
    }
    
    with open('data/processed/metadata.txt', 'w') as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")
    
    print("Data saved successfully!")
    return metadata

def main():
    """Main function to process OWID data"""
    print("Starting OWID CO2 data processing...")
    
    # Load data
    df = load_owid_data()
    
    # Clean data
    df_clean = clean_owid_data(df)
    
    # Create summary statistics
    summary_stats = create_summary_statistics(df_clean)
    
    # Save processed data
    metadata = save_processed_data(df_clean, summary_stats)
    
    print("\n=== Processing Complete ===")
    print(f"Processed {len(df_clean)} records from {summary_stats['total_countries']} countries")
    print(f"Year range: {summary_stats['year_range']}")
    print(f"Latest year: {summary_stats['latest_year']}")
    print(f"Output files saved in data/processed/")
    
    return df_clean, summary_stats

if __name__ == "__main__":
    main() 