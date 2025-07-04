#!/usr/bin/env python3
"""
Test script for AI agent functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from ai_agent.agent import create_ai_agent

def test_ai_agent():
    """Test the AI agent with energy sector queries"""
    
    # Create sample data
    data = {
        'country': ['USA', 'China', 'India', 'Germany'],
        'co2': [5000, 10000, 3000, 2000],
        'coal_co2': [2000, 6000, 1500, 800],
        'oil_co2': [1500, 2000, 800, 600],
        'gas_co2': [1000, 1500, 500, 400],
        'year': [2020, 2020, 2020, 2020],
        'population': [330000000, 1400000000, 1380000000, 83000000]
    }
    
    df = pd.DataFrame(data)
    
    # Create AI agent
    ai_agent = create_ai_agent()
    
    # Test energy sector query
    print("Testing energy sector query...")
    result = ai_agent.generate_realtime_recommendations(
        df, 
        user_query="how to reduce emissions in energy sector",
        filters={'countries': ['USA', 'China']}
    )
    
    print(f"AI Answer: {result.get('ai_answer', 'No answer')}")
    print(f"Confidence: {result.get('confidence_score', 0):.1%}")
    
    # Test general query
    print("\nTesting general query...")
    result2 = ai_agent.generate_realtime_recommendations(
        df, 
        user_query="which country has highest emissions",
        filters={'countries': ['USA', 'China']}
    )
    
    print(f"AI Answer: {result2.get('ai_answer', 'No answer')}")
    print(f"Confidence: {result2.get('confidence_score', 0):.1%}")

    if has_energy_keyword and has_policy_keyword:
        # energy policy recommendations

if __name__ == "__main__":
    test_ai_agent() 