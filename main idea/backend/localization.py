"""
Geographic Localization Engine for upGrad AI Marketing Automation
Adapts content for Indian Tier-1 cities with cultural context
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalizationEngine:
    """
    Provides city-specific content localization for Indian markets
    Incorporates cultural context, local events, and regional preferences
    """
    
    def __init__(self):
        self.city_contexts = self._load_city_contexts()
        self.regional_languages = self._load_regional_languages()
        self.local_events = self._load_local_events()
        self.cultural_adaptations = self._load_cultural_adaptations()
    
    def _load_city_contexts(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive city context data"""
        return {
            "Bangalore": {
                "nickname": "Silicon Valley of India",
                "key_industries": ["IT Services", "Startups", "R&D", "Biotechnology"],
                "cultural_tone": "Tech-forward, innovation-focused, cosmopolitan",
                "local_events": ["Bangalore Tech Summit", "Global Innovation Summit", "India Mobile Congress"],
                "language_preference": "English with tech jargon",
                "market_sentiment": "High competition, growth-oriented, startup culture",
                "salary_expectations": "High (₹12-36 LPA)",
                "work_culture": "Fast-paced, flexible, innovation-driven",
                "key_companies": ["Infosys", "Wipro", "TCS", "Flipkart", "Ola"],
                "hashtags": ["#BangaloreTech", "#SiliconValleyOfIndia", "#NammaOoru"],
                "local_references": ["Namma Metro", "UB City", "Electronic City", "Whitefield"]
            },
            "Mumbai": {
                "nickname": "Financial Capital of India",
                "key_industries": ["Finance", "Media", "Entertainment", "Pharmaceuticals"],
                "cultural_tone": "Fast-paced, opportunity-driven, commercial",
                "local_events": ["Mumbai Fintech Festival", "Digital Marketing Summit", "Bombay Stock Exchange Events"],
                "language_preference": "English/Hindi mix, business-focused",
                "market_sentiment": "Networking-focused, premium positioning, ambitious",
                "salary_expectations": "Premium (₹10-22 LPA)",
                "work_culture": "Hustle mentality, networking-heavy, results-oriented",
                "key_companies": ["Reliance", "Tata Group", "HDFC", "Kotak Mahindra"],
                "hashtags": ["#MumbaiFinance", "#MaxCity", "#BombayDreams"],
                "local_references": ["Nariman Point", "BKC", "Marine Drive", "Local trains"]
            },
            "Delhi NCR": {
                "nickname": "Corporate Hub of India",
                "key_industries": ["Government", "Consulting", "MNCs", "Manufacturing"],
                "cultural_tone": "Professional, hierarchical, power-conscious",
                "local_events": ["Delhi Business Summit", "India Leadership Conclave", "CII Events"],
                "language_preference": "Hindi/English mix, formal tone",
                "market_sentiment": "Authority-respecting, status-conscious, traditional",
                "salary_expectations": "Competitive (₹11-24 LPA)",
                "work_culture": "Formal, hierarchy-aware, relationship-based",
                "key_companies": ["HCL", "Tech Mahindra", "Maruti Suzuki", "Hero MotoCorp"],
                "hashtags": ["#DelhiNCR", "#CapitalCareers", "#DilliKiDhadak"],
                "local_references": ["Connaught Place", "Gurgaon", "Noida", "Metro"]
            },
            "Hyderabad": {
                "nickname": "Cyberabad",
                "key_industries": ["IT Services", "Biotech", "Aerospace", "Pharmaceuticals"],
                "cultural_tone": "Tech-savvy, cost-conscious, traditional yet modern",
                "local_events": ["Hyderabad Tech Conference", "BioTech Summit", "HITEC City Events"],
                "language_preference": "Telugu/English mix, respectful tone",
                "market_sentiment": "Value-focused, pragmatic, family-oriented",
                "salary_expectations": "Value-driven (₹9-20 LPA)",
                "work_culture": "Balanced, family-friendly, cost-effective",
                "key_companies": ["Microsoft", "Google", "Amazon", "Facebook"],
                "hashtags": ["#Cyberabad", "#HyderabadTech", "#CityOfPearls"],
                "local_references": ["HITEC City", "Gachibowli", "Jubilee Hills", "Charminar"]
            },
            "Chennai": {
                "nickname": "Detroit of India",
                "key_industries": ["Automotive", "Manufacturing", "IT", "Healthcare"],
                "cultural_tone": "Traditional yet progressive, quality-focused",
                "local_events": ["Chennai Auto Expo", "South India Tech Meet", "Manufacturing Summit"],
                "language_preference": "Tamil/English mix, respectful approach",
                "market_sentiment": "Quality-focused, relationship-driven, conservative",
                "salary_expectations": "Steady (₹8-18 LPA)",
                "work_culture": "Methodical, quality-oriented, relationship-based",
                "key_companies": ["TCS", "Cognizant", "Ford", "Hyundai"],
                "hashtags": ["#ChennaiTech", "#DetroitOfIndia", "#TamilNaduTech"],
                "local_references": ["OMR", "Velachery", "T.Nagar", "Marina Beach"]
            },
            "Pune": {
                "nickname": "Oxford of the East",
                "key_industries": ["Education", "IT", "Automotive", "Manufacturing"],
                "cultural_tone": "Academic, youthful, collaborative",
                "local_events": ["Pune Tech Festival", "Education Innovation Summit", "Auto Expo"],
                "language_preference": "Marathi/English mix, academic tone",
                "market_sentiment": "Learning-oriented, collaborative, student-friendly",
                "salary_expectations": "Moderate (₹9-19 LPA)",
                "work_culture": "Academic, collaborative, innovation-friendly",
                "key_companies": ["Infosys", "TCS", "Bajaj", "Mahindra"],
                "hashtags": ["#PuneTech", "#OxfordOfTheEast", "#PuneIT"],
                "local_references": ["Hinjewadi", "Magarpatta", "Koregaon Park", "Deccan"]
            },
            "Ahmedabad": {
                "nickname": "Manchester of India",
                "key_industries": ["Textiles", "Chemicals", "Pharmaceuticals", "IT"],
                "cultural_tone": "Business-minded, entrepreneurial, traditional",
                "local_events": ["Gujarat Business Summit", "Textile Expo", "Pharma Conference"],
                "language_preference": "Gujarati/English mix, business-focused",
                "market_sentiment": "Entrepreneurial, cost-effective, business-oriented",
                "salary_expectations": "Cost-effective (₹7-16 LPA)",
                "work_culture": "Entrepreneurial, family-business oriented, frugal",
                "key_companies": ["Adani Group", "Torrent", "Zydus", "Infibeam"],
                "hashtags": ["#AhmedabadBusiness", "#GujaratTech", "#ManchesterOfIndia"],
                "local_references": ["SG Highway", "Satellite", "Vastrapur", "Sabarmati"]
            },
            "Kolkata": {
                "nickname": "Cultural Capital of India",
                "key_industries": ["IT", "Finance", "Jute", "Steel"],
                "cultural_tone": "Intellectual, cultural, traditional",
                "local_events": ["Kolkata Book Fair", "Bengal IT Summit", "Cultural Festivals"],
                "language_preference": "Bengali/English mix, intellectual tone",
                "market_sentiment": "Intellectual, culture-appreciating, traditional",
                "salary_expectations": "Modest (₹6-15 LPA)",
                "work_culture": "Intellectual, discussion-oriented, culture-rich",
                "key_companies": ["TCS", "Wipro", "ITC", "Coal India"],
                "hashtags": ["#KolkataTech", "#CulturalCapital", "#CityOfJoy"],
                "local_references": ["Salt Lake", "New Town", "Park Street", "Howrah Bridge"]
            }
        }
    
    def _load_regional_languages(self) -> Dict[str, Dict[str, str]]:
        """Load regional language translations for key phrases"""
        return {
            "Bangalore": {
                "hello": "Namaskara",
                "opportunity": "Avakasha",
                "career": "Vyavasaya",
                "success": "Safalate"
            },
            "Mumbai": {
                "hello": "Namaskar",
                "opportunity": "Mauka",
                "career": "Career",
                "success": "Safalta"
            },
            "Delhi NCR": {
                "hello": "Namaste",
                "opportunity": "Mauka",
                "career": "Career",
                "success": "Safalta"
            },
            "Hyderabad": {
                "hello": "Namaste",
                "opportunity": "Avakasam",
                "career": "Udyogam",
                "success": "Vijayam"
            },
            "Chennai": {
                "hello": "Vanakkam",
                "opportunity": "Vaaipu",
                "career": "Thozhil",
                "success": "Vetri"
            },
            "Pune": {
                "hello": "Namaskar",
                "opportunity": "Sandhi",
                "career": "Vyavasaya",
                "success": "Yash"
            }
        }
    
    def _load_local_events(self) -> Dict[str, List[Dict[str, str]]]:
        """Load upcoming local events for each city"""
        return {
            "Bangalore": [
                {"name": "Bangalore Tech Summit", "date": "November 2025", "relevance": "High"},
                {"name": "Global Innovation Summit", "date": "December 2025", "relevance": "Medium"},
                {"name": "India Mobile Congress", "date": "October 2025", "relevance": "High"}
            ],
            "Mumbai": [
                {"name": "Mumbai Fintech Festival", "date": "October 2025", "relevance": "High"},
                {"name": "Digital Marketing Summit", "date": "November 2025", "relevance": "Medium"}
            ],
            "Delhi NCR": [
                {"name": "Delhi Business Summit", "date": "December 2025", "relevance": "High"},
                {"name": "India Leadership Conclave", "date": "January 2026", "relevance": "Medium"}
            ]
        }
    
    def _load_cultural_adaptations(self) -> Dict[str, Dict[str, Any]]:
        """Load cultural adaptation rules"""
        return {
            "formal_cities": ["Delhi NCR", "Mumbai", "Chennai"],
            "tech_cities": ["Bangalore", "Hyderabad", "Pune"],
            "business_cities": ["Mumbai", "Ahmedabad", "Delhi NCR"],
            "youth_cities": ["Pune", "Bangalore", "Hyderabad"],
            "traditional_cities": ["Chennai", "Kolkata", "Ahmedabad"]
        }
    
    def localize_content(self, content: Dict[str, Any], city: str) -> Dict[str, Any]:
        """Apply comprehensive localization to campaign content"""
        
        city_context = self.city_contexts.get(city, {})
        if not city_context:
            logger.warning(f"No localization data for city: {city}")
            return content
        
        localized_content = content.copy()
        
        # Localize email subject
        localized_content['email_subject'] = self._localize_subject(
            content.get('email_subject', ''), city_context
        )
        
        # Localize email body
        localized_content['email_body'] = self._localize_body(
            content.get('email_body', ''), city_context
        )
        
        # Localize social post
        localized_content['social_post'] = self._localize_social(
            content.get('social_post', ''), city_context
        )
        
        # Add regional language version
        localized_content['regional_version'] = self._create_regional_version(
            content, city_context
        )
        
        # Add local context
        localized_content['local_context'] = city_context
        
        return localized_content
    
    def _localize_subject(self, subject: str, context: Dict[str, Any]) -> str:
        """Localize email subject line with city context"""
        
        nickname = context.get('nickname', '')
        city_name = context.get('city', '')
        
        # Add city nickname if not already present
        if nickname and nickname not in subject:
            subject = f"{subject} | {nickname}"
        
        # Add urgency based on market sentiment
        sentiment = context.get('market_sentiment', '')
        if 'high competition' in sentiment.lower():
            subject = subject.replace('!', ' - Act Fast!')
        
        return subject[:60]  # Keep within email subject limits
    
    def _localize_body(self, body: str, context: Dict[str, Any]) -> str:
        """Localize email body with comprehensive city context"""
        
        # Add local industry context
        industries = context.get('key_industries', [])
        if industries:
            industry_text = f"\n\nWith {', '.join(industries[:2])} leading {context.get('nickname', 'the city')}'s growth"
            body += industry_text
        
        # Add local events
        events = self._get_relevant_events(context.get('city', ''))
        if events:
            event_text = f", and upcoming events like {events[0]['name']}"
            body += event_text
        
        # Add local references
        references = context.get('local_references', [])
        if references:
            ref_text = f" in areas like {references[0]}"
            body += ref_text
        
        # Add cultural closing
        work_culture = context.get('work_culture', '')
        if 'family-friendly' in work_culture:
            body += "\n\nJoin thousands of professionals who've transformed their careers while maintaining work-life balance."
        elif 'fast-paced' in work_culture:
            body += "\n\nJoin the fast-track to success with industry-leading curriculum and expert mentorship."
        
        return body
    
    def _localize_social(self, social_post: str, context: Dict[str, Any]) -> str:
        """Localize social media post with city-specific hashtags"""
        
        # Add city-specific hashtags
        hashtags = context.get('hashtags', [])
        if hashtags:
            # Remove existing generic hashtags and add city-specific ones
            social_post = re.sub(r'#\w+', '', social_post).strip()
            social_post += f" {' '.join(hashtags[:3])}"
        
        # Add local references if space allows
        if len(social_post) < 200:  # Leave room for additions
            references = context.get('local_references', [])
            if references:
                social_post += f" #{references[0].replace(' ', '')}"
        
        return social_post[:280]  # Twitter limit
    
    def _create_regional_version(self, content: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Create a regional language version of the campaign"""
        
        city = context.get('city', '')
        regional_lang = self.regional_languages.get(city, {})
        
        if not regional_lang:
            return "Regional version not available for this city."
        
        # Create a simple regional version
        hello = regional_lang.get('hello', 'Hello')
        opportunity = regional_lang.get('opportunity', 'opportunity')
        career = regional_lang.get('career', 'career')
        success = regional_lang.get('success', 'success')
        
        regional_text = f"{hello}! {context.get('nickname', city)} mein {opportunity} hai! "
        regional_text += f"Apna {career} transform karo aur {success} pao upGrad ke saath!"
        
        return regional_text
    
    def _get_relevant_events(self, city: str) -> List[Dict[str, str]]:
        """Get relevant upcoming events for the city"""
        events = self.local_events.get(city, [])
        # Filter for high relevance events
        return [event for event in events if event.get('relevance') == 'High']
    
    def get_localization_recommendations(self, city: str, course: str) -> Dict[str, Any]:
        """Get localization recommendations for a specific city and course"""
        
        context = self.city_contexts.get(city, {})
        if not context:
            return {"error": f"No localization data available for {city}"}
        
        recommendations = {
            "tone_adjustments": self._get_tone_recommendations(context, course),
            "cultural_considerations": self._get_cultural_considerations(context),
            "local_hooks": self._get_local_hooks(context, course),
            "language_preferences": context.get('language_preference', 'English'),
            "optimal_timing": self._get_optimal_timing(context),
            "platform_preferences": self._get_platform_preferences(context)
        }
        
        return recommendations
    
    def _get_tone_recommendations(self, context: Dict[str, Any], course: str) -> List[str]:
        """Get tone recommendations based on city culture"""
        
        cultural_tone = context.get('cultural_tone', '')
        recommendations = []
        
        if 'formal' in cultural_tone or 'hierarchical' in cultural_tone:
            recommendations.append("Use formal, respectful language")
            recommendations.append("Emphasize authority and credentials")
        
        if 'tech-forward' in cultural_tone or 'innovation' in cultural_tone:
            recommendations.append("Use tech terminology and innovation language")
            recommendations.append("Highlight cutting-edge curriculum")
        
        if 'traditional' in cultural_tone:
            recommendations.append("Balance modern content with traditional values")
            recommendations.append("Emphasize family and stability benefits")
        
        return recommendations
    
    def _get_cultural_considerations(self, context: Dict[str, Any]) -> List[str]:
        """Get cultural considerations for the city"""
        
        considerations = []
        work_culture = context.get('work_culture', '')
        
        if 'family-friendly' in work_culture:
            considerations.append("Emphasize work-life balance")
            considerations.append("Mention flexible learning options")
        
        if 'networking' in work_culture:
            considerations.append("Highlight networking opportunities")
            considerations.append("Mention industry connections")
        
        if 'entrepreneurial' in work_culture:
            considerations.append("Focus on business skills and startup opportunities")
            considerations.append("Mention entrepreneurship support")
        
        return considerations
    
    def _get_local_hooks(self, context: Dict[str, Any], course: str) -> List[str]:
        """Generate local hooks for campaigns"""
        
        hooks = []
        nickname = context.get('nickname', '')
        industries = context.get('key_industries', [])
        
        if nickname:
            hooks.append(f"Join {nickname}'s tech revolution")
        
        if industries:
            relevant_industry = self._find_relevant_industry(industries, course)
            if relevant_industry:
                hooks.append(f"{relevant_industry} professionals in high demand")
        
        return hooks
    
    def _find_relevant_industry(self, industries: List[str], course: str) -> Optional[str]:
        """Find the most relevant industry for the course"""
        
        course_industry_map = {
            'AI/ML': ['IT Services', 'Startups', 'R&D'],
            'Data Science': ['IT Services', 'Finance', 'E-commerce'],
            'Generative AI': ['IT Services', 'Media', 'Entertainment'],
            'MSc Finance': ['Finance', 'Banking', 'Fintech']
        }
        
        relevant_industries = course_industry_map.get(course, [])
        
        for industry in industries:
            if any(rel_ind.lower() in industry.lower() for rel_ind in relevant_industries):
                return industry
        
        return industries[0] if industries else None
    
    def _get_optimal_timing(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Get optimal timing recommendations"""
        
        work_culture = context.get('work_culture', '')
        
        if 'fast-paced' in work_culture:
            return {"best_time": "Early morning or late evening", "avoid": "Lunch hours"}
        elif 'traditional' in work_culture:
            return {"best_time": "Business hours", "avoid": "Early morning or late evening"}
        else:
            return {"best_time": "Business hours", "avoid": "Weekends"}
    
    def _get_platform_preferences(self, context: Dict[str, Any]) -> List[str]:
        """Get platform preferences based on city culture"""
        
        cultural_tone = context.get('cultural_tone', '')
        
        if 'tech-forward' in cultural_tone:
            return ["LinkedIn", "Twitter", "Instagram"]
        elif 'traditional' in cultural_tone:
            return ["LinkedIn", "Facebook", "Email"]
        elif 'business' in cultural_tone:
            return ["LinkedIn", "Email", "WhatsApp Business"]
        else:
            return ["LinkedIn", "Facebook", "Instagram"]

# Global instance
localization_engine = LocalizationEngine()
