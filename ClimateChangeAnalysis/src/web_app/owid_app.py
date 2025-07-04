import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import ClimateAIAgent

# Page configuration
st.set_page_config(
    page_title="OWID Climate Change Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3498db;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .ai-chat {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .ai-response {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #fff;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_owid_data():
    """Load the processed OWID data"""
    try:
        df = pd.read_csv('data/processed/cleaned_owid_co2_data.csv')
        return df
    except FileNotFoundError:
        st.error("Processed OWID data not found. Please run the data preparation script first.")
        return None

@st.cache_data
def load_summary_data():
    """Load summary statistics"""
    try:
        top_emitters = pd.read_csv('data/processed/top_emitters.csv')
        top_per_capita = pd.read_csv('data/processed/top_per_capita.csv')
        global_trends = pd.read_csv('data/processed/global_trends.csv')
        return top_emitters, top_per_capita, global_trends
    except FileNotFoundError:
        return None, None, None

def create_global_overview(df):
    """Create global overview metrics"""
    if df is None:
        return
    
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    
    # Global metrics
    total_emissions = latest_data['co2'].sum()
    total_population = latest_data['population'].sum()
    avg_per_capita = total_emissions / total_population
    total_countries = df['country'].nunique()
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_emissions:,.0f}</div>
            <div class="metric-label">Total CO2 Emissions (Mt)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_per_capita:.1f}</div>
            <div class="metric-label">Global Avg per Capita (t)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_countries}</div>
            <div class="metric-label">Countries Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{latest_year}</div>
            <div class="metric-label">Latest Data Year</div>
        </div>
        """, unsafe_allow_html=True)

def create_global_trends_chart(df):
    """Create global CO2 trends chart"""
    if df is None:
        return
    
    st.markdown('<h2 class="section-header">Global CO2 Emissions Trends</h2>', unsafe_allow_html=True)
    
    # Aggregate global data
    global_trends = df.groupby('year').agg({
        'co2': 'sum',
        'coal_co2': 'sum',
        'oil_co2': 'sum',
        'gas_co2': 'sum',
        'cement_co2': 'sum',
        'flaring_co2': 'sum',
        'population': 'sum'
    }).reset_index()
    
    global_trends['co2_per_capita'] = global_trends['co2'] / global_trends['population']
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Total CO2 Emissions', 'CO2 per Capita', 'Emissions by Fuel Source', 'Fuel Source Share'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Total emissions
    fig.add_trace(
        go.Scatter(x=global_trends['year'], y=global_trends['co2'], 
                  mode='lines+markers', name='Total CO2', line=dict(color='#2E86AB', width=3)),
        row=1, col=1
    )
    
    # Per capita emissions
    fig.add_trace(
        go.Scatter(x=global_trends['year'], y=global_trends['co2_per_capita'], 
                  mode='lines+markers', name='CO2 per Capita', line=dict(color='#A23B72', width=3)),
        row=1, col=2
    )
    
    # Fuel sources
    fuels = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']
    fuel_names = ['Coal', 'Oil', 'Gas', 'Cement', 'Flaring']
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B4513']
    
    for fuel, name, color in zip(fuels, fuel_names, colors):
        fig.add_trace(
            go.Scatter(x=global_trends['year'], y=global_trends[fuel], 
                      mode='lines', name=name, line=dict(color=color, width=2)),
            row=2, col=1
        )
    
    # Fuel source percentages
    total_emissions = global_trends[fuels].sum(axis=1)
    for fuel, name, color in zip(fuels, fuel_names, colors):
        percentage = (global_trends[fuel] / total_emissions) * 100
        fig.add_trace(
            go.Scatter(x=global_trends['year'], y=percentage, 
                      mode='lines', name=f'{name} %', line=dict(color=color, width=2)),
            row=2, col=2
        )
    
    fig.update_layout(height=800, showlegend=True, title_text="Global CO2 Emissions Analysis")
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="CO2 Emissions (Mt)", row=1, col=1)
    fig.update_yaxes(title_text="CO2 per Capita (t)", row=1, col=2)
    fig.update_yaxes(title_text="CO2 Emissions (Mt)", row=2, col=1)
    fig.update_yaxes(title_text="Percentage (%)", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)

def create_country_analysis(df):
    """Create country-level analysis"""
    if df is None:
        return
    
    st.markdown('<h2 class="section-header">Country-Level Analysis</h2>', unsafe_allow_html=True)
    
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].copy()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric = st.selectbox(
            "Select Metric",
            ["Total CO2", "CO2 per Capita", "Share of Global Emissions"],
            key="country_metric"
        )
    
    with col2:
        top_n = st.slider("Number of Countries", 5, 30, 15, key="top_n_countries")
    
    with col3:
        year_filter = st.selectbox(
            "Select Year",
            sorted(df['year'].unique(), reverse=True),
            key="country_year"
        )
    
    # Filter data based on selected year
    year_data = df[df['year'] == year_filter].copy()
    
    # Map metric to column
    metric_map = {
        "Total CO2": "co2",
        "CO2 per Capita": "co2_per_capita",
        "Share of Global Emissions": "share_global_co2"
    }
    
    selected_metric = metric_map[metric]
    top_countries = year_data.nlargest(top_n, selected_metric)
    
    # Create chart
    fig = px.bar(
        top_countries,
        x=selected_metric,
        y='country',
        orientation='h',
        title=f'Top {top_n} Countries by {metric} ({year_filter})',
        color=selected_metric,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        xaxis_title=metric,
        yaxis_title='Country',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data table
    st.subheader("Detailed Data")
    display_columns = ['country', 'co2', 'co2_per_capita', 'share_global_co2', 'population']
    available_columns = [col for col in display_columns if col in top_countries.columns]
    
    st.dataframe(
        top_countries[available_columns].round(2),
        use_container_width=True
    )

def create_fuel_source_analysis(df):
    """Create fuel source analysis"""
    if df is None:
        return
    
    st.markdown('<h2 class="section-header">Fuel Source Analysis</h2>', unsafe_allow_html=True)
    
    # Year selector
    selected_year = st.selectbox(
        "Select Year for Fuel Analysis",
        sorted(df['year'].unique(), reverse=True),
        key="fuel_year"
    )
    
    year_data = df[df['year'] == selected_year].copy()
    
    # Global fuel mix for selected year
    global_fuel_mix = year_data[['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']].sum()
    
    # Create pie chart
    fig = px.pie(
        values=global_fuel_mix.values,
        names=['Coal', 'Oil', 'Gas', 'Cement', 'Flaring'],
        title=f'Global CO2 Emissions by Fuel Source ({selected_year})',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Fuel trends over time
    st.subheader("Fuel Source Trends Over Time")
    
    global_trends = df.groupby('year')[['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']].sum().reset_index()
    
    fig = go.Figure()
    
    fuels = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']
    fuel_names = ['Coal', 'Oil', 'Gas', 'Cement', 'Flaring']
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B4513']
    
    for fuel, name, color in zip(fuels, fuel_names, colors):
        fig.add_trace(go.Scatter(
            x=global_trends['year'],
            y=global_trends[fuel],
            mode='lines',
            name=name,
            line=dict(color=color, width=3)
        ))
    
    fig.update_layout(
        title='Global CO2 Emissions by Fuel Source Over Time',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions (million tonnes)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_ai_insights_section():
    """Create AI-powered insights section"""
    st.markdown('<h2 class="section-header">AI-Powered Climate Insights</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="ai-chat">
        <h3>🤖 Climate AI Assistant</h3>
        <p>Ask questions about climate change data, trends, and policy recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize AI agent
    ai_agent = ClimateAIAgent()
    
    # Chat interface
    user_query = st.text_area(
        "Ask a question about climate change data:",
        placeholder="e.g., What are the main drivers of CO2 emissions? Which countries have made the most progress in reducing emissions?",
        height=100
    )
    
    if st.button("Get AI Insights", type="primary"):
        if user_query:
            with st.spinner("AI is analyzing the data..."):
                try:
                    response = ai_agent.get_recommendations(user_query)
                    ai_answer = response.get('ai_answer', 'No response generated.')
                    
                    st.markdown(f"""
                    <div class="ai-response">
                        <strong>AI Analysis:</strong><br>
                        {ai_answer}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error getting AI insights: {str(e)}")
        else:
            st.warning("Please enter a question to get AI insights.")

