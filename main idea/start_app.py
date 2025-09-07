#!/usr/bin/env python3
"""
Startup script for upGrad AI Marketing Automation System
"""

import sys
import os
import time
import subprocess

def main():
    print("🚀 upGrad AI Marketing Automation System")
    print("=" * 50)
    print()
    
    # Check if required files exist
    required_files = [
        "simple_server.py",
        "data/raw/company_hiring_data.xlsx",
        "data/raw/marketing_automation_data.xlsx",
        "config/.env"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print()
        print("Please ensure all required files are present.")
        return False
    
    print("✅ All required files found")
    print()
    
    # Test module import
    try:
        print("📦 Loading application modules...")
        import simple_server
        print("✅ Application modules loaded successfully")
        print()
    except Exception as e:
        print(f"❌ Error loading modules: {e}")
        return False
    
    # Start the server
    try:
        print("🌐 Starting web server...")
        print("📱 Dashboard: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        import uvicorn
        uvicorn.run(
            "simple_server:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
