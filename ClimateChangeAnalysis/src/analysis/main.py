#!/usr/bin/env python3
"""
Data Analysis for Carbon Footprint Analysis
This script performs comprehensive analysis and visualization of organizational carbon emissions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Load the cleaned data"""
    project_root = Path(__file__).parent.parent.parent
    data_path = project_root / 'data' / 'processed' / 'cleaned_organization_emissions.csv'
    
    if not data_path.exists():
        print(f"Error: Could not find {data_path}")
        return None
    
    df = pd.read_csv(data_path)
    print(f"✓ Loaded {len(df)} records from {data_path}")
    return df

def basic_statistics(df):
    """Generate basic statistical analysis"""
    print("\n=== BASIC STATISTICAL ANALYSIS ===")
    
    print(f"\n1. Dataset Overview:")
    print(f"   - Total organizations: {len(df)}")
    print(f"   - Total CO2 emissions: {df['CO2_Emissions_tonnes'].sum():,.0f} tonnes")
    print(f"   - Average emissions per organization: {df['CO2_Emissions_tonnes'].mean():,.0f} tonnes")
    print(f"   - Median emissions: {df['CO2_Emissions_tonnes'].median():,.0f} tonnes")
    
    print(f"\n2. Emissions Range:")
    print(f"   - Minimum: {df['CO2_Emissions_tonnes'].min():,.0f} tonnes")
    print(f"   - Maximum: {df['CO2_Emissions_tonnes'].max():,.0f} tonnes")
    print(f"   - Standard deviation: {df['CO2_Emissions_tonnes'].std():,.0f} tonnes")
    
    print(f"\n3. Sector Analysis:")
    sector_stats = df.groupby('Sector').agg({
        'CO2_Emissions_tonnes': ['count', 'sum', 'mean', 'std']
    }).round(0)
    sector_stats.columns = ['Count', 'Total_Emissions', 'Mean_Emissions', 'Std_Emissions']
    print(sector_stats)
    
    print(f"\n4. Country Analysis:")
    country_stats = df.groupby('Country').agg({
        'CO2_Emissions_tonnes': ['count', 'sum', 'mean']
    }).round(0)
    country_stats.columns = ['Count', 'Total_Emissions', 'Mean_Emissions']
    print(country_stats)

