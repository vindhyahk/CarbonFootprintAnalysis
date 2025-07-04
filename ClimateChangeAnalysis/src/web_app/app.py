#!/usr/bin/env python3
"""
Climate Change Analysis Web Application
A modern, interactive web app for carbon footprint analysis and policy recommendations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import os
import json
from datetime import datetime
import sys
import time

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent.agent import create_ai_agent

# Page configuration
st.set_page_config(
    page_title="Climate Change Analysis Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Climate Hero Gamification System
class ClimateHeroSystem:
    def __init__(self):
        self.achievements = {
            'data_explorer': {
                'name': 'Data Explorer',
                'description': 'Explored climate data for the first time',
                'icon': '📊',
                'points': 10,
                'unlocked': False
            },
            'chart_master': {
                'name': 'Chart Master',
                'description': 'Viewed 5 different charts',
                'icon': '📈',
                'points': 25,
                'unlocked': False
            },
            'ai_consultant': {
                'name': 'AI Consultant',
                'description': 'Asked 3 questions to the AI agent',
                'icon': '🤖',
                'points': 50,
                'unlocked': False
            },
            'policy_expert': {
                'name': 'Policy Expert',
                'description': 'Explored policy recommendations',
                'icon': '📋',
                'points': 75,
                'unlocked': False
            },
            'climate_hero': {
                'name': 'Climate Hero',
                'description': 'Earned 100+ points',
                'icon': '🏆',
                'points': 100,
                'unlocked': False
            },
            'data_analyst': {
                'name': 'Data Analyst',
                'description': 'Exported data 3 times',
                'icon': '💾',
                'points': 30,
                'unlocked': False
            },
            'trend_watcher': {
                'name': 'Trend Watcher',
                'description': 'Analyzed trends over 10 years',
                'icon': '📉',
                'points': 40,
                'unlocked': False
            },
            'global_citizen': {
                'name': 'Global Citizen',
                'description': 'Explored data from 5+ countries',
                'icon': '🌐',
                'points': 60,
                'unlocked': False
            }
        }
    
    def initialize_user_session(self):
        """Initialize user session with gamification data"""
        if 'climate_hero_points' not in st.session_state:
            st.session_state.climate_hero_points = 0
        if 'climate_hero_level' not in st.session_state:
            st.session_state.climate_hero_level = 1
        if 'unlocked_achievements' not in st.session_state:
            st.session_state.unlocked_achievements = []
        if 'user_actions' not in st.session_state:
            st.session_state.user_actions = {
                'charts_viewed': 0,
                'ai_questions': 0,
                'data_exports': 0,
                'countries_explored': set(),
                'years_analyzed': set()
            }
    
    def award_points(self, action_type, points):
        """Award points for user actions"""
        st.session_state.climate_hero_points += points
        self.check_level_up()
        self.check_achievements()
    
    def check_level_up(self):
        """Check if user should level up"""
        points = st.session_state.climate_hero_points
        new_level = 1 + (points // 50)  # Level up every 50 points
        if new_level > st.session_state.climate_hero_level:
            st.session_state.climate_hero_level = new_level
            st.balloons()
            st.success(f"🎉 Level Up! You're now Level {new_level}!")
    
    def check_achievements(self):
        """Check and unlock achievements based on user actions"""
        actions = st.session_state.user_actions
        
        # Data Explorer
        if not self.achievements['data_explorer']['unlocked']:
            self.achievements['data_explorer']['unlocked'] = True
            st.session_state.unlocked_achievements.append('data_explorer')
            self.award_points('achievement', self.achievements['data_explorer']['points'])
            self.show_achievement_notification('data_explorer')
        
        # Chart Master
        if actions['charts_viewed'] >= 5 and not self.achievements['chart_master']['unlocked']:
            self.achievements['chart_master']['unlocked'] = True
            st.session_state.unlocked_achievements.append('chart_master')
            self.award_points('achievement', self.achievements['chart_master']['points'])
            self.show_achievement_notification('chart_master')
        
        # AI Consultant
        if actions['ai_questions'] >= 3 and not self.achievements['ai_consultant']['unlocked']:
            self.achievements['ai_consultant']['unlocked'] = True
            st.session_state.unlocked_achievements.append('ai_consultant')
            self.award_points('achievement', self.achievements['ai_consultant']['points'])
            self.show_achievement_notification('ai_consultant')
        
        # Data Analyst
        if actions['data_exports'] >= 3 and not self.achievements['data_analyst']['unlocked']:
            self.achievements['data_analyst']['unlocked'] = True
            st.session_state.unlocked_achievements.append('data_analyst')
            self.award_points('achievement', self.achievements['data_analyst']['points'])
            self.show_achievement_notification('data_analyst')
        
        # Global Citizen
        if len(actions['countries_explored']) >= 5 and not self.achievements['global_citizen']['unlocked']:
            self.achievements['global_citizen']['unlocked'] = True
            st.session_state.unlocked_achievements.append('global_citizen')
            self.award_points('achievement', self.achievements['global_citizen']['points'])
            self.show_achievement_notification('global_citizen')
        
        # Climate Hero
        if st.session_state.climate_hero_points >= 100 and not self.achievements['climate_hero']['unlocked']:
            self.achievements['climate_hero']['unlocked'] = True
            st.session_state.unlocked_achievements.append('climate_hero')
            self.award_points('achievement', self.achievements['climate_hero']['points'])
            self.show_achievement_notification('climate_hero')
    
    def show_achievement_notification(self, achievement_id):
        """Show temporary achievement notification that disappears"""
        achievement = self.achievements[achievement_id]
        
        # Create a unique key for this notification
        notification_key = f"achievement_{achievement_id}_{int(time.time())}"
        
        # Store notification in session state with timestamp
        if 'temp_notifications' not in st.session_state:
            st.session_state.temp_notifications = {}
        
        st.session_state.temp_notifications[notification_key] = {
            'achievement': achievement,
            'timestamp': time.time(),
            'shown': False
        }
    
    def display_temp_notifications(self):
        """Display and manage temporary notifications"""
        if 'temp_notifications' not in st.session_state:
            return
        
        current_time = time.time()
        notifications_to_remove = []
        
        for key, notification_data in st.session_state.temp_notifications.items():
            # Check if notification should be shown (not shown yet and within 5 seconds)
            if (not notification_data['shown'] and 
                current_time - notification_data['timestamp'] < 5):
                
                # Show the notification
                achievement = notification_data['achievement']
                st.markdown(f"""
                <div class="achievement-notification" id="{key}">
                    <h3>{achievement['icon']} Achievement Unlocked!</h3>
                    <p><strong>{achievement['name']}</strong></p>
                    <p>{achievement['description']}</p>
                    <p>+{achievement['points']} points earned!</p>
                    <div style="background: rgba(255,255,255,0.2); height: 3px; border-radius: 2px; margin-top: 0.5rem;">
                        <div style="background: #f093fb; height: 100%; border-radius: 2px; animation: progressBar 5s linear forwards;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Mark as shown
                st.session_state.temp_notifications[key]['shown'] = True
                
                # Trigger balloons
                st.balloons()
                
            # Remove notifications older than 5 seconds
            elif current_time - notification_data['timestamp'] >= 5:
                notifications_to_remove.append(key)
        
        # Clean up old notifications
        for key in notifications_to_remove:
            del st.session_state.temp_notifications[key]
    
    def display_gamification_sidebar(self):
        """Display gamification elements in sidebar"""
        st.sidebar.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h3>🏆 Climate Hero</h3>
            <h2>Level {}</h2>
            <p>{} Points</p>
        </div>
        """.format(st.session_state.climate_hero_level, st.session_state.climate_hero_points), 
        unsafe_allow_html=True)
        
        # Progress bar to next level
        points_to_next = 50 - (st.session_state.climate_hero_points % 50)
        progress = 1 - (points_to_next / 50)
        st.sidebar.progress(progress)
        st.sidebar.caption(f"📈 {points_to_next} points to Level {st.session_state.climate_hero_level + 1}")
        
        # Recent achievements
        if st.session_state.unlocked_achievements:
            st.sidebar.markdown("### 🎖️ Recent Achievements")
            for achievement_id in st.session_state.unlocked_achievements[-3:]:  # Show last 3
                achievement = self.achievements[achievement_id]
                st.sidebar.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.1); padding: 0.5rem; border-radius: 8px; margin: 0.25rem 0;">
                    <strong>{achievement['icon']} {achievement['name']}</strong><br>
                    <small>{achievement['description']}</small><br>
                    <small>+{achievement['points']} points</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Available achievements
        st.sidebar.markdown("### 🎯 Available Achievements")
        for achievement_id, achievement in self.achievements.items():
            if not achievement['unlocked']:
                st.sidebar.markdown(f"""
                <div style="background: rgba(0,0,0,0.05); padding: 0.5rem; border-radius: 8px; margin: 0.25rem 0; opacity: 0.6;">
                    <strong>🔒 {achievement['name']}</strong><br>
                    <small>{achievement['description']}</small><br>
                    <small>+{achievement['points']} points</small>
                </div>
                """, unsafe_allow_html=True)

# Initialize gamification system
climate_hero = ClimateHeroSystem()

# Custom CSS for better styling
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling - make it smaller and cleaner */
    .css-1d391kg {
        width: 280px !important;
        min-width: 280px !important;
    }
    
    .css-1lcbmhc {
        width: 280px !important;
        min-width: 280px !important;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Enhanced Header styling with climate theme */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 2px;
        line-height: 1.2;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 5px rgba(102, 126, 234, 0.3)); }
        to { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.6)); }
    }
    
    /* Enhanced Section titles with climate theme */
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 2.5rem 0 1.5rem 0;
        padding: 1rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        border-left: 6px solid #f093fb;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .section-title::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .section-title:hover::before {
        left: 100%;
    }
    
    .section-title:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.25);
    }
    
    /* Enhanced Metric cards with climate theme */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 0.75rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        border: 2px solid transparent;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #f093fb);
        animation: rainbow 3s linear infinite;
    }
    
    @keyframes rainbow {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.35);
        border-color: rgba(255,255,255,0.3);
    }
    
    .metric-card h3 {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card h2 {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Enhanced Chat bubble with climate theme */
    .chat-bubble {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
        font-size: 1.1rem;
        color: #2c3e50;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 2px solid #e9ecef;
        line-height: 1.7;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .chat-bubble:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    /* Enhanced Buttons with climate theme */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Enhanced Sidebar styling with climate theme */
    .css-1d391kg .css-1lcbmhc {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 2px solid #e9ecef;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    }
    
    /* Enhanced Sidebar headers with climate theme */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Enhanced Input fields with climate theme */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e9ecef;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        transform: translateY(-1px);
    }
    
    /* Enhanced Multiselect with climate theme */
    .stMultiSelect > div > div {
        border-radius: 12px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    }
    
    /* Enhanced Dataframe styling with climate theme */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 2px solid #e9ecef;
    }
    
    /* Enhanced Plotly charts with climate theme */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    /* Enhanced Footer with climate theme */
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 1rem;
        margin-top: 4rem;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        border-top: 4px solid #667eea;
        box-shadow: 0 -4px 20px rgba(102, 126, 234, 0.1);
    }
    
    /* Climate-themed loading animation */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Floating action button for quick actions */
    .floating-action {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .floating-action:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Enhanced achievement notification with fade out */
    .achievement-notification {
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        animation: slideInFadeOut 5s ease-in-out forwards;
        z-index: 1000;
        max-width: 300px;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    @keyframes slideInFadeOut {
        0% { 
            transform: translateX(100%); 
            opacity: 0; 
        }
        10% { 
            transform: translateX(0); 
            opacity: 1; 
        }
        80% { 
            transform: translateX(0); 
            opacity: 1; 
        }
        100% { 
            transform: translateX(100%); 
            opacity: 0; 
        }
    }
    
    .achievement-notification h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        text-align: center;
    }
    
    .achievement-notification p {
        margin: 0.25rem 0;
        text-align: center;
        font-size: 0.9rem;
    }
    
    .achievement-notification strong {
        color: #f093fb;
        font-weight: 700;
    }
    
    @keyframes progressBar {
        0% { width: 100%; }
        100% { width: 0%; }
    }
    
    /* Climate-themed progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Enhanced tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        text-align: center;
        border-radius: 8px;
        padding: 0.5rem;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.9rem;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load the cleaned OWID CO2 data"""
    project_root = Path(__file__).parent.parent.parent
    data_path = project_root / 'data' / 'processed' / 'cleaned_owid_co2_data.csv'
    
    if data_path.exists():
        return pd.read_csv(data_path)
    else:
        st.error('Processed OWID CO2 data not found. Please run the data preparation script.')
        return None

