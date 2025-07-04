import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_processed_data():
    """Load the processed OWID data"""
    print("Loading processed OWID data...")
    df = pd.read_csv('data/processed/cleaned_owid_co2_data.csv')
    return df

def create_global_trends_analysis(df):
    """Analyze global CO2 emission trends"""
    print("Creating global trends analysis...")
    
    # Global trends over time
    global_trends = df.groupby('year').agg({
        'co2': 'sum',
        'coal_co2': 'sum',
        'oil_co2': 'sum',
        'gas_co2': 'sum',
        'cement_co2': 'sum',
        'flaring_co2': 'sum',
        'population': 'sum'
    }).reset_index()
    
    # Calculate per capita emissions globally
    global_trends['co2_per_capita_global'] = global_trends['co2'] / global_trends['population']
    
    return global_trends

def create_country_analysis(df):
    """Analyze country-level emissions"""
    print("Creating country analysis...")
    
    # Get latest year data
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].copy()
    
    # Top 20 emitters
    top_20_emitters = latest_data.nlargest(20, 'co2')
    
    # Top 20 per capita emitters
    top_20_per_capita = latest_data.nlargest(20, 'co2_per_capita')
    
    # Countries with highest growth in emissions (comparing 1990 vs latest)
    if 1990 in df['year'].values:
        data_1990 = df[df['year'] == 1990][['country', 'co2']].rename(columns={'co2': 'co2_1990'})
        growth_data = latest_data[['country', 'co2']].merge(data_1990, on='country', how='inner')
        growth_data['emission_growth'] = ((growth_data['co2'] - growth_data['co2_1990']) / growth_data['co2_1990']) * 100
        top_growth = growth_data.nlargest(20, 'emission_growth')
    else:
        top_growth = None
    
    return {
        'latest_year': latest_year,
        'top_20_emitters': top_20_emitters,
        'top_20_per_capita': top_20_per_capita,
        'top_growth': top_growth
    }

def create_fuel_source_analysis(df):
    """Analyze emissions by fuel source"""
    print("Creating fuel source analysis...")
    
    # Global fuel mix over time
    fuel_trends = df.groupby('year').agg({
        'coal_co2': 'sum',
        'oil_co2': 'sum',
        'gas_co2': 'sum',
        'cement_co2': 'sum',
        'flaring_co2': 'sum'
    }).reset_index()
    
    # Calculate percentages
    total_emissions = fuel_trends[['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']].sum(axis=1)
    for fuel in ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']:
        fuel_trends[f'{fuel}_pct'] = (fuel_trends[fuel] / total_emissions) * 100
    
    return fuel_trends