def main():
    """Main application function"""
    # Header
    st.markdown('<h1 class="main-header">🌍 OWID Climate Change Analysis</h1>', unsafe_allow_html=True)
    st.markdown("### Comprehensive analysis of global CO2 emissions using Our World in Data dataset")
    
    # Load data
    df = load_owid_data()
    
    if df is None:
        st.error("""
        **Data not found!** Please run the data preparation script first:
        
        ```bash
        python src/data_prep/owid_data_prep.py
        ```
        """)
        return
    
    # Sidebar
    st.sidebar.title("📊 Analysis Options")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose Analysis Section",
        ["Global Overview", "Country Analysis", "Fuel Sources", "AI Insights", "Data Explorer"]
    )
    
    # Main content based on selection
    if page == "Global Overview":
        create_global_overview(df)
        create_global_trends_chart(df)
        
    elif page == "Country Analysis":
        create_country_analysis(df)
        
    elif page == "Fuel Sources":
        create_fuel_source_analysis(df)
        
    elif page == "AI Insights":
        create_ai_insights_section()
        
    elif page == "Data Explorer":
        st.markdown('<h2 class="section-header">Data Explorer</h2>', unsafe_allow_html=True)
        
        # Data filters
        col1, col2 = st.columns(2)
        
        with col1:
            selected_countries = st.multiselect(
                "Select Countries",
                options=sorted(df['country'].unique()),
                default=sorted(df['country'].unique())[:5]
            )
        
        with col2:
            year_range = st.slider(
                "Year Range",
                min_value=int(df['year'].min()),
                max_value=int(df['year'].max()),
                value=(int(df['year'].min()), int(df['year'].max()))
            )
        
        # Filter data
        filtered_df = df[
            (df['country'].isin(selected_countries)) &
            (df['year'] >= year_range[0]) &
            (df['year'] <= year_range[1])
        ]
        
        # Show filtered data
        st.subheader("Filtered Data")
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download option
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name=f'climate_data_{year_range[0]}_{year_range[1]}.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    main() 