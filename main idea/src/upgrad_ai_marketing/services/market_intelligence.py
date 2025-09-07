"""
Market Intelligence Engine for upGrad AI Marketing Automation
Processes real hiring data and provides market insights
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketIntelligenceEngine:
    """
    Processes comprehensive hiring data to provide market intelligence
    for AI-powered marketing campaign generation
    """
    
    def __init__(self, data_path: str = None):
        # Use proper data directory path
        if data_path is None:
            self.data_path = Path(__file__).parent.parent.parent.parent / "data" / "raw"
        else:
            self.data_path = Path(data_path)
        self.hiring_df = None
        self.campaign_df = None
        self.processed_data = {}
        self.load_data()
    
    def load_data(self):
        """Load and preprocess all data sources"""
        try:
            # Load hiring data
            hiring_file = self.data_path / "company_hiring_data.xlsx"
            self.hiring_df = pd.read_excel(hiring_file)
            logger.info(f"Loaded hiring data: {self.hiring_df.shape[0]} companies")

            # Load marketing automation data
            marketing_file = self.data_path / "marketing_automation_data.xlsx"
            self.campaign_df = pd.read_excel(marketing_file, sheet_name="Campaign_Performance")
            logger.info(f"Loaded campaign data: {self.campaign_df.shape[0]} campaigns")
            
            # Preprocess data
            self._preprocess_data()
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            # Create dummy data for development
            self._create_dummy_data()
    
    def _preprocess_data(self):
        """Clean and preprocess the loaded data"""
        # Clean hiring data
        if self.hiring_df is not None:
            # Convert positions_available to numeric
            self.hiring_df['positions_available'] = pd.to_numeric(
                self.hiring_df['positions_available'], errors='coerce'
            ).fillna(0)
            
            # Clean city names
            self.hiring_df['city'] = self.hiring_df['city'].str.strip().str.title()
            
            # Process skills data
            self.hiring_df['skills_list'] = self.hiring_df['skills_technologies'].apply(
                self._parse_skills
            )
        
        logger.info("Data preprocessing completed")
    
    def _parse_skills(self, skills_str) -> List[str]:
        """Parse skills from string format"""
        if pd.isna(skills_str):
            return []
        
        skills = str(skills_str).split(',')
        return [skill.strip().title() for skill in skills if skill.strip()]
    
    def _create_dummy_data(self):
        """Create dummy data for development when real data is not available"""
        logger.warning("Creating dummy data for development")
        
        cities = ["Bangalore", "Mumbai", "Delhi NCR", "Hyderabad", "Chennai", "Pune"]
        industries = ["IT Services", "Fintech", "E-commerce", "Healthcare", "Manufacturing"]
        skills = ["AI/ML", "Data Science", "Python", "DevOps", "Cloud Computing", "Cybersecurity"]
        
        # Create dummy hiring data
        dummy_hiring = []
        for i in range(100):
            dummy_hiring.append({
                'company_name': f'Company_{i}',
                'city': np.random.choice(cities),
                'industry': np.random.choice(industries),
                'positions_available': np.random.randint(1, 100),
                'skills_technologies': ', '.join(np.random.choice(skills, size=3)),
                'salary_range': f"₹{np.random.randint(8, 25)}-{np.random.randint(25, 40)} LPA",
                'hiring_urgency': np.random.choice(['Low', 'Medium', 'High', 'Critical'])
            })
        
        self.hiring_df = pd.DataFrame(dummy_hiring)
        self.hiring_df['skills_list'] = self.hiring_df['skills_technologies'].apply(self._parse_skills)
    
    def get_city_insights(self, city: str) -> Dict[str, Any]:
        """Get detailed insights for a specific city"""
        if self.hiring_df is None:
            return {"error": "No data available"}
        
        city_data = self.hiring_df[self.hiring_df['city'].str.contains(city, case=False, na=False)]
        
        if city_data.empty:
            return {"error": f"No data found for city: {city}"}
        
        # Calculate insights
        total_positions = city_data['positions_available'].sum()
        companies_hiring = len(city_data)
        
        # Get top skills
        all_skills = []
        for skills_list in city_data['skills_list']:
            all_skills.extend(skills_list)
        
        skill_counts = Counter(all_skills)
        top_skills = dict(skill_counts.most_common(10))
        
        # Get salary insights
        salary_ranges = city_data['salary_range'].dropna().tolist()
        
        # Get hiring urgency distribution
        urgency_dist = city_data['hiring_urgency'].value_counts().to_dict() if 'hiring_urgency' in city_data.columns else {}
        
        # Get industry distribution
        industry_dist = city_data['industry'].value_counts().to_dict() if 'industry' in city_data.columns else {}
        
        return {
            "city": city,
            "total_positions": int(total_positions),
            "companies_hiring": companies_hiring,
            "top_skills": top_skills,
            "salary_ranges": salary_ranges[:5],  # Top 5 salary ranges
            "hiring_urgency": urgency_dist,
            "industries": industry_dist,
            "market_score": min(total_positions / 100, 10),  # Scale to 10
            "last_updated": datetime.now().isoformat()
        }
    
    def get_skill_demand(self) -> Dict[str, int]:
        """Get overall skill demand across all cities"""
        if self.hiring_df is None:
            return {}
        
        all_skills = []
        for skills_list in self.hiring_df['skills_list']:
            all_skills.extend(skills_list)
        
        skill_counts = Counter(all_skills)
        return dict(skill_counts.most_common(20))
    
    def get_course_relevance(self, course: str) -> Dict[str, Any]:
        """Analyze market relevance for upGrad courses"""
        course_mapping = {
            'AI/ML': ['AI/ML', 'Machine Learning', 'Artificial Intelligence', 'Data Science', 'Python'],
            'Generative AI': ['AI/ML', 'Machine Learning', 'Python', 'Deep Learning'],
            'Data Science': ['Data Science', 'Python', 'Analytics', 'Statistics', 'R'],
            'MSc Finance': ['Finance', 'FinTech', 'Banking', 'Investment', 'Risk Management']
        }
        
        relevant_skills = course_mapping.get(course, [])
        skill_demand = self.get_skill_demand()
        
        total_demand = sum(skill_demand.get(skill, 0) for skill in relevant_skills)
        
        return {
            "course": course,
            "relevant_positions": total_demand,
            "demand_skills": {skill: skill_demand.get(skill, 0) for skill in relevant_skills},
            "market_score": min(total_demand / 50, 10),  # Scale to 10
            "growth_potential": "High" if total_demand > 100 else "Medium" if total_demand > 50 else "Low"
        }
    
    def get_hiring_trends(self) -> Dict[str, Any]:
        """Get overall hiring trends and market intelligence"""
        if self.hiring_df is None:
            return {}
        
        # City-wise analysis
        city_stats = self.hiring_df.groupby('city').agg({
            'positions_available': 'sum',
            'company_name': 'count'
        }).rename(columns={'company_name': 'companies_hiring'})
        
        city_performance = {}
        for city, stats in city_stats.iterrows():
            city_performance[city] = {
                'positions_available': int(stats['positions_available']),
                'companies_hiring': int(stats['companies_hiring']),
                'avg_positions_per_company': round(stats['positions_available'] / stats['companies_hiring'], 1)
            }
        
        # Industry analysis
        industry_stats = self.hiring_df.groupby('industry')['positions_available'].sum().to_dict() if 'industry' in self.hiring_df.columns else {}
        
        # Urgency analysis
        urgency_stats = self.hiring_df['hiring_urgency'].value_counts().to_dict() if 'hiring_urgency' in self.hiring_df.columns else {}
        
        return {
            "city_performance": city_performance,
            "industry_demand": industry_stats,
            "hiring_urgency": urgency_stats,
            "total_positions": int(self.hiring_df['positions_available'].sum()),
            "total_companies": len(self.hiring_df),
            "skill_demand": self.get_skill_demand(),
            "last_updated": datetime.now().isoformat()
        }
    
    def get_market_context(self, city: str, course: str = None) -> Dict[str, Any]:
        """Get comprehensive market context for campaign generation"""
        city_insights = self.get_city_insights(city)
        course_relevance = self.get_course_relevance(course) if course else {}
        
        # Generate market context summary
        context = {
            "city_data": city_insights,
            "course_relevance": course_relevance,
            "market_summary": self._generate_market_summary(city_insights, course_relevance),
            "campaign_hooks": self._generate_campaign_hooks(city_insights, course_relevance)
        }
        
        return context
    
    def _generate_market_summary(self, city_data: Dict, course_data: Dict) -> str:
        """Generate a market summary for AI content generation"""
        if city_data.get('error'):
            return "Market data not available for this location."
        
        city = city_data.get('city', 'Unknown')
        positions = city_data.get('total_positions', 0)
        companies = city_data.get('companies_hiring', 0)
        
        summary = f"{city} has {positions} open positions across {companies} companies. "
        
        if city_data.get('top_skills'):
            top_skill = list(city_data['top_skills'].keys())[0]
            summary += f"Top skill in demand: {top_skill}. "
        
        if course_data.get('growth_potential'):
            summary += f"Growth potential for this course: {course_data['growth_potential']}."
        
        return summary
    
    def _generate_campaign_hooks(self, city_data: Dict, course_data: Dict) -> List[str]:
        """Generate campaign hooks based on market data"""
        hooks = []
        
        if not city_data.get('error'):
            positions = city_data.get('total_positions', 0)
            if positions > 1000:
                hooks.append(f"Over {positions} job opportunities available")
            
            if city_data.get('hiring_urgency', {}).get('Critical', 0) > 0:
                hooks.append("Companies hiring urgently")
            
            if city_data.get('top_skills'):
                top_skill = list(city_data['top_skills'].keys())[0]
                hooks.append(f"{top_skill} professionals in high demand")
        
        if course_data.get('growth_potential') == 'High':
            hooks.append("High growth potential in this field")
        
        return hooks[:3]  # Return top 3 hooks

# Global instance
market_intelligence = MarketIntelligenceEngine()
