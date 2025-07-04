#!/usr/bin/env python3
"""
Test script for temporary achievement notifications
"""

import streamlit as st
import time

def test_notifications():
    """Test the temporary notification system"""
    
    st.set_page_config(
        page_title="Achievement Notification Test",
        page_icon="🏆",
        layout="wide"
    )
    
    st.title("🏆 Achievement Notification Test")
    st.markdown("Test the temporary achievement notification system")
    
    # Test notification button
    if st.button("🎉 Test Achievement Notification"):
        # Simulate achievement unlock
        st.markdown("""
        <div class="achievement-notification">
            <h3>🏆 Achievement Unlocked!</h3>
            <p><strong>Test Achievement</strong></p>
            <p>This is a test notification</p>
            <p>+50 points earned!</p>
            <div style="background: rgba(255,255,255,0.2); height: 3px; border-radius: 2px; margin-top: 0.5rem;">
                <div style="background: #f093fb; height: 100%; border-radius: 2px; animation: progressBar 5s linear forwards;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
    
    # CSS for the notification
    st.markdown("""
    <style>
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
    
    @keyframes progressBar {
        0% { width: 100%; }
        100% { width: 0%; }
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
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("""
    1. **Click the button above** to test the notification
    2. **Notification slides in** from the right
    3. **Stays visible for 5 seconds** with a progress bar
    4. **Automatically slides out** and disappears
    5. **No permanent clutter** on the page
    """)

if __name__ == "__main__":
    test_notifications() 