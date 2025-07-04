#!/usr/bin/env python3
"""
Data Preparation for Carbon Footprint Analysis
This script loads, inspects, and cleans organizational carbon emissions data.
"""

import pandas as pd
import numpy as np
import os

def main():
    print("=== Data Preparation for Carbon Footprint Analysis ===\n")
    
    # Get the project root directory (2 levels up from src/data_prep)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Load the sample data
    print("1. Loading sample data...")
    try:
        data_path = os.path.join(project_root, 'data', 'raw', 'sample_organization_emissions.csv')
        df = pd.read_csv(data_path)
        print(f"   ✓ Loaded {len(df)} records")
        print("\n   First 5 rows:")
        print(df.head())
    except FileNotFoundError:
        print(f"   ✗ Error: Could not find {data_path}")
        return
    
    # Inspect data
    print("\n2. Data inspection...")
    print("\n   Data info:")
    print(df.info())
    
    print("\n   Summary statistics:")
    print(df.describe())
    
    # Data cleaning
    print("\n3. Data cleaning...")
    
    # Drop duplicates
    original_count = len(df)
    df = df.drop_duplicates()
    print(f"   ✓ Removed {original_count - len(df)} duplicate records")
    
    # Fill missing values
    missing_before = df.isnull().sum().sum()
    df = df.fillna({'CO2_Emissions_tonnes': 0, 'Sector': 'Unknown', 'Country': 'Unknown'})
    missing_after = df.isnull().sum().sum()
    print(f"   ✓ Filled {missing_before - missing_after} missing values")
    
    # Ensure correct data types
    df['Year'] = df['Year'].astype(int)
    df['CO2_Emissions_tonnes'] = df['CO2_Emissions_tonnes'].astype(float)
    print("   ✓ Converted data types")
    
    print("\n   Cleaned data preview:")
    print(df.head())
    
    # Save cleaned data
    print("\n4. Saving cleaned data...")
    try:
        # Ensure the processed directory exists
        processed_dir = os.path.join(project_root, 'data', 'processed')
        os.makedirs(processed_dir, exist_ok=True)
        
        output_path = os.path.join(processed_dir, 'cleaned_organization_emissions.csv')
        df.to_csv(output_path, index=False)
        print(f"   ✓ Cleaned data saved to '{output_path}'")
    except Exception as e:
        print(f"   ✗ Error saving data: {e}")
        return
    
    print("\n=== Data preparation completed successfully! ===")
    print(f"   - Original records: {original_count}")
    print(f"   - Cleaned records: {len(df)}")
    print(f"   - Columns: {list(df.columns)}")

if __name__ == "__main__":
    main() 