def create_metrics(df):
    """Create key metrics cards for OWID data"""
    if df is None:
        return
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    total_emissions = latest_data['co2'].sum()
    total_population = latest_data['population'].sum()
    # Set global average per capita to 4.8 tons as requested
    avg_per_capita = 4.8
    total_countries = df['country'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total CO2 Emissions</h3>
            <h2>{total_emissions:,.0f} t</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Global Avg per Capita</h3>
            <h2>{avg_per_capita:.1f} t</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Countries Analyzed</h3>
            <h2>{total_countries}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Latest Year</h3>
            <h2>{latest_year}</h2>
        </div>
        """, unsafe_allow_html=True)

def create_emissions_by_country_chart(df, theme="plotly"):
    """Create emissions by country chart for OWID data"""
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    country_emissions = latest_data.groupby('country')['co2'].sum().reset_index()
    fig = px.bar(
        country_emissions.nlargest(20, 'co2'),
        x='co2',
        y='country',
        orientation='h',
        title=f'Top 20 CO2 Emitting Countries ({latest_year})',
        color='co2',
        color_continuous_scale='viridis',
        text='co2'
    )
    fig.update_layout(
        template=theme,
        title_font_size=18,
        title_font_color='#2c3e50',
        xaxis_title="CO2 Emissions (t)",
        yaxis_title="Country",
        showlegend=False,
        height=600,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
    return fig

def create_emissions_by_fuel_chart(df, theme="plotly"):
    """Create emissions by fuel source over time"""
    fuels = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']
    fuel_names = ['Coal', 'Oil', 'Gas', 'Cement', 'Flaring']
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#8B4513']
    yearly = df.groupby('year')[fuels].sum().reset_index()
    fig = go.Figure()
    for fuel, name, color in zip(fuels, fuel_names, colors):
        fig.add_trace(go.Scatter(
            x=yearly['year'],
            y=yearly[fuel],
            mode='lines',
            name=name,
            line=dict(color=color, width=3)
        ))
    fig.update_layout(
        title='Global CO2 Emissions by Fuel Source Over Time',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions (t)',
        height=500,
        template=theme
    )
    return fig

def create_per_capita_chart(df, theme="plotly"):
    """Create per capita emissions chart"""
    yearly = df.groupby('year').agg({'co2': 'sum', 'population': 'sum'}).reset_index()
    yearly['co2_per_capita'] = yearly['co2'] / yearly['population']
    fig = px.line(
        yearly,
        x='year',
        y='co2_per_capita',
        title='Global CO2 Emissions per Capita Over Time',
        markers=True
    )
    fig.update_layout(
        template=theme,
        title_font_size=18,
        title_font_color='#2c3e50',
        xaxis_title="Year",
        yaxis_title="CO2 per Capita (t)",
        height=450,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_cumulative_emissions_chart(df, theme="plotly"):
    """Create cumulative emissions chart over time"""
    yearly = df.groupby('year')['co2'].sum().reset_index()
    yearly['cumulative_co2'] = yearly['co2'].cumsum()
    
    fig = px.line(
        yearly,
        x='year',
        y='cumulative_co2',
        title='Cumulative Global CO2 Emissions Over Time',
        markers=True
    )
    fig.update_layout(
        template=theme,
        title_font_size=18,
        title_font_color='#2c3e50',
        xaxis_title="Year",
        yaxis_title="Cumulative CO2 Emissions (t)",
        height=450,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_fuel_source_pie_chart(df, theme="plotly"):
    """Create fuel source percentage pie chart for latest year"""
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    
    # Sum fuel sources for latest year
    fuel_sources = {
        'Coal': latest_data['coal_co2'].sum(),
        'Oil': latest_data['oil_co2'].sum(),
        'Gas': latest_data['gas_co2'].sum(),
        'Cement': latest_data['cement_co2'].sum(),
        'Flaring': latest_data['flaring_co2'].sum()
    }
    
    # Remove zero values
    fuel_sources = {k: v for k, v in fuel_sources.items() if v > 0}
    
    if not fuel_sources:
        st.warning("No fuel source data available for the selected year")
        return go.Figure()
    
    fig = px.pie(
        values=list(fuel_sources.values()),
        names=list(fuel_sources.keys()),
        title=f'Global CO2 Emissions by Fuel Source ({latest_year})',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        template=theme,
        title_font_size=18,
        title_font_color='#2c3e50',
        height=450,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_ai_recommendations(df):
    """Generate AI-powered recommendations (OWID version)"""
    # This function is deprecated - we now use the real-time AI agent
    # Keeping for compatibility but it's not used in the main flow
    if df is None or df.empty:
        return []
    
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    
    if latest_data.empty:
        return []
    
    total_emissions = latest_data['co2'].sum()
    highest_emitter = latest_data.loc[latest_data['co2'].idxmax()]
    highest_country = latest_data.groupby('country')['co2'].sum().idxmax()
    
    recommendations = [
        {
            "category": "Immediate Actions",
            "recommendations": [
                f"Focus reduction efforts on {highest_country} (highest emissions)",
                f"Study best practices from countries with lower emissions",
                "Implement real-time emission monitoring systems"
            ]
        },
        {
            "category": "Policy Recommendations",
            "recommendations": [
                "Establish country-specific emission reduction targets",
                "Implement carbon pricing or cap-and-trade systems",
                "Create incentives for renewable energy adoption"
            ]
        },
        {
            "category": "Long-term Strategy",
            "recommendations": [
                "Develop comprehensive carbon neutrality roadmap",
                "Invest in carbon capture and storage technologies",
                "Establish international partnerships for sustainable development"
            ]
        }
    ]
    
    return recommendations

def main():
    """Main application function"""
    # Initialize gamification system
    climate_hero.initialize_user_session()
    
    # Clear cache to ensure fresh AI agent loading
    if 'ai_agent' in st.session_state:
        del st.session_state['ai_agent']
    
    # Initialize AI agent
    if 'ai_agent' not in st.session_state:
        st.session_state['ai_agent'] = create_ai_agent()
    
    ai_agent = st.session_state['ai_agent']
    
    # Enhanced Header with climate theme
    st.markdown("""
    <div class="main-header">
        🌍 Climate Change Analysis Platform
    </div>
    """, unsafe_allow_html=True)
    
    # Subtitle with climate theme
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #6c757d; font-size: 1.2rem; font-weight: 500;">
        📊 Data-Driven Insights • 🤖 AI-Powered Recommendations • 🏆 Climate Hero Journey
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Display gamification sidebar
    climate_hero.display_gamification_sidebar()
    
    # Display temporary achievement notifications
    climate_hero.display_temp_notifications()
    
    # Sidebar with enhanced styling
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   background-clip: text;">🎛️ Controls</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter options
    st.sidebar.markdown("### 🌍 Country Selection")
    all_countries = sorted(df['country'].unique())
    selected_countries = st.sidebar.multiselect(
        "Select countries to analyze:",
        all_countries,
        default=all_countries[:10],
        help="Choose countries to include in your analysis"
    )
    
    # Award points for exploring countries
    if selected_countries:
        climate_hero.award_points('country_exploration', 5)
        st.session_state.user_actions['countries_explored'].update(selected_countries)
    
    st.sidebar.markdown("### 📅 Year Range")
    year_range = st.sidebar.slider(
        "Select year range:",
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max())),
        help="Choose the time period for analysis"
    )
    
    # Award points for exploring years
    if year_range:
        climate_hero.award_points('year_exploration', 3)
        st.session_state.user_actions['years_analyzed'].update(range(year_range[0], year_range[1] + 1))
    
    # Filter data based on selections
    filtered_df = df[
        (df['country'].isin(selected_countries)) &
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1])
    ]
    
    if not filtered_df.empty:
        # Award points for data exploration
        climate_hero.award_points('data_exploration', 10)
        
        # Enhanced section title
        st.markdown('<div class="section-title">📊 Key Metrics Overview</div>', unsafe_allow_html=True)
        
        # Create metrics with enhanced styling
        create_metrics(filtered_df)
        
        # Award points for viewing metrics
        climate_hero.award_points('metrics_viewed', 5)
        
        # Enhanced section title for charts
        st.markdown('<div class="section-title">📈 Interactive Visualizations</div>', unsafe_allow_html=True)
        
        # Chart selection with enhanced styling
        chart_options = {
            "Emissions by Country": "country",
            "Global CO2 Trends": "trends", 
            "Per Capita Emissions": "per_capita",
            "Fuel Source Breakdown": "fuel",
            "Cumulative Emissions": "cumulative"
        }
        
        selected_charts = st.multiselect(
            "🎨 Select charts to display:",
            list(chart_options.keys()),
            default=["Emissions by Country", "Global CO2 Trends"],
            help="Choose which visualizations to show"
        )
        
        # Track charts viewed for gamification
        charts_viewed_count = 0
        
        # Display selected charts with enhanced styling
        if "Emissions by Country" in selected_charts:
            st.markdown("### 🏭 Top CO2 Emitting Countries")
            fig = create_emissions_by_country_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
            charts_viewed_count += 1
            climate_hero.award_points('chart_viewed', 2)
        
        if "Global CO2 Trends" in selected_charts:
            st.markdown("### 📈 Global CO2 Emissions Over Time")
            fig = create_emissions_by_fuel_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
            charts_viewed_count += 1
            climate_hero.award_points('chart_viewed', 2)
        
        if "Per Capita Emissions" in selected_charts:
            st.markdown("### 👥 Per Capita CO2 Emissions")
            fig = create_per_capita_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
            charts_viewed_count += 1
            climate_hero.award_points('chart_viewed', 2)
        
        if "Fuel Source Breakdown" in selected_charts:
            st.markdown("### ⛽ Fuel Source Distribution")
            fig = create_fuel_source_pie_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
            charts_viewed_count += 1
            climate_hero.award_points('chart_viewed', 2)
        
        if "Cumulative Emissions" in selected_charts:
            st.markdown("### 📊 Cumulative Global Emissions")
            fig = create_cumulative_emissions_chart(filtered_df)
            st.plotly_chart(fig, use_container_width=True)
            charts_viewed_count += 1
            climate_hero.award_points('chart_viewed', 2)
        
        # Update charts viewed count
        st.session_state.user_actions['charts_viewed'] += charts_viewed_count
        
        # Enhanced AI section with gamification
        st.markdown('<div class="section-title">🤖 AI Climate Analysis & Recommendations</div>', unsafe_allow_html=True)
        
        # AI query interface with enhanced styling
        col_ai1, col_ai2 = st.columns([3, 1])
        
        with col_ai1:
            user_query = st.text_input(
                "💭 Ask the AI about climate data, policies, or trends:",
                placeholder="e.g., 'What policies work best for energy?' or 'How to reduce emissions?'",
                help="Ask specific questions about emissions reduction strategies"
            )
        
        with col_ai2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔍 Get Recommendations", type="primary"):
                pass
        
        # Generate AI recommendations
        ai_output = ai_agent.generate_realtime_recommendations(filtered_df, user_query=user_query, filters={
            'countries': selected_countries
        })
        
        # Award points for AI interaction
        if user_query and user_query.strip():
            climate_hero.award_points('ai_question', 10)
            st.session_state.user_actions['ai_questions'] += 1
        
        # Safety check for ai_answer
        ai_answer = ai_output.get('ai_answer', 'Analyzing data and generating recommendations...')
        
        # Enhanced AI recommendation styling
        st.markdown("""
        <style>
        .ai-recommendation-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            margin: 1.5rem 0;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        .ai-recommendation-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        }
        .ai-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 1.3rem;
            font-weight: 700;
        }
        .ai-content {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #fff;
            font-size: 1.1rem;
            line-height: 1.6;
            backdrop-filter: blur(10px);
        }
        .confidence-badge {
            background: rgba(255, 255, 255, 0.2);
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            display: inline-block;
            font-size: 0.95rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .ai-icon {
            font-size: 2rem;
            margin-right: 0.75rem;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Enhanced AI recommendation display
        st.markdown(f"""
        <div class="ai-recommendation-box">
            <div class="ai-header">
                <span class="ai-icon">🤖</span>
                <span>AI Climate Analysis & Recommendations</span>
            </div>
            <div class="ai-content">
                <strong>💡 Key Insights:</strong><br><br>
                {ai_answer}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced confidence score
        confidence = ai_output['confidence_score']*100
        st.markdown(f"""
        <div style="text-align: right; margin: 1rem 0;">
            <span class="confidence-badge">
                🎯 Confidence Level: {confidence:.1f}%
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Display ethics compliance information
        if 'ethics_compliance' in ai_output:
            with st.expander("📋 Ethics Compliance Details", expanded=False):
                ethics = ai_output['ethics_compliance']
                st.markdown("**Transparency Notes:**")
                for note in ethics.get('transparency_notes', []):
                    st.markdown(f"• {note}")
                
                st.markdown("**Data Quality Assessment:**")
                st.markdown(f"• Data Quality Score: {ai_output['context_summary'].get('data_quality_score', 0):.1%}")
                st.markdown(f"• Uncertainty Level: {ai_output['context_summary'].get('uncertainty_level', 'unknown')}")
                st.markdown(f"• Anomalies Detected: {ai_output['context_summary'].get('anomalies_detected', 0)}")
        
        # Data table with better styling
        st.markdown('<div class="section-title">📋 Data Overview</div>', unsafe_allow_html=True)
        
        # Add search functionality
        search_term = st.text_input("🔍 Search organizations or countries", placeholder="Type to filter data...")
        if search_term:
            filtered_df_display = filtered_df[
                filtered_df['country'].str.contains(search_term, case=False)
            ]
        else:
            filtered_df_display = filtered_df
        
        st.dataframe(
            filtered_df_display, 
            use_container_width=True,
            hide_index=True
        )
        
        # Export section with better styling and gamification
        st.markdown('<div class="section-title">💾 Export & Share</div>', unsafe_allow_html=True)
        
        col7, col8, col9 = st.columns(3)
        
        with col7:
            csv = filtered_df.to_csv(index=False)
            if st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"carbon_emissions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                help="Download data as CSV file"
            ):
                climate_hero.award_points('data_export', 15)
                st.session_state.user_actions['data_exports'] += 1
        
        with col8:
            json_data = filtered_df.to_json(orient='records', indent=2)
            if st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"carbon_emissions_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                help="Download data as JSON file"
            ):
                climate_hero.award_points('data_export', 15)
                st.session_state.user_actions['data_exports'] += 1
        
        with col9:
            # Generate a simple report
            report_text = f"""
# Carbon Emissions Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Records Analyzed: {len(filtered_df)}
- Total CO2 Emissions: {filtered_df['co2'].sum():,.0f} tonnes
- Average Emissions per Record: {filtered_df['co2'].mean():,.0f} tonnes
- Highest Emitting Country: {filtered_df.loc[filtered_df['co2'].idxmax(), 'country']}
- Data Year Range: {filtered_df['year'].min()} - {filtered_df['year'].max()}

## AI Recommendations
{ai_answer}

## Data Details
{filtered_df.to_string()}
            """
            if st.download_button(
                label="📄 Download Report",
                data=report_text,
                file_name=f"carbon_emissions_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                help="Download analysis report as Markdown"
            ):
                climate_hero.award_points('data_export', 15)
                st.session_state.user_actions['data_exports'] += 1
    
    else:
        st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
    
    # Enhanced Footer with climate theme and gamification
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div>
                <h3 style="margin: 0; color: #667eea;">🌱 Climate Change Analysis Platform</h3>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Making data-driven policy decisions</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; font-weight: 600;">🏆 Climate Hero Level {}</p>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem;">{} Points Earned</p>
            </div>
        </div>
        <div style="border-top: 1px solid #e9ecef; padding-top: 1rem; text-align: center;">
            <p style="margin: 0; font-size: 0.8rem;">Built with Streamlit | Ethical AI Approach | Granite Guidelines</p>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem;">© 2024 Climate Change Analysis Platform</p>
        </div>
    </div>
    """.format(st.session_state.climate_hero_level, st.session_state.climate_hero_points), 
    unsafe_allow_html=True)

if __name__ == "__main__":
    main() 