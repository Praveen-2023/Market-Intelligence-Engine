#!/usr/bin/env python3
"""
Server startup script for upGrad AI Marketing Automation
Industry-standard server startup with proper error handling
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import uvicorn

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'pandas', 'openpyxl', 
        'requests', 'python-dotenv', 'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("✅ All packages installed!")

def print_startup_banner():
    """Print startup banner"""
    print("=" * 60)
    print("🚀 upGrad AI Marketing Automation System")
    print("=" * 60)
    print("📊 Loading market intelligence data...")
    print("🤖 Initializing AI engines...")
    print("📈 Setting up performance analytics...")
    print("🎨 Loading frontend assets...")
    print("=" * 60)

def main():
    """Main server startup function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print_startup_banner()
    
    # Check dependencies
    try:
        check_dependencies()
    except Exception as e:
        logger.error(f"Dependency check failed: {e}")
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Start the server
    try:
        print("🌐 Starting FastAPI server...")
        print("📱 Dashboard will be available at: http://localhost:8000")
        print("📚 API documentation at: http://localhost:8000/docs")
        print("=" * 60)
        
        # Run the application
        uvicorn.run(
            "src.upgrad_ai_marketing.app:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        logger.error(f"Failed to import app: {e}")
        print("❌ Failed to start server. Check your installation.")
        print("💡 Make sure you're running from the project root directory")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
