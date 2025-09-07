"""
AI Content Generation Engine for upGrad Marketing Automation
Integrates with Gemini API for personalized campaign content
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    genai = None
    logging.warning("Google Generative AI not available. Install with: pip install google-generativeai")

import requests
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIContentGenerator:
    """
    AI-powered content generation for marketing campaigns
    Uses Gemini API for contextual content creation
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.stability_api_key = os.getenv('STABILITY_API_KEY')
        self.model = None
        self.brand_guidelines = self._load_brand_guidelines()
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini API"""
        if genai and self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                # Use the correct model name for the current API version
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Gemini API initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing Gemini API: {e}")
                # Try alternative model names
                try:
                    self.model = genai.GenerativeModel('gemini-pro')
                    logger.info("Gemini API initialized with gemini-pro")
                except Exception as e2:
                    logger.error(f"Error with gemini-pro: {e2}")
                    self.model = None
        else:
            logger.warning("Gemini API not available - using fallback content generation")
    
    def _load_brand_guidelines(self) -> Dict[str, Any]:
        """Load upGrad brand guidelines"""
        return {
            "brand_name": "upGrad",
            "colors": {
                "primary": "#007BFF",
                "secondary": "#FFFFFF",
                "accent": "#FF6B35"
            },
            "tone": "professional, motivational, career-focused",
            "target_audience": "working professionals seeking career advancement",
            "key_messages": [
                "Upskill for Success",
                "Transform Your Career",
                "Industry-Relevant Skills",
                "Expert-Led Learning"
            ],
            "content_guidelines": {
                "focus_on_career_growth": True,
                "include_salary_benefits": True,
                "create_urgency": True,
                "reference_market_data": True,
                "maintain_professional_tone": True
            }
        }
    
    async def generate_campaign_content(self, 
                                      course: str, 
                                      city: str, 
                                      campaign_type: str,
                                      market_context: Dict[str, Any],
                                      localization_level: str = "basic") -> Dict[str, Any]:
        """Generate complete campaign content using AI"""
        
        try:
            # Create context-aware prompt
            prompt = self._create_content_prompt(course, city, campaign_type, market_context)
            
            # Generate content using Gemini or fallback
            if self.model:
                content = await self._generate_with_gemini(prompt)
            else:
                content = self._generate_fallback_content(course, city, campaign_type, market_context)
            
            # Parse and structure the content
            structured_content = self._parse_ai_response(content, course, city)
            
            # Add performance predictions
            structured_content['predictions'] = self._predict_performance(
                course, city, campaign_type, market_context
            )
            
            return structured_content
            
        except Exception as e:
            logger.error(f"Error generating campaign content: {e}")
            return self._generate_fallback_content(course, city, campaign_type, market_context)
    
    def _create_content_prompt(self, 
                             course: str, 
                             city: str, 
                             campaign_type: str,
                             market_context: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for AI content generation"""
        
        # Extract market insights
        city_data = market_context.get('city_data', {})
        course_relevance = market_context.get('course_relevance', {})
        market_summary = market_context.get('market_summary', '')
        campaign_hooks = market_context.get('campaign_hooks', [])
        
        prompt = f"""
Create a high-converting marketing campaign for upGrad's {course} course targeting professionals in {city}.

MARKET CONTEXT:
{market_summary}

KEY MARKET INSIGHTS:
- Total positions available: {city_data.get('total_positions', 'N/A')}
- Companies hiring: {city_data.get('companies_hiring', 'N/A')}
- Course market score: {course_relevance.get('market_score', 'N/A')}/10
- Growth potential: {course_relevance.get('growth_potential', 'Medium')}

CAMPAIGN HOOKS TO USE:
{', '.join(campaign_hooks) if campaign_hooks else 'Focus on career advancement'}

BRAND GUIDELINES:
- Brand: upGrad
- Tone: {self.brand_guidelines['tone']}
- Target: {self.brand_guidelines['target_audience']}
- Key Message: {self.brand_guidelines['key_messages'][0]}

GENERATE THE FOLLOWING:

1. EMAIL SUBJECT LINE (max 60 characters):
[Create urgency and include city/course reference]

2. EMAIL BODY (150-200 words):
[Professional tone, include market data, salary benefits, call-to-action]

3. SOCIAL MEDIA POST (280 characters max):
[Engaging, include relevant hashtags, motivational]

4. CALL-TO-ACTION:
[Clear, action-oriented, creates urgency]

5. KEY BENEFITS (3 points):
[Career growth, salary increase, market relevance]

FORMAT YOUR RESPONSE AS:
SUBJECT: [subject line]
BODY: [email body]
SOCIAL: [social media post]
CTA: [call to action]
BENEFITS: [benefit 1] | [benefit 2] | [benefit 3]

Current date: {datetime.now().strftime('%B %Y')}
Campaign type: {campaign_type}
"""
        
        return prompt
    
    async def _generate_with_gemini(self, prompt: str) -> str:
        """Generate content using Gemini API"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def _generate_fallback_content(self, 
                                 course: str, 
                                 city: str, 
                                 campaign_type: str,
                                 market_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback content when AI is not available"""
        
        city_data = market_context.get('city_data', {})
        positions = city_data.get('total_positions', 1000)
        companies = city_data.get('companies_hiring', 50)
        
        # Template-based content generation
        templates = {
            'AI/ML': {
                'subject': f"{city}'s AI Boom: {positions}+ Jobs - Upskill Now!",
                'body': f"Hey [Name], {city} is experiencing unprecedented AI/ML growth with {positions}+ positions across {companies}+ companies. Join upGrad's comprehensive {course} program and ride the wave of AI transformation. Industry experts, hands-on projects, and guaranteed career support. Limited seats - enroll today!",
                'social': f"🚀 {city} AI revolution is HERE! {positions}+ jobs, {companies}+ companies hiring. Ready to level up? #upGrad #AIJobs #{city.replace(' ', '')}Tech",
                'cta': "Enroll in AI/ML Program - Limited Seats!"
            },
            'Data Science': {
                'subject': f"{city} Data Gold Rush: {positions}+ Opportunities!",
                'body': f"[Name], {city}'s data landscape is exploding with {positions}+ opportunities across {companies}+ companies! Master Data Science with upGrad's industry-aligned program. Real projects, expert mentorship, and career transformation guaranteed. Your data-driven future starts now!",
                'social': f"📊 {city} needs data wizards! {positions}+ positions, {companies}+ companies. Become the data hero! #DataScience #upGrad #{city.replace(' ', '')}",
                'cta': "Start Your Data Science Journey Today!"
            },
            'Generative AI': {
                'subject': f"{city} GenAI Boom: Create Your Future Today!",
                'body': f"Ready to shape the future, [Name]? {city}'s GenAI sector is booming with {positions}+ opportunities! Master Generative AI with upGrad and unlock unlimited potential. From ChatGPT to image generation - learn it all. Transform your career in the AI revolution!",
                'social': f"✨ GenAI is transforming {city}! Create, innovate, earn big. Join the revolution! #GenerativeAI #upGrad #{city.replace(' ', '')}",
                'cta': "Master Generative AI - Enroll Now!"
            }
        }
        
        template = templates.get(course, templates['AI/ML'])
        
        return {
            'email_subject': template['subject'],
            'email_body': template['body'],
            'social_post': template['social'],
            'call_to_action': template['cta'],
            'key_benefits': [
                f"Access to {positions}+ job opportunities",
                "Industry-expert led curriculum",
                "Guaranteed career support"
            ]
        }
    
    def _parse_ai_response(self, ai_response: str, course: str, city: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        
        try:
            # Extract components using regex
            subject_match = re.search(r'SUBJECT:\s*(.+)', ai_response, re.IGNORECASE)
            body_match = re.search(r'BODY:\s*(.+?)(?=SOCIAL:|$)', ai_response, re.IGNORECASE | re.DOTALL)
            social_match = re.search(r'SOCIAL:\s*(.+?)(?=CTA:|$)', ai_response, re.IGNORECASE)
            cta_match = re.search(r'CTA:\s*(.+?)(?=BENEFITS:|$)', ai_response, re.IGNORECASE)
            benefits_match = re.search(r'BENEFITS:\s*(.+)', ai_response, re.IGNORECASE)
            
            # Extract and clean content
            email_subject = subject_match.group(1).strip() if subject_match else f"{city} {course} Opportunity - Transform Your Career!"
            email_body = body_match.group(1).strip() if body_match else f"Exciting {course} opportunities in {city}. Join upGrad today!"
            social_post = social_match.group(1).strip() if social_match else f"🚀 {course} opportunities in {city}! #upGrad"
            call_to_action = cta_match.group(1).strip() if cta_match else "Enroll Now - Limited Seats!"
            
            # Parse benefits
            benefits = []
            if benefits_match:
                benefits_text = benefits_match.group(1).strip()
                benefits = [b.strip() for b in benefits_text.split('|')]
            else:
                benefits = ["Career advancement", "Salary increase", "Industry recognition"]
            
            return {
                'email_subject': email_subject[:60],  # Limit to 60 chars
                'email_body': email_body,
                'social_post': social_post[:280],  # Twitter limit
                'call_to_action': call_to_action,
                'key_benefits': benefits[:3]  # Top 3 benefits
            }
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            # Return fallback content
            return self._generate_fallback_content(course, city, "Email", {})
    
    def _predict_performance(self, 
                           course: str, 
                           city: str, 
                           campaign_type: str,
                           market_context: Dict[str, Any]) -> Dict[str, str]:
        """Predict campaign performance based on market context"""
        
        # Base performance metrics
        base_ctr = 0.12
        base_conversion = 0.05
        base_roas = 3.2
        base_cost = 300
        
        # Course multipliers
        course_multipliers = {
            'AI/ML': {'ctr': 1.4, 'conversion': 1.3, 'roas': 1.3, 'cost': 0.8},
            'Generative AI': {'ctr': 1.2, 'conversion': 1.1, 'roas': 1.1, 'cost': 0.9},
            'Data Science': {'ctr': 1.1, 'conversion': 1.0, 'roas': 1.0, 'cost': 1.0},
            'MSc Finance': {'ctr': 0.9, 'conversion': 0.9, 'roas': 0.9, 'cost': 1.1}
        }
        
        # Get course multiplier
        multiplier = course_multipliers.get(course, course_multipliers['Data Science'])
        
        # Apply market context boost
        city_data = market_context.get('city_data', {})
        market_score = city_data.get('market_score', 5)
        market_boost = 1 + (market_score / 20)  # 5% boost per market score point
        
        # Calculate final metrics
        final_ctr = base_ctr * multiplier['ctr'] * market_boost
        final_conversion = base_conversion * multiplier['conversion'] * market_boost
        final_roas = base_roas * multiplier['roas'] * market_boost
        final_cost = base_cost * multiplier['cost'] / market_boost
        
        return {
            'ctr': f"{final_ctr * 100:.1f}%",
            'conversion_rate': f"{final_conversion * 100:.1f}%",
            'roas': f"{final_roas:.1f}x",
            'cost_per_conversion': f"₹{int(final_cost)}"
        }
    
    async def generate_image_prompt(self, content_context: Dict[str, Any]) -> str:
        """Generate image prompt for Stable Diffusion"""
        
        course = content_context.get('course', 'Professional Development')
        city = content_context.get('city', 'India')
        theme = content_context.get('theme', 'Career Growth')
        
        prompt = f"""
Professional marketing poster for upGrad education platform.
Theme: {theme} in {course}
Setting: Modern office environment in {city}, India
People: Diverse Indian professionals, confident and successful
Colors: Primary blue (#007BFF) and orange (#FF6B35) accents
Style: Clean, modern, motivational, high-quality
Text overlay: "upGrad" logo prominently displayed
Background: Subtle tech/data visualization elements
Mood: Inspiring, professional, aspirational
Quality: High resolution, marketing-ready, professional photography style
"""
        
        return prompt

# Global instance
ai_content_generator = AIContentGenerator()