def create_visualizations(df):
    """Create comprehensive visualizations"""
    print("\n=== CREATING VISUALIZATIONS ===")
    
    # Create output directory for plots
    project_root = Path(__file__).parent.parent.parent
    plots_dir = project_root / 'data' / 'processed' / 'plots'
    plots_dir.mkdir(exist_ok=True)
    
    # Set up the plotting style
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    
    # 1. Emissions by Sector (Bar Chart)
    plt.figure(figsize=(10, 6))
    sector_emissions = df.groupby('Sector')['CO2_Emissions_tonnes'].sum().sort_values(ascending=False)
    colors = plt.cm.Set3(np.linspace(0, 1, len(sector_emissions)))
    
    bars = plt.bar(sector_emissions.index, sector_emissions.values, color=colors)
    plt.title('Total CO2 Emissions by Sector', fontsize=16, fontweight='bold')
    plt.ylabel('CO2 Emissions (tonnes)', fontsize=12)
    plt.xlabel('Sector', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, sector_emissions.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000, 
                f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(plots_dir / 'emissions_by_sector.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Emissions by Country (Bar Chart)
    plt.figure(figsize=(10, 6))
    country_emissions = df.groupby('Country')['CO2_Emissions_tonnes'].sum().sort_values(ascending=False)
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(country_emissions)))
    
    bars = plt.bar(country_emissions.index, country_emissions.values, color=colors)
    plt.title('Total CO2 Emissions by Country', fontsize=16, fontweight='bold')
    plt.ylabel('CO2 Emissions (tonnes)', fontsize=12)
    plt.xlabel('Country', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, country_emissions.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000, 
                f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(plots_dir / 'emissions_by_country.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Distribution of Emissions (Histogram)
    plt.figure(figsize=(10, 6))
    plt.hist(df['CO2_Emissions_tonnes'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Distribution of CO2 Emissions Across Organizations', fontsize=16, fontweight='bold')
    plt.xlabel('CO2 Emissions (tonnes)', fontsize=12)
    plt.ylabel('Number of Organizations', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.axvline(df['CO2_Emissions_tonnes'].mean(), color='red', linestyle='--', 
                label=f'Mean: {df["CO2_Emissions_tonnes"].mean():,.0f}')
    plt.axvline(df['CO2_Emissions_tonnes'].median(), color='green', linestyle='--', 
                label=f'Median: {df["CO2_Emissions_tonnes"].median():,.0f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig(plots_dir / 'emissions_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 4. Sector vs Country Heatmap
    plt.figure(figsize=(12, 8))
    pivot_table = df.pivot_table(values='CO2_Emissions_tonnes', 
                                index='Sector', columns='Country', 
                                aggfunc='sum', fill_value=0)
    
    sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', 
                cbar_kws={'label': 'CO2 Emissions (tonnes)'})
    plt.title('CO2 Emissions: Sector vs Country Heatmap', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(plots_dir / 'sector_country_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 5. Top Organizations by Emissions
    plt.figure(figsize=(12, 6))
    top_orgs = df.nlargest(5, 'CO2_Emissions_tonnes')
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_orgs)))
    
    bars = plt.barh(top_orgs['Organization'], top_orgs['CO2_Emissions_tonnes'], color=colors)
    plt.title('Top 5 Organizations by CO2 Emissions', fontsize=16, fontweight='bold')
    plt.xlabel('CO2 Emissions (tonnes)', fontsize=12)
    plt.ylabel('Organization', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for bar, value in zip(bars, top_orgs['CO2_Emissions_tonnes']):
        plt.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2, 
                f'{value:,.0f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(plots_dir / 'top_organizations.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"✓ All plots saved to {plots_dir}")

def generate_insights(df):
    """Generate actionable insights from the data"""
    print("\n=== KEY INSIGHTS & RECOMMENDATIONS ===")
    
    # Calculate key metrics
    total_emissions = df['CO2_Emissions_tonnes'].sum()
    avg_emissions = df['CO2_Emissions_tonnes'].mean()
    highest_emitter = df.loc[df['CO2_Emissions_tonnes'].idxmax()]
    lowest_emitter = df.loc[df['CO2_Emissions_tonnes'].idxmin()]
    
    # Sector analysis
    sector_emissions = df.groupby('Sector')['CO2_Emissions_tonnes'].sum()
    highest_sector = sector_emissions.idxmax()
    lowest_sector = sector_emissions.idxmin()
    
    print(f"\n1. Overall Impact:")
    print(f"   • Total carbon footprint: {total_emissions:,.0f} tonnes CO2")
    print(f"   • Average per organization: {avg_emissions:,.0f} tonnes CO2")
    
    print(f"\n2. Sector Analysis:")
    print(f"   • Highest emitting sector: {highest_sector} ({sector_emissions[highest_sector]:,.0f} tonnes)")
    print(f"   • Lowest emitting sector: {lowest_sector} ({sector_emissions[lowest_sector]:,.0f} tonnes)")
    print(f"   • Sector with most organizations: {df['Sector'].value_counts().index[0]}")
    
    print(f"\n3. Organizational Leaders:")
    print(f"   • Highest emitter: {highest_emitter['Organization']} ({highest_emitter['Sector']}, {highest_emitter['Country']})")
    print(f"   • Lowest emitter: {lowest_emitter['Organization']} ({lowest_emitter['Sector']}, {lowest_emitter['Country']})")
    
    print(f"\n4. Recommendations:")
    print(f"   • Focus reduction efforts on {highest_sector} sector")
    print(f"   • Study best practices from {lowest_emitter['Organization']} in {lowest_emitter['Sector']}")
    print(f"   • Implement sector-specific emission reduction targets")
    print(f"   • Consider carbon pricing or cap-and-trade systems")

def main():
    """Main analysis function"""
    print("=== CARBON FOOTPRINT ANALYSIS ===")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Perform analysis
    basic_statistics(df)
    create_visualizations(df)
    generate_insights(df)
    
    print("\n=== ANALYSIS COMPLETED ===")
    print("Next steps:")
    print("1. Review the generated plots in data/processed/plots/")
    print("2. Use insights for policy recommendations")
    print("3. Integrate with AI agent for regulatory scanning")

if __name__ == "__main__":
    main() 