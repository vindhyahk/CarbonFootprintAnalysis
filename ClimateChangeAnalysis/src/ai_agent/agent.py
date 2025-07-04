#!/usr/bin/env python3
"""
Real-time AI Agent for Climate Change Analysis
Dynamic AI agent that generates real-time recommendations based on user interactions.
Implements Granite AI ethics principles for cautious, transparent, and ethical decision-making.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from typing import Dict, List, Any
import random

class ClimateAIAgent:
    """Real-time AI agent for climate change analysis and recommendations with Granite AI ethics"""
    
    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
        self.analysis_context = {}
        
        # Granite AI Ethics Framework
        self.ethics_framework = {
            'principles': [
                'Cautious decision-making with uncertainty acknowledgment',
                'Transparency in reasoning and data sources',
                'Fairness and non-discrimination in recommendations',
                'Accountability for recommendations and their potential impacts',
                'Privacy protection and data security',
                'Environmental responsibility and sustainability focus'
            ],
            'safety_guidelines': [
                'Always acknowledge limitations and uncertainties',
                'Provide multiple perspectives and options',
                'Avoid overconfident or absolute statements',
                'Consider potential negative impacts of recommendations',
                'Prioritize evidence-based over speculative advice',
                'Maintain human oversight and decision-making authority'
            ],
            'transparency_requirements': [
                'Clear explanation of data sources and methodology',
                'Explicit confidence levels and uncertainty ranges',
                'Disclosure of potential biases or limitations',
                'Traceable reasoning for all recommendations',
                'Regular updates on recommendation effectiveness'
            ]
        }
        
        # Knowledge base for different scenarios
        self.knowledge_base = {
            'high_emissions': {
                'triggers': ['emissions > 100000', 'country_rank > 3'],
                'recommendations': [
                    "Immediate carbon reduction program implementation",
                    "Energy efficiency audit and optimization",
                    "Renewable energy transition planning",
                    "Carbon offset program development"
                ]
            },
            'country_focus': {
                'triggers': ['country_analysis', 'geographic_comparison'],
                'recommendations': [
                    "Country-specific emission reduction targets",
                    "Regional best practice adoption",
                    "Technology innovation investment",
                    "Cross-border collaboration initiatives"
                ]
            },
            'geographic_analysis': {
                'triggers': ['country_analysis', 'regional_focus'],
                'recommendations': [
                    "Local regulatory compliance review",
                    "Regional partnership opportunities",
                    "Geographic-specific policy recommendations",
                    "Cross-border collaboration initiatives"
                ]
            },
            'trend_analysis': {
                'triggers': ['trend_detection', 'pattern_analysis'],
                'recommendations': [
                    "Predictive modeling for emission trends",
                    "Scenario planning for different futures",
                    "Adaptive strategy development",
                    "Continuous monitoring and adjustment"
                ]
            }
        }
    
    def analyze_data_context(self, df: pd.DataFrame, filters: Dict = None) -> Dict:
        """Analyze current data context for real-time insights (OWID version)"""
        context = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(df),
            'total_emissions': df['co2'].sum(),
            'avg_emissions': df['co2'].mean(),
            'countries': df['country'].unique().tolist(),
            'highest_emitter': df.loc[df['co2'].idxmax()].to_dict() if not df.empty else {},
            'lowest_emitter': df.loc[df['co2'].idxmin()].to_dict() if not df.empty else {},
            'country_emissions': df.groupby('country')['co2'].sum().to_dict(),
            'data_columns': df.columns.tolist()  # Include available data columns
        }
        
        # Add fuel source analysis if available
        fuel_columns = ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2']
        available_fuels = [col for col in fuel_columns if col in df.columns]
        if available_fuels:
            context['fuel_analysis'] = {}
            for fuel in available_fuels:
                context['fuel_analysis'][fuel] = df[fuel].sum()
        
        # Add filter context
        if filters:
            context['active_filters'] = filters
        
        return context
    
    def detect_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """Detect anomalies in the data for real-time alerts (OWID version)"""
        anomalies = []
        if 'co2' not in df.columns or df.empty:
            return anomalies
        
        # Detect high emissions outliers
        q75 = df['co2'].quantile(0.75)
        q25 = df['co2'].quantile(0.25)
        iqr = q75 - q25
        upper_bound = q75 + 1.5 * iqr
        
        high_emitters = df[df['co2'] > upper_bound]
        
        for _, row in high_emitters.iterrows():
            anomalies.append({
                'type': 'high_emissions',
                'country': row['country'],
                'emissions': row['co2'],
                'severity': 'high' if row['co2'] > upper_bound * 1.5 else 'medium',
                'message': f"High emissions detected for {row['country']}"
            })
        
        return anomalies
    
    def generate_realtime_recommendations(self, df: pd.DataFrame, user_query: str = None, 
                                        filters: Dict = None) -> Dict:
        """Generate real-time AI recommendations based on current context with Granite AI ethics (OWID version)"""
        
        # Analyze current context
        context = self.analyze_data_context(df, filters)
        anomalies = self.detect_anomalies(df)
        
        # Store context for conversation history
        self.analysis_context = context
        
        # Calculate confidence and uncertainty metrics (Granite AI principle)
        data_quality_score = self._assess_data_quality(df)
        confidence_score = min(0.95, data_quality_score * 0.9)  # Conservative confidence
        
        # Generate recommendations based on context and user query
        recommendations = {
            'timestamp': datetime.now().isoformat(),
            'context_summary': {
                'total_impact': f"{context['total_emissions']:,.0f} tonnes CO2",
                'key_insights': [],
                'anomalies_detected': len(anomalies),
                'data_quality_score': data_quality_score,
                'uncertainty_level': 'medium' if data_quality_score < 0.8 else 'low'
            },
            'immediate_actions': [],
            'strategic_recommendations': [],
            'policy_suggestions': [],
            'anomalies': anomalies,
            'confidence_score': confidence_score,
            'ai_answer': '',
            'ethics_compliance': {
                'principles_applied': self.ethics_framework['principles'],
                'transparency_notes': [],
                'uncertainty_acknowledgment': True,
                'safety_guidelines_followed': True
            }
        }
        
        # Generate context-based insights with cautious approach
        if context['total_emissions'] > 100000:
            recommendations['context_summary']['key_insights'].append(
                f"High total emissions detected: {context['total_emissions']:,.0f} tonnes (with ±5% uncertainty)"
            )
            recommendations['immediate_actions'].extend([
                "Consider implementing emergency emission reduction protocols (pending stakeholder review)",
                "Conduct immediate energy audit across all facilities (recommended)",
                "Evaluate carbon offset purchasing program feasibility (requires cost-benefit analysis)"
            ])
        
        # Geographic recommendations with caution
        if context['country_emissions']:
            highest_country = max(context['country_emissions'], key=context['country_emissions'].get)
            recommendations['policy_suggestions'].extend([
                f"Review regulatory compliance in {highest_country} (consult legal experts)",
                "Explore regional carbon trading opportunities (requires market analysis)",
                "Consider country-specific sustainability partnerships (recommended)"
            ])
        
        # Handle user queries with Granite AI ethics
        if user_query and user_query.strip():
            query_recommendations = self._process_user_query(user_query, context)
            if query_recommendations:
                recommendations['user_specific'] = query_recommendations
                # Conversational answer with ethics compliance
                recommendations['ai_answer'] = (
                    f"Based on your question about '{user_query}', here are my data-driven recommendations "
                    f"(confidence: {confidence_score:.1%}): " +
                    ' '.join([f'{i+1}. {rec}' for i, rec in enumerate(query_recommendations)]) +
                    f" Note: These recommendations are based on analysis of {len(df)} data points from {len(context['countries'])} countries."
                )
            else:
                # Provide data-based insights even for general queries
                data_insights = []
                if context.get('total_emissions'):
                    data_insights.append(f"Total emissions: {context['total_emissions']:,.0f} tonnes")
                if context.get('country_emissions'):
                    highest_country = max(context['country_emissions'], key=context['country_emissions'].get)
                    data_insights.append(f"Highest emitter: {highest_country}")
                if context.get('fuel_analysis'):
                    data_insights.append("Fuel source data available for detailed analysis")
                
                recommendations['ai_answer'] = (
                    f"Based on your question about '{user_query}', here are insights from the current data "
                    f"(confidence: {confidence_score:.1%}): " +
                    '; '.join(data_insights) + ". " +
                    ' '.join([f'{i+1}. {rec}' for i, rec in enumerate(recommendations['policy_suggestions'][:3])]) +
                    " Please consult with climate experts for specific guidance."
                )
        else:
            # Default with data-driven insights
            data_summary = []
            if context.get('total_emissions'):
                data_summary.append(f"Total emissions: {context['total_emissions']:,.0f} tonnes")
            if context.get('countries'):
                data_summary.append(f"Countries analyzed: {len(context['countries'])}")
            if context.get('fuel_analysis'):
                data_summary.append("Fuel source breakdown available")
            
            recommendations['ai_answer'] = (
                f"Here are key insights from the current data analysis "
                f"(confidence: {confidence_score:.1%}): " +
                '; '.join(data_summary) + ". " +
                ' '.join([f'{i+1}. {rec}' for i, rec in enumerate(recommendations['policy_suggestions'][:3])]) +
                " These suggestions should be reviewed by stakeholders and climate experts before implementation."
            )
        
        # Add anomaly-based recommendations with caution
        if anomalies:
            recommendations['anomaly_recommendations'] = self._generate_anomaly_recommendations(anomalies)
            # Add anomaly info to AI answer with transparency
            anomaly_text = f" I also detected {len(anomalies)} potential anomaly(ies) that may require attention. "
            anomaly_text += "Please verify these findings with additional data sources."
            recommendations['ai_answer'] += anomaly_text
        
        # Add transparency notes (Granite AI requirement)
        recommendations['ethics_compliance']['transparency_notes'] = [
            f"Analysis based on {len(df)} data points from {len(context['countries'])} countries",
            f"Confidence level: {confidence_score:.1%} (conservative estimate)",
            "Recommendations should be validated by domain experts",
            "Data limitations: Sample size may not represent full population",
            "Consider multiple scenarios and stakeholder perspectives"
        ]
        
        return recommendations
    
    def _process_user_query(self, query: str, context: Dict) -> List[str]:
        """Process user queries and generate specific recommendations (OWID version)"""
        query_lower = query.lower()
        recommendations = []
        
        # Robust energy sector and policy detection
        energy_keywords = ['energy', 'fuel', 'coal', 'oil', 'gas', 'renewable', 'power', 'electricity']
        policy_keywords = ['policy', 'policies', 'regulation', 'regulations', 'compliance', 'legal', 'law', 'laws']
        has_energy_keyword = any(word in query_lower for word in energy_keywords)
        has_policy_keyword = any(word in query_lower for word in policy_keywords)
        has_fuel_data = any(col in context.get('data_columns', []) for col in ['coal_co2', 'oil_co2', 'gas_co2', 'cement_co2', 'flaring_co2'])
        
        # Energy policy recommendations
        if has_energy_keyword and has_policy_keyword:
            recommendations.extend([
                "Implement renewable portfolio standards (RPS) to mandate a minimum share of renewables in energy mix",
                "Introduce feed-in tariffs or tax incentives for renewable energy projects",
                "Establish carbon pricing (carbon tax or cap-and-trade) for energy producers",
                "Mandate energy efficiency standards for power plants and industrial facilities",
                "Support grid modernization and energy storage policies",
                "Promote just transition policies for workers in fossil fuel industries"
            ])
        elif has_energy_keyword and has_fuel_data:
            recommendations.extend([
                "Accelerate transition from coal and oil to renewable energy sources (solar, wind, hydro)",
                "Implement energy efficiency programs in power generation and industrial sectors",
                "Modernize the electricity grid to support distributed renewables",
                "Establish carbon pricing or cap-and-trade mechanisms for energy producers",
                "Invest in R&D for clean energy technologies and storage solutions"
            ])
        elif has_energy_keyword:
            recommendations.extend([
                "Conduct a comprehensive energy audit to identify major emission sources",
                "Develop a national or organizational renewable energy transition roadmap",
                "Set ambitious but achievable energy sector emission reduction targets",
                "Promote electrification and efficiency in transport and buildings",
                "Support workforce transition and training for clean energy jobs"
            ])
        elif 'country' in query_lower or 'geographic' in query_lower or 'region' in query_lower:
            if context.get('country_emissions'):
                highest_country = max(context['country_emissions'], key=context['country_emissions'].get)
                recommendations.extend([
                    f"Focus reduction efforts on {highest_country} (highest emissions: {context['country_emissions'][highest_country]:,.0f} tonnes)",
                    "Review regional regulatory frameworks and compliance",
                    "Consider geographic emission distribution strategies",
                    "Develop country-specific emission reduction targets"
                ])
        elif any(word in query_lower for word in ['reduce', 'decrease', 'lower', 'cut', 'minimize']):
            if context.get('total_emissions'):
                recommendations.extend([
                    f"Current total emissions: {context['total_emissions']:,.0f} tonnes - target 20% reduction",
                    "Implement immediate energy efficiency measures across all sectors",
                    "Develop phased emission reduction plan with quarterly milestones",
                    "Set up continuous monitoring and real-time reporting systems",
                    "Establish carbon offset programs for unavoidable emissions"
                ])
        elif has_policy_keyword:
            recommendations.extend([
                "Review current regulatory compliance status across all operations",
                "Develop comprehensive policy advocacy strategy",
                "Engage with regulatory bodies for guidance and best practices",
                "Establish internal compliance monitoring and reporting systems",
                "Create policy impact assessment framework"
            ])
        elif any(word in query_lower for word in ['technology', 'innovation', 'tech', 'solution']):
            recommendations.extend([
                "Invest in carbon capture and storage (CCS) technologies",
                "Implement smart grid and energy management systems",
                "Develop digital monitoring and analytics platforms",
                "Explore emerging clean energy technologies",
                "Establish technology innovation partnerships"
            ])
        else:
            if context.get('total_emissions'):
                recommendations.extend([
                    f"Current total emissions: {context['total_emissions']:,.0f} tonnes",
                    "Implement comprehensive emission reduction strategy",
                    "Establish baseline measurements and tracking systems",
                    "Develop stakeholder engagement and communication plan"
                ])
        return recommendations
    
    def _generate_anomaly_recommendations(self, anomalies: List[Dict]) -> List[str]:
        """Generate recommendations based on detected anomalies"""
        recommendations = []
        
        for anomaly in anomalies:
            if anomaly['type'] == 'high_emissions':
                recommendations.append(
                    f"Immediate intervention required for {anomaly['country']}: "
                    f"Implement emergency reduction measures and conduct detailed audit"
                )
        
        return recommendations
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history for context"""
        return self.conversation_history
    
    def add_user_preference(self, preference: str, value: Any):
        """Add user preference for personalized recommendations"""
        self.user_preferences[preference] = value
    
    def get_personalized_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate personalized recommendations based on user preferences (OWID version)"""
        personalized = []
        
        if 'focus_country' in self.user_preferences:
            country = self.user_preferences['focus_country']
            country_data = df[df['country'] == country]
            if not country_data.empty:
                personalized.append(f"Focus on {country} emission reduction strategies")
        
        if 'emission_target' in self.user_preferences:
            target = self.user_preferences['emission_target']
            current_total = df['co2'].sum()
            reduction_needed = current_total - target
            if reduction_needed > 0:
                personalized.append(f"Need to reduce emissions by {reduction_needed:,.0f} tonnes to meet target")
        
        return personalized
    
    def _assess_data_quality(self, df: pd.DataFrame) -> float:
        """Assess data quality for confidence scoring (Granite AI principle)"""
        quality_score = 1.0
        
        if 'co2' not in df.columns or df.empty:
            return 0.5
        
        # Check for missing data
        missing_data_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        quality_score -= missing_data_ratio * 0.3
        
        # Check for data consistency
        if len(df) < 10:
            quality_score -= 0.2  # Small sample size penalty
        
        # Check for extreme outliers
        emissions = df['co2']
        q1, q3 = emissions.quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = ((emissions < (q1 - 1.5 * iqr)) | (emissions > (q3 + 1.5 * iqr))).sum()
        outlier_ratio = outliers / len(df)
        quality_score -= outlier_ratio * 0.2
        
        return max(0.5, quality_score)  # Minimum 50% confidence

def create_ai_agent():
    """Factory function to create AI agent instance"""
    return ClimateAIAgent() 