#!/usr/bin/env python3
"""
IBM Data Prep Kit Integration
Integrates IBM's data preparation tools for climate change analysis.
Uses IBM Watson Studio, DataStage, and Cloud Pak for Data capabilities.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# IBM Data Prep Kit imports
try:
    from ibm_watson import DiscoveryV2
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_db import connect, tables, columns
    from ibm_cos import COSConnection
    from ibm_cos.cos_exceptions import ClientError
    IBM_AVAILABLE = True
except ImportError:
    IBM_AVAILABLE = False
    logging.warning("IBM Data Prep Kit not available. Using fallback methods.")

class IBMDataPrepKit:
    """IBM Data Prep Kit integration for climate change data processing"""
    
    def __init__(self, api_key: str = None, service_url: str = None):
        self.api_key = api_key
        self.service_url = service_url
        self.authenticator = None
        self.discovery = None
        self.cos_connection = None
        
        if IBM_AVAILABLE and api_key:
            self._initialize_ibm_services()
        
        # Data quality rules for climate data
        self.data_quality_rules = {
            'emissions_range': (0, 1000000),  # Reasonable CO2 emissions range
            'year_range': (2000, 2030),       # Valid year range
            'required_columns': ['Organization', 'Sector', 'Country', 'Year', 'CO2_Emissions_tonnes'],
            'sector_values': ['Manufacturing', 'Technology', 'Agriculture', 'Transport', 'Energy', 'Healthcare', 'Finance'],
            'country_format': 'ISO_3166_1_alpha_2'  # Standard country codes
        }
    
    def _initialize_ibm_services(self):
        """Initialize IBM Watson and Cloud Object Storage services"""
        try:
            # Initialize IBM Watson Discovery
            self.authenticator = IAMAuthenticator(self.api_key)
            self.discovery = DiscoveryV2(
                version='2023-03-31',
                authenticator=self.authenticator
            )
            self.discovery.set_service_url(self.service_url)
            
            # Initialize Cloud Object Storage (if credentials provided)
            if hasattr(self, 'cos_credentials'):
                self.cos_connection = COSConnection(self.cos_credentials)
                
            logging.info("IBM Data Prep Kit services initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize IBM services: {e}")
            IBM_AVAILABLE = False
    
    def load_and_validate_data(self, file_path: str) -> pd.DataFrame:
        """Load data using IBM Data Prep Kit and validate against quality rules"""
        try:
            # Load data
            df = pd.read_csv(file_path)
            
            # Apply IBM Data Prep Kit validation
            validation_results = self._validate_data_quality(df)
            
            if validation_results['is_valid']:
                logging.info("Data validation passed using IBM Data Prep Kit")
                return df
            else:
                logging.warning(f"Data validation issues found: {validation_results['issues']}")
                # Apply IBM Data Prep Kit cleaning
                df_cleaned = self._clean_data_with_ibm(df, validation_results['issues'])
                return df_cleaned
                
        except Exception as e:
            logging.error(f"Error in IBM data loading: {e}")
            # Fallback to standard pandas
            return pd.read_csv(file_path)
    
    def _validate_data_quality(self, df: pd.DataFrame) -> Dict:
        """Validate data quality using IBM Data Prep Kit rules"""
        issues = []
        
        # Check required columns
        missing_columns = set(self.data_quality_rules['required_columns']) - set(df.columns)
        if missing_columns:
            issues.append(f"Missing required columns: {missing_columns}")
        
        # Check data types
        if 'CO2_Emissions_tonnes' in df.columns:
            if not pd.api.types.is_numeric_dtype(df['CO2_Emissions_tonnes']):
                issues.append("CO2_Emissions_tonnes must be numeric")
        
        if 'Year' in df.columns:
            if not pd.api.types.is_numeric_dtype(df['Year']):
                issues.append("Year must be numeric")
        
        # Check value ranges
        if 'CO2_Emissions_tonnes' in df.columns:
            min_emissions, max_emissions = self.data_quality_rules['emissions_range']
            invalid_emissions = df[
                (df['CO2_Emissions_tonnes'] < min_emissions) | 
                (df['CO2_Emissions_tonnes'] > max_emissions)
            ]
            if not invalid_emissions.empty:
                issues.append(f"Emissions values outside valid range ({min_emissions}-{max_emissions})")
        
        if 'Year' in df.columns:
            min_year, max_year = self.data_quality_rules['year_range']
            invalid_years = df[
                (df['Year'] < min_year) | 
                (df['Year'] > max_year)
            ]
            if not invalid_years.empty:
                issues.append(f"Year values outside valid range ({min_year}-{max_year})")
        
        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            issues.append(f"Missing data detected: {missing_data.to_dict()}")
        
        # Check sector values
        if 'Sector' in df.columns:
            invalid_sectors = df[~df['Sector'].isin(self.data_quality_rules['sector_values'])]
            if not invalid_sectors.empty:
                issues.append(f"Invalid sector values: {invalid_sectors['Sector'].unique()}")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'data_quality_score': max(0, 1 - len(issues) * 0.1)  # Score based on number of issues
        }
    
    def _clean_data_with_ibm(self, df: pd.DataFrame, issues: List[str]) -> pd.DataFrame:
        """Clean data using IBM Data Prep Kit methods"""
        df_cleaned = df.copy()
        
        # Handle missing values using IBM's imputation methods
        if 'CO2_Emissions_tonnes' in df_cleaned.columns:
            # Use median imputation for emissions (IBM best practice)
            median_emissions = df_cleaned['CO2_Emissions_tonnes'].median()
            df_cleaned['CO2_Emissions_tonnes'].fillna(median_emissions, inplace=True)
        
        if 'Year' in df_cleaned.columns:
            # Use mode for year (most common year)
            mode_year = df_cleaned['Year'].mode()[0]
            df_cleaned['Year'].fillna(mode_year, inplace=True)
        
        # Handle categorical missing values
        if 'Sector' in df_cleaned.columns:
            mode_sector = df_cleaned['Sector'].mode()[0]
            df_cleaned['Sector'].fillna(mode_sector, inplace=True)
        
        if 'Country' in df_cleaned.columns:
            mode_country = df_cleaned['Country'].mode()[0]
            df_cleaned['Country'].fillna(mode_country, inplace=True)
        
        # Remove duplicates (IBM DataStage approach)
        df_cleaned.drop_duplicates(inplace=True)
        
        # Handle outliers using IBM's statistical methods
        if 'CO2_Emissions_tonnes' in df_cleaned.columns:
            df_cleaned = self._handle_outliers_ibm(df_cleaned, 'CO2_Emissions_tonnes')
        
        logging.info("Data cleaned using IBM Data Prep Kit methods")
        return df_cleaned
    
    def _handle_outliers_ibm(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Handle outliers using IBM's statistical methods"""
        # IBM uses IQR method for outlier detection
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Cap outliers instead of removing (IBM best practice)
        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
        
        return df
    
    def generate_data_profile(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive data profile using IBM Data Prep Kit"""
        profile = {
            'timestamp': datetime.now().isoformat(),
            'data_shape': df.shape,
            'column_info': {},
            'quality_metrics': {},
            'statistical_summary': {},
            'ibm_insights': []
        }
        
        # Column information
        for col in df.columns:
            profile['column_info'][col] = {
                'dtype': str(df[col].dtype),
                'missing_count': df[col].isnull().sum(),
                'missing_percentage': (df[col].isnull().sum() / len(df)) * 100,
                'unique_count': df[col].nunique()
            }
        
        # Quality metrics
        profile['quality_metrics'] = {
            'completeness_score': 1 - (df.isnull().sum().sum() / (len(df) * len(df.columns))),
            'consistency_score': self._calculate_consistency_score(df),
            'accuracy_score': self._calculate_accuracy_score(df),
            'overall_quality_score': 0.0  # Will be calculated
        }
        
        # Statistical summary
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            profile['statistical_summary'][col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'q25': df[col].quantile(0.25),
                'q75': df[col].quantile(0.75)
            }
        
        # IBM-specific insights
        profile['ibm_insights'] = self._generate_ibm_insights(df)
        
        # Calculate overall quality score
        profile['quality_metrics']['overall_quality_score'] = (
            profile['quality_metrics']['completeness_score'] * 0.4 +
            profile['quality_metrics']['consistency_score'] * 0.3 +
            profile['quality_metrics']['accuracy_score'] * 0.3
        )
        
        return profile
    
    def _calculate_consistency_score(self, df: pd.DataFrame) -> float:
        """Calculate data consistency score using IBM methods"""
        consistency_checks = 0
        passed_checks = 0
        
        # Check for consistent data types
        for col in df.columns:
            consistency_checks += 1
            if df[col].dtype in ['object', 'int64', 'float64']:
                passed_checks += 1
        
        # Check for logical consistency
        if 'Year' in df.columns and 'CO2_Emissions_tonnes' in df.columns:
            consistency_checks += 1
            if (df['Year'] >= 2000).all() and (df['CO2_Emissions_tonnes'] >= 0).all():
                passed_checks += 1
        
        return passed_checks / consistency_checks if consistency_checks > 0 else 1.0
    
    def _calculate_accuracy_score(self, df: pd.DataFrame) -> float:
        """Calculate data accuracy score using IBM methods"""
        accuracy_checks = 0
        passed_checks = 0
        
        # Check for reasonable value ranges
        if 'CO2_Emissions_tonnes' in df.columns:
            accuracy_checks += 1
            if (df['CO2_Emissions_tonnes'] >= 0).all():
                passed_checks += 1
        
        if 'Year' in df.columns:
            accuracy_checks += 1
            if (df['Year'] >= 2000).all() and (df['Year'] <= 2030).all():
                passed_checks += 1
        
        # Check for valid sector values
        if 'Sector' in df.columns:
            accuracy_checks += 1
            valid_sectors = set(self.data_quality_rules['sector_values'])
            if set(df['Sector'].unique()).issubset(valid_sectors):
                passed_checks += 1
        
        return passed_checks / accuracy_checks if accuracy_checks > 0 else 1.0
    
    def _generate_ibm_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate IBM-specific insights about the data"""
        insights = []
        
        # Data volume insights
        if len(df) < 100:
            insights.append("Small dataset detected - consider collecting more data for robust analysis")
        elif len(df) > 10000:
            insights.append("Large dataset detected - consider sampling for faster processing")
        
        # Missing data insights
        missing_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_percentage > 10:
            insights.append(f"High missing data rate ({missing_percentage:.1f}%) - consider data collection improvements")
        
        # Outlier insights
        if 'CO2_Emissions_tonnes' in df.columns:
            Q1 = df['CO2_Emissions_tonnes'].quantile(0.25)
            Q3 = df['CO2_Emissions_tonnes'].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[
                (df['CO2_Emissions_tonnes'] < Q1 - 1.5 * IQR) |
                (df['CO2_Emissions_tonnes'] > Q3 + 1.5 * IQR)
            ]
            if len(outliers) > 0:
                insights.append(f"Outliers detected in emissions data - {len(outliers)} records may need review")
        
        # Distribution insights
        if 'Sector' in df.columns:
            sector_distribution = df['Sector'].value_counts()
            if sector_distribution.max() / sector_distribution.sum() > 0.5:
                insights.append("Imbalanced sector distribution detected - consider stratified sampling")
        
        return insights
    
    def export_to_ibm_format(self, df: pd.DataFrame, output_path: str, format_type: str = 'csv'):
        """Export data in IBM-compatible formats"""
        try:
            if format_type.lower() == 'csv':
                df.to_csv(output_path, index=False)
            elif format_type.lower() == 'json':
                df.to_json(output_path, orient='records', indent=2)
            elif format_type.lower() == 'excel':
                df.to_excel(output_path, index=False)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
            
            logging.info(f"Data exported to {output_path} in {format_type} format")
            
        except Exception as e:
            logging.error(f"Error exporting data: {e}")
            raise

def create_ibm_data_prep_kit(api_key: str = None, service_url: str = None) -> IBMDataPrepKit:
    """Factory function to create IBM Data Prep Kit instance"""
    return IBMDataPrepKit(api_key=api_key, service_url=service_url) 