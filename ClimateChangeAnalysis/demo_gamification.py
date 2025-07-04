#!/usr/bin/env python3
"""
Climate Hero Gamification Demo
Showcase the gamification features and visual enhancements
"""

import streamlit as st

def demo_gamification():
    """Demo the gamification features"""
    
    st.set_page_config(
        page_title="Climate Hero Gamification Demo",
        page_icon="🏆",
        layout="wide"
    )
    
    # Enhanced header with climate theme
    st.markdown("""
    <div style="font-size: 2.8rem; font-weight: 800; text-align: center; margin-bottom: 2rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                background-clip: text; letter-spacing: 2px; line-height: 1.2;">
        🏆 Climate Hero Gamification Demo
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #6c757d; font-size: 1.2rem; font-weight: 500;">
        🎮 Experience the Future of Climate Data Analysis
    </div>
    """, unsafe_allow_html=True)
    
    # Demo sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0;">
            <h2>🎮 Gamification Features</h2>
            <ul style="text-align: left;">
                <li>🏆 Climate Hero Levels</li>
                <li>🎖️ Achievement System</li>
                <li>📊 Points System</li>
                <li>🎯 Progress Tracking</li>
                <li>🌟 Engagement Rewards</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 20px; color: white; margin: 1rem 0;">
            <h2>🎨 Visual Enhancements</h2>
            <ul style="text-align: left;">
                <li>🌈 Climate-themed gradients</li>
                <li>✨ Animated elements</li>
                <li>🎭 Interactive hover effects</li>
                <li>🌊 Smooth transitions</li>
                <li>🌟 Achievement notifications</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Achievement showcase
    st.markdown("""
    <div style="font-size: 1.6rem; font-weight: 700; color: #2c3e50; margin: 2.5rem 0 1.5rem 0;
                padding: 1rem 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; border-radius: 15px;">
        🏅 Available Achievements
    </div>
    """, unsafe_allow_html=True)
    
    # Achievement grid
    achievements = [
        {"icon": "📊", "name": "Data Explorer", "description": "First data exploration", "points": 10},
        {"icon": "📈", "name": "Chart Master", "description": "View 5 different charts", "points": 25},
        {"icon": "🤖", "name": "AI Consultant", "description": "Ask 3 questions to AI", "points": 50},
        {"icon": "💾", "name": "Data Analyst", "description": "Export data 3 times", "points": 30},
        {"icon": "🌐", "name": "Global Citizen", "description": "Explore 5+ countries", "points": 60},
        {"icon": "🏆", "name": "Climate Hero", "description": "Earn 100+ points", "points": 100}
    ]
    
    cols = st.columns(3)
    for i, achievement in enumerate(achievements):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 15px; color: white; margin: 0.5rem 0; text-align: center;">
                <h3 style="font-size: 2rem; margin: 0;">{achievement['icon']}</h3>
                <h4 style="margin: 0.5rem 0;">{achievement['name']}</h4>
                <p style="margin: 0.25rem 0; font-size: 0.9rem;">{achievement['description']}</p>
                <p style="margin: 0.25rem 0; font-weight: bold;">+{achievement['points']} points</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0; padding: 2rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; color: white;">
        <h2>🚀 Ready to Become a Climate Hero?</h2>
        <p style="font-size: 1.2rem; margin: 1rem 0;">Launch the full application and start your journey!</p>
        <p style="font-size: 1rem; opacity: 0.9;">Run: <code>streamlit run src/web_app/app.py</code></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    demo_gamification() 