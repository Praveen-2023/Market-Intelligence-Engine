# 🚀 upGrad AI Marketing Automation Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![AI Powered](https://img.shields.io/badge/AI-Gemini%20%2B%20Stability-orange.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Revolutionary AI-powered marketing automation platform with regional language intelligence for the Indian EdTech market**

## 🌟 Overview

The upGrad AI Marketing Automation Platform is a comprehensive solution that transforms how EdTech companies create and deploy marketing campaigns. Built with cutting-edge AI technology, it delivers personalized, culturally-relevant content across multiple channels while integrating real-time market intelligence.

### ✨ Key Highlights
- **🤖 Dual AI Integration**: Gemini AI for content + Stability AI for images
- **🌍 Regional Intelligence**: 8 Indian cities with local language adaptation
- **📱 Multi-Channel**: Email, Social Media, SMS/WhatsApp, Images
- **📊 Real Market Data**: 472+ companies, 46,336+ job positions
- **🎨 Modern UI**: Glass morphism design with animated gradients

## 🎯 Features

### 🤖 AI-Powered Content Generation
- **Smart Content Creation**: Generate unique marketing copy in 2-3 minutes
- **Multi-Variant Support**: Create multiple campaign approaches automatically
- **Tone Scaling**: Adjust from professional (1) to urgent/FOMO (10)
- **Platform Optimization**: Content tailored for LinkedIn, Instagram, Facebook, Twitter

### 🌍 Regional Language Intelligence
- **Bangalore**: Kannada elements (Namaskara, ಭವಿಷ್ಯ, ಕೆಲಸ, Dhanyawadagalu)
- **Hyderabad**: Telugu elements (Namaste, భవిష్యత్తు, పని, Dhanyawadamulu)
- **Mumbai**: Hindi elements (Namaste, काम, सफलता, Dhanyawad)
- **Chennai**: Tamil elements (Vanakkam, வேலை, எதிர்காலம், Nandri)
- **Delhi NCR**: Hindi elements (Namaste, नौकरी, कैरियर, Dhanyawad)
- **Pune**: Marathi elements (Namaskar, काम, यश, Dhanyawad)
- **Kolkata**: Bengali elements (Namaskar, কাজ, ভবিষ্যৎ, Dhonnobad)
- **Ahmedabad**: Gujarati elements (Namaste, કામ, સફળતા, Dhanyawad)

### 📊 Real-Time Market Intelligence
- **Live Job Data**: 46,336+ positions across major Indian cities
- **Company Insights**: 472+ companies actively hiring
- **Salary Analytics**: Real-time salary ranges (₹6-36 LPA)
- **Market Trends**: Growth rates and hiring patterns

### 🎨 Custom Image Generation
- **AI-Generated Banners**: Professional marketing visuals with Stability AI
- **Multiple Styles**: Professional, Modern, Creative, Minimal
- **Custom Prompts**: Describe exactly what you want
- **Various Formats**: Square, Landscape, Portrait, Social Media sizes

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- API Keys (Gemini AI + Stability AI)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Praveen-2023/Market-Intelligence-Engine.git
cd Market-Intelligence-Engine/main\ idea
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API keys**
```bash
# Edit config/.env file
GEMINI_API_KEY=your_gemini_api_key_here
STABILITY_API_KEY=your_stability_api_key_here
```

4. **Run the application**
```bash
python simple_server.py
```

5. **Access the dashboard**
- **Dashboard**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📱 Usage

### Content Generation
1. **Select Cities**: Choose target cities (Bangalore, Mumbai, Delhi, etc.)
2. **Choose Content Type**: Email, Social Media, SMS/WhatsApp, or Images
3. **Configure Parameters**: Course, tone scale, language preferences
4. **Generate**: Get AI-powered, regionally-adapted content in seconds

### Regional Adaptation
The platform automatically adapts content based on selected cities:
- **Greetings**: Local language greetings (Namaskara, Vanakkam, etc.)
- **Cultural Context**: City-specific references (Silicon Valley of India, Cyberabad)
- **Language Elements**: Native script integration where appropriate
- **Market Data**: City-specific job statistics and salary ranges

## 🏗️ Architecture

### Core Components
- **FastAPI Backend**: High-performance async API server
- **AI Engines**: Gemini AI (content) + Stability AI (images)
- **Data Layer**: Excel-based market intelligence with real-time processing
- **Frontend**: Modern glass morphism UI with responsive design

### API Endpoints
- `GET /` - Main dashboard
- `POST /api/generate-campaign` - Content generation
- `POST /api/generate-image` - Image generation
- `GET /api/market-intelligence` - Market data
- `GET /api/health` - System status

## 📊 Market Intelligence

### Real Data Integration
- **Companies**: 472 companies across India
- **Positions**: 46,336+ job openings
- **Cities**: 8 major Indian markets
- **Salary Ranges**: ₹6-36 LPA across different roles
- **Growth Rate**: +15% YoY market expansion

### Sample Market Data
```json
{
  "Bangalore": {
    "positions_available": 6195,
    "companies_hiring": 44,
    "avg_salary": "₹12-36 LPA",
    "growth_rate": "+15% YoY"
  },
  "Mumbai": {
    "positions_available": 3801,
    "companies_hiring": 32,
    "avg_salary": "₹16-21 LPA",
    "growth_rate": "+15% YoY"
  }
}
```

## 🎨 UI/UX Features

### Modern Design
- **Glass Morphism**: Frosted glass panels with backdrop blur
- **Animated Gradients**: 5-color shifting background
- **Professional Typography**: Poppins + Inter font families
- **Responsive Layout**: 3-panel dashboard design
- **Interactive Elements**: Hover effects and smooth transitions

### Content Type Tabs
- **📧 Email Campaigns**: Subject lines + body content
- **📱 Social Media**: Platform-optimized posts
- **🎨 Image Generation**: Custom AI-generated visuals
- **💬 SMS/WhatsApp**: Character-limited messaging

## 🔧 Configuration

### Environment Variables
```env
# API Keys
GEMINI_API_KEY=your_gemini_key
STABILITY_API_KEY=your_stability_key

# Settings
DEBUG=True
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=2000
DEFAULT_LANGUAGE=en
```

### Supported Cities
- Bangalore, Mumbai, Delhi NCR, Hyderabad
- Chennai, Pune, Ahmedabad, Kolkata

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for advanced content generation
- **Stability AI** for professional image creation
- **FastAPI** for the robust backend framework
- **Indian EdTech Community** for market insights and feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Praveen-2023/Market-Intelligence-Engine/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Praveen-2023/Market-Intelligence-Engine/discussions)
- **Email**: support@upgrad-ai-marketing.com

---

**Built with ❤️ for the Indian EdTech ecosystem**

*Transforming marketing automation with AI and regional intelligence*
