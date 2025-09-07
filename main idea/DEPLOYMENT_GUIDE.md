# upGrad AI Marketing Automation - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16+ (optional, for advanced frontend features)
- 4GB RAM minimum
- Internet connection for AI APIs

### 1. Install Dependencies
```bash
cd "main idea"
pip install -r requirements.txt
```

### 2. Environment Setup (Optional)
Create a `.env` file for API keys:
```bash
# Optional: For enhanced AI features
GEMINI_API_KEY=your_gemini_api_key_here
STABILITY_API_KEY=your_stability_api_key_here
```

### 3. Start the System
```bash
python run_server.py
```

### 4. Access the Dashboard
Open your browser and navigate to:
- **Main Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 📋 System Architecture

### Backend Components
- **FastAPI Server** (`backend/app.py`) - Main API server
- **Market Intelligence Engine** (`backend/market_intel.py`) - Real hiring data processing
- **AI Content Generator** (`backend/ai_engine.py`) - Campaign content creation
- **Localization Engine** (`backend/localization.py`) - City-specific adaptations
- **Image Generator** (`backend/image_generator.py`) - Visual content creation
- **ML Optimizer** (`backend/ml_optimizer.py`) - Performance prediction

### Frontend Components
- **Dashboard UI** (`MI/index.html`) - Main user interface
- **Styling** (`MI/style.css`) - Responsive design
- **JavaScript** (`MI/app.js`) - Interactive functionality
- **Backend Connector** (`backend/dashboard_connector.js`) - API integration

### Data Sources
- **Hiring Data**: `comprehensive_company_hiring_data (2).xlsx`
- **Marketing Data**: `intelligent_marketing_automation_data.xlsx`

---

## 🧪 Testing

### Run System Tests
```bash
python test_system.py
```

### Test Coverage
- ✅ Backend Health Checks
- ✅ Market Intelligence APIs
- ✅ Campaign Generation
- ✅ Performance Analytics
- ✅ Error Handling
- ✅ Data Processing

### Expected Test Results
- **Success Rate**: >90%
- **Response Time**: <2 seconds for most endpoints
- **Campaign Generation**: <10 seconds

---

## 🔧 Configuration

### Server Configuration
- **Host**: 0.0.0.0 (accessible from network)
- **Port**: 8000 (configurable)
- **Reload**: Enabled in development

### Performance Tuning
- **Workers**: 1 (increase for production)
- **Memory**: 2GB recommended
- **Concurrent Requests**: 100+

### API Rate Limits
- **Campaign Generation**: 10 requests/minute
- **Market Intelligence**: 100 requests/minute
- **General APIs**: 1000 requests/minute

---

## 📊 Features Overview

### 🎯 Market Intelligence
- **Real-time hiring data** from 8+ Indian cities
- **Skill demand analysis** across 20+ technologies
- **Company hiring trends** with 500+ companies
- **Salary insights** and market scoring

### 🤖 AI Campaign Generation
- **Personalized content** for email, social media, display ads
- **City-specific localization** with cultural context
- **Performance predictions** using ML models
- **Brand-consistent visuals** with upGrad styling

### 📈 Performance Analytics
- **Platform comparison** (Facebook, LinkedIn, Instagram, etc.)
- **City performance metrics** with ROI tracking
- **Content theme analysis** and optimization
- **Real-time dashboard updates**

### 🌍 Geographic Localization
- **8 Tier-1 Indian cities** with cultural adaptation
- **Regional language support** for key phrases
- **Local event integration** and market context
- **City-specific campaign hooks**

---

## 🚀 Production Deployment

### Option 1: Local Server
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.app:app --bind 0.0.0.0:8000
```

### Option 2: Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run_server.py"]
```

### Option 3: Cloud Deployment
- **AWS**: Use EC2 + Application Load Balancer
- **Google Cloud**: Use Cloud Run or Compute Engine
- **Azure**: Use App Service or Container Instances
- **Heroku**: Use web dyno with Procfile

---

## 🔒 Security Considerations

### API Security
- **CORS enabled** for frontend integration
- **Input validation** on all endpoints
- **Rate limiting** to prevent abuse
- **Error handling** without sensitive data exposure

### Data Security
- **No sensitive data storage** in logs
- **API keys** stored in environment variables
- **HTTPS recommended** for production
- **Data encryption** for sensitive information

---

## 📝 API Documentation

### Core Endpoints
- `GET /api/health` - System health check
- `GET /api/market-intelligence` - Market data
- `POST /api/generate-campaign` - AI campaign generation
- `GET /api/city-insights/{city}` - City-specific data
- `GET /api/performance-analytics` - Analytics dashboard

### Response Format
```json
{
  "status": "success",
  "data": { ... },
  "timestamp": "2025-01-07T10:30:00Z"
}
```

### Error Handling
```json
{
  "status": "error",
  "message": "Error description",
  "timestamp": "2025-01-07T10:30:00Z"
}
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Check port availability
netstat -an | grep 8000
```

#### Data Loading Issues
```bash
# Verify data files exist
ls -la *.xlsx

# Check file permissions
chmod 644 *.xlsx

# Test data loading
python -c "import pandas as pd; print(pd.read_excel('comprehensive_company_hiring_data (2).xlsx').shape)"
```

#### API Connection Issues
```bash
# Test backend health
curl http://localhost:8000/api/health

# Check firewall settings
# Ensure port 8000 is open

# Test from different network
curl http://your-server-ip:8000/api/health
```

### Performance Issues
- **Slow campaign generation**: Check AI API keys and network
- **High memory usage**: Reduce concurrent requests
- **Database timeouts**: Optimize data queries

### Logging
- **Application logs**: Check console output
- **Error logs**: Review error messages in detail
- **Performance logs**: Monitor response times

---

## 📞 Support

### Documentation
- **API Docs**: http://localhost:8000/docs
- **System Tests**: `python test_system.py`
- **Test Report**: `test_report.json`

### Monitoring
- **Health Check**: http://localhost:8000/api/health
- **System Status**: Monitor CPU, memory, disk usage
- **API Performance**: Track response times and error rates

### Maintenance
- **Regular Updates**: Keep dependencies updated
- **Data Refresh**: Update Excel files monthly
- **Performance Monitoring**: Track system metrics
- **Backup Strategy**: Regular data backups

---

## 🎉 Success Metrics

### System Performance
- **Uptime**: >99.5%
- **Response Time**: <2 seconds average
- **Error Rate**: <1%
- **Concurrent Users**: 50+

### Business Impact
- **Campaign Generation**: 10x faster than manual
- **Market Intelligence**: Real-time insights
- **Localization**: 8 cities covered
- **ROI Improvement**: 25%+ predicted

---

**🚀 Your upGrad AI Marketing Automation System is ready to transform digital marketing campaigns with AI-powered intelligence and localization!**