def create_visualizations(df, global_trends, country_analysis, fuel_trends):
    """Create comprehensive visualizations"""
    print("Creating visualizations...")
    
    # Create plots directory
    os.makedirs('data/processed/plots', exist_ok=True)
    
    # 1. Global CO2 Emissions Over Time
    plt.figure(figsize=(12, 8))
    plt.plot(global_trends['year'], global_trends['co2'], linewidth=3, color='#2E86AB')
    plt.title('Global CO2 Emissions Over Time (1950-2021)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('CO2 Emissions (million tonnes)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/processed/plots/global_co2_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Top 20 Emitters
    plt.figure(figsize=(14, 10))
    top_20 = country_analysis['top_20_emitters']
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_20)))
    bars = plt.barh(range(len(top_20)), top_20['co2'], color=colors)
    plt.yticks(range(len(top_20)), top_20['country'])
    plt.xlabel('CO2 Emissions (million tonnes)', fontsize=12)
    plt.title(f'Top 20 CO2 Emitters ({country_analysis["latest_year"]})', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                f'{width:.0f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('data/processed/plots/top_20_emitters.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Fuel Source Mix Over Time
    plt.figure(figsize=(14, 8))
    fuels = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']
    fuel_names = ['Coal', 'Oil', 'Gas', 'Cement', 'Flaring']
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B4513']
    
    for i, (fuel, name, color) in enumerate(zip(fuels, fuel_names, colors)):
        plt.plot(fuel_trends['year'], fuel_trends[fuel], label=name, linewidth=2, color=color)
    
    plt.title('Global CO2 Emissions by Fuel Source Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('CO2 Emissions (million tonnes)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/processed/plots/fuel_source_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Per Capita Emissions
    plt.figure(figsize=(14, 10))
    top_per_capita = country_analysis['top_20_per_capita']
    colors = plt.cm.plasma(np.linspace(0, 1, len(top_per_capita)))
    bars = plt.barh(range(len(top_per_capita)), top_per_capita['co2_per_capita'], color=colors)
    plt.yticks(range(len(top_per_capita)), top_per_capita['country'])
    plt.xlabel('CO2 Emissions per Capita (tonnes)', fontsize=12)
    plt.title(f'Top 20 CO2 Emitters per Capita ({country_analysis["latest_year"]})', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('data/processed/plots/top_per_capita_emitters.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Global Per Capita Emissions
    plt.figure(figsize=(12, 8))
    plt.plot(global_trends['year'], global_trends['co2_per_capita_global'], 
             linewidth=3, color='#2E86AB')
    plt.title('Global CO2 Emissions per Capita Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('CO2 Emissions per Capita (tonnes)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/processed/plots/global_per_capita_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Fuel Source Percentage Stacked Area Chart
    plt.figure(figsize=(14, 8))
    fuel_pct_cols = [col for col in fuel_trends.columns if col.endswith('_pct')]
    fuel_names = ['Coal', 'Oil', 'Gas', 'Cement', 'Flaring']
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B4513']
    
    plt.stackplot(fuel_trends['year'], 
                  [fuel_trends[col] for col in fuel_pct_cols],
                  labels=fuel_names, colors=colors, alpha=0.8)
    
    plt.title('Global CO2 Emissions by Fuel Source (% Share)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Percentage of Total Emissions (%)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/processed/plots/fuel_source_percentage.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_interactive_plots(df, global_trends, country_analysis, fuel_trends):
    """Create interactive Plotly visualizations"""
    print("Creating interactive plots...")
    
    # 1. Interactive Global Trends
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=global_trends['year'],
        y=global_trends['co2'],
        mode='lines+markers',
        name='Total CO2',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Global CO2 Emissions Over Time (Interactive)',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions (million tonnes)',
        hovermode='x unified',
        template='plotly_white'
    )
    
    fig.write_html('data/processed/plots/interactive_global_trends.html')
    
    # 2. Interactive Top Emitters
    fig = px.bar(
        country_analysis['top_20_emitters'],
        x='co2',
        y='country',
        orientation='h',
        title=f'Top 20 CO2 Emitters ({country_analysis["latest_year"]})',
        color='co2',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        xaxis_title='CO2 Emissions (million tonnes)',
        yaxis_title='Country',
        template='plotly_white'
    )
    
    fig.write_html('data/processed/plots/interactive_top_emitters.html')
    
    # 3. Interactive Fuel Source Trends
    fig = go.Figure()
    
    fuels = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']
    fuel_names = ['Coal', 'Oil', 'Gas', 'Cement', 'Flaring']
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B4513']
    
    for fuel, name, color in zip(fuels, fuel_names, colors):
        fig.add_trace(go.Scatter(
            x=fuel_trends['year'],
            y=fuel_trends[fuel],
            mode='lines',
            name=name,
            line=dict(color=color, width=2)
        ))
    
    fig.update_layout(
        title='Global CO2 Emissions by Fuel Source',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions (million tonnes)',
        hovermode='x unified',
        template='plotly_white'
    )
    
    fig.write_html('data/processed/plots/interactive_fuel_trends.html')

def generate_insights(df, global_trends, country_analysis, fuel_trends):
    """Generate key insights from the data"""
    print("Generating insights...")
    
    latest_year = country_analysis['latest_year']
    
    # Key statistics
    total_emissions_2021 = global_trends[global_trends['year'] == latest_year]['co2'].iloc[0]
    total_emissions_1950 = global_trends[global_trends['year'] == 1950]['co2'].iloc[0]
    growth_factor = total_emissions_2021 / total_emissions_1950
    
    # Top emitters
    top_3_emitters = country_analysis['top_20_emitters'].head(3)
    
    # Fuel mix in latest year
    latest_fuel_data = fuel_trends[fuel_trends['year'] == latest_year]
    
    insights = {
        'total_emissions_2021': total_emissions_2021,
        'growth_since_1950': growth_factor,
        'top_3_emitters': top_3_emitters,
        'latest_fuel_mix': latest_fuel_data,
        'total_countries': df['country'].nunique(),
        'year_range': f"{df['year'].min()} - {df['year'].max()}"
    }
    
    # Save insights
    with open('data/processed/key_insights.txt', 'w') as f:
        f.write("KEY INSIGHTS FROM OWID CO2 DATA ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"1. GLOBAL EMISSIONS:\n")
        f.write(f"   - Total CO2 emissions in {latest_year}: {total_emissions_2021:,.0f} million tonnes\n")
        f.write(f"   - Growth since 1950: {growth_factor:.1f}x increase\n")
        f.write(f"   - Data covers {insights['total_countries']} countries\n\n")
        
        f.write(f"2. TOP EMITTERS ({latest_year}):\n")
        for _, row in top_3_emitters.iterrows():
            f.write(f"   - {row['country']}: {row['co2']:,.0f} million tonnes ({row['share_global_co2']:.1f}% of global)\n")
        f.write("\n")
        
        f.write(f"3. FUEL MIX ({latest_year}):\n")
        for fuel in ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']:
            if fuel in latest_fuel_data.columns:
                value = latest_fuel_data[fuel].iloc[0]
                f.write(f"   - {fuel.replace('_co2', '').title()}: {value:,.0f} million tonnes\n")
    
    return insights

def main():
    """Main analysis function"""
    print("Starting OWID CO2 data analysis...")
    
    # Load data
    df = load_processed_data()
    
    # Perform analyses
    global_trends = create_global_trends_analysis(df)
    country_analysis = create_country_analysis(df)
    fuel_trends = create_fuel_source_analysis(df)
    
    # Create visualizations
    create_visualizations(df, global_trends, country_analysis, fuel_trends)
    create_interactive_plots(df, global_trends, country_analysis, fuel_trends)
    
    # Generate insights
    insights = generate_insights(df, global_trends, country_analysis, fuel_trends)
    
    print("\n=== Analysis Complete ===")
    print(f"Generated {len(os.listdir('data/processed/plots'))} visualization files")
    print(f"Key insights saved to data/processed/key_insights.txt")
    print(f"Interactive plots saved to data/processed/plots/")
    
    return df, global_trends, country_analysis, fuel_trends, insights

if __name__ == "__main__":
    main() 