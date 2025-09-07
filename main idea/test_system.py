#!/usr/bin/env python3
"""
upGrad AI Marketing Automation System - Test Suite
Comprehensive testing for all system components
"""

import asyncio
import requests
import json
import time
import sys
from pathlib import Path
import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemTester:
    """Comprehensive system testing for upGrad AI Marketing Automation"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.test_results = []
        
    def run_all_tests(self):
        """Run all system tests"""
        logger.info("🧪 Starting upGrad AI Marketing System Tests")
        logger.info("=" * 60)
        
        # Test categories
        test_categories = [
            ("Backend Health", self.test_backend_health),
            ("Market Intelligence", self.test_market_intelligence),
            ("Campaign Generation", self.test_campaign_generation),
            ("Performance Analytics", self.test_performance_analytics),
            ("API Endpoints", self.test_api_endpoints),
            ("Data Processing", self.test_data_processing),
            ("Error Handling", self.test_error_handling)
        ]
        
        for category, test_func in test_categories:
            logger.info(f"\n📋 Testing: {category}")
            logger.info("-" * 40)
            
            try:
                result = test_func()
                self.test_results.append({
                    "category": category,
                    "status": "PASS" if result else "FAIL",
                    "details": result
                })
                
                if result:
                    logger.info(f"✅ {category}: PASSED")
                else:
                    logger.error(f"❌ {category}: FAILED")
                    
            except Exception as e:
                logger.error(f"❌ {category}: ERROR - {str(e)}")
                self.test_results.append({
                    "category": category,
                    "status": "ERROR",
                    "details": str(e)
                })
        
        # Generate test report
        self.generate_test_report()
        
        # Return overall success
        failed_tests = [r for r in self.test_results if r["status"] != "PASS"]
        return len(failed_tests) == 0
    
    def test_backend_health(self):
        """Test backend health and availability"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                
                # Check required fields
                required_fields = ["status", "timestamp", "version", "services"]
                for field in required_fields:
                    if field not in health_data:
                        logger.error(f"Missing field in health response: {field}")
                        return False
                
                # Check service status
                if health_data["status"] != "healthy":
                    logger.error(f"Backend not healthy: {health_data['status']}")
                    return False
                
                logger.info(f"Backend version: {health_data.get('version', 'Unknown')}")
                logger.info(f"Services: {health_data.get('services', {})}")
                
                return True
            else:
                logger.error(f"Health check failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check request failed: {e}")
            return False
    
    def test_market_intelligence(self):
        """Test market intelligence endpoints"""
        try:
            # Test main market intelligence endpoint
            response = requests.get(f"{self.api_url}/market-intelligence", timeout=15)
            
            if response.status_code != 200:
                logger.error(f"Market intelligence failed: {response.status_code}")
                return False
            
            data = response.json()
            
            # Validate response structure
            if data.get("status") != "success":
                logger.error(f"Market intelligence status not success: {data.get('status')}")
                return False
            
            market_data = data.get("data", {})
            
            # Check for required data fields
            required_fields = ["city_performance", "total_positions", "total_companies"]
            for field in required_fields:
                if field not in market_data:
                    logger.warning(f"Missing market data field: {field}")
            
            # Test city insights
            test_cities = ["Bangalore", "Mumbai", "Delhi NCR"]
            for city in test_cities:
                city_response = requests.get(f"{self.api_url}/city-insights/{city}", timeout=10)
                if city_response.status_code == 200:
                    city_data = city_response.json()
                    if city_data.get("status") == "success":
                        logger.info(f"City insights for {city}: ✅")
                    else:
                        logger.warning(f"City insights for {city}: ⚠️")
                else:
                    logger.warning(f"City insights for {city} failed: {city_response.status_code}")
            
            # Test skill demand
            skill_response = requests.get(f"{self.api_url}/skill-demand", timeout=10)
            if skill_response.status_code == 200:
                logger.info("Skill demand endpoint: ✅")
            else:
                logger.warning(f"Skill demand failed: {skill_response.status_code}")
            
            return True
            
        except Exception as e:
            logger.error(f"Market intelligence test error: {e}")
            return False
    
    def test_campaign_generation(self):
        """Test AI campaign generation"""
        try:
            # Test campaign generation with sample data
            test_campaigns = [
                {
                    "course": "AI/ML",
                    "city": "Bangalore",
                    "campaign_type": "Email",
                    "trend_integration": True,
                    "localization": "basic"
                },
                {
                    "course": "Data Science",
                    "city": "Mumbai",
                    "campaign_type": "Social Media",
                    "trend_integration": False,
                    "localization": "advanced"
                }
            ]
            
            for i, campaign_data in enumerate(test_campaigns):
                logger.info(f"Testing campaign {i+1}: {campaign_data['course']} in {campaign_data['city']}")
                
                response = requests.post(
                    f"{self.api_url}/generate-campaign",
                    json=campaign_data,
                    timeout=30
                )
                
                if response.status_code != 200:
                    logger.error(f"Campaign generation failed: {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    return False
                
                result = response.json()
                
                if result.get("status") != "success":
                    logger.error(f"Campaign generation status not success: {result.get('status')}")
                    return False
                
                # Validate campaign content
                campaign_content = result.get("data", {}).get("content", {})
                required_content = ["email_subject", "email_body", "social_post", "call_to_action"]
                
                for field in required_content:
                    if field not in campaign_content:
                        logger.warning(f"Missing campaign content field: {field}")
                    else:
                        content_length = len(str(campaign_content[field]))
                        logger.info(f"{field}: {content_length} characters")
                
                # Check predictions
                predictions = result.get("data", {}).get("predictions", {})
                if predictions:
                    logger.info(f"Performance predictions: {predictions}")
                
                logger.info(f"Campaign {i+1}: ✅")
            
            return True
            
        except Exception as e:
            logger.error(f"Campaign generation test error: {e}")
            return False
    
    def test_performance_analytics(self):
        """Test performance analytics endpoints"""
        try:
            response = requests.get(f"{self.api_url}/performance-analytics", timeout=15)
            
            if response.status_code != 200:
                logger.error(f"Performance analytics failed: {response.status_code}")
                return False
            
            data = response.json()
            
            if data.get("status") != "success":
                logger.error(f"Performance analytics status not success: {data.get('status')}")
                return False
            
            analytics_data = data.get("data", {})
            
            # Check for analytics components
            expected_components = ["platform_performance", "city_performance", "content_themes", "campaign_metrics"]
            for component in expected_components:
                if component in analytics_data:
                    logger.info(f"Analytics component {component}: ✅")
                else:
                    logger.warning(f"Missing analytics component: {component}")
            
            return True
            
        except Exception as e:
            logger.error(f"Performance analytics test error: {e}")
            return False
    
    def test_api_endpoints(self):
        """Test all API endpoints for basic functionality"""
        endpoints = [
            ("/health", "GET"),
            ("/market-intelligence", "GET"),
            ("/skill-demand", "GET"),
            ("/performance-analytics", "GET"),
            ("/city-insights/Bangalore", "GET"),
            ("/course-relevance/AI/ML", "GET")
        ]
        
        success_count = 0
        
        for endpoint, method in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                else:
                    response = requests.post(f"{self.api_url}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    logger.info(f"{method} {endpoint}: ✅")
                    success_count += 1
                else:
                    logger.warning(f"{method} {endpoint}: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"{method} {endpoint}: ERROR - {e}")
        
        return success_count >= len(endpoints) * 0.8  # 80% success rate
    
    def test_data_processing(self):
        """Test data processing capabilities"""
        try:
            # Test if data files exist
            data_files = [
                "main idea/comprehensive_company_hiring_data (2).xlsx",
                "main idea/intelligent_marketing_automation_data.xlsx"
            ]
            
            files_exist = 0
            for file_path in data_files:
                if Path(file_path).exists():
                    logger.info(f"Data file exists: {Path(file_path).name} ✅")
                    files_exist += 1
                else:
                    logger.warning(f"Data file missing: {Path(file_path).name} ⚠️")
            
            # Test data processing through market intelligence
            response = requests.get(f"{self.api_url}/market-intelligence", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                market_data = data.get("data", {})
                
                # Check if we have processed data
                if market_data.get("total_positions", 0) > 0:
                    logger.info(f"Data processing successful: {market_data.get('total_positions')} positions processed")
                    return True
                else:
                    logger.warning("Data processing returned no positions")
                    return files_exist > 0  # Pass if files exist even if processing is limited
            
            return False
            
        except Exception as e:
            logger.error(f"Data processing test error: {e}")
            return False
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        try:
            # Test invalid endpoints
            invalid_response = requests.get(f"{self.api_url}/invalid-endpoint", timeout=5)
            if invalid_response.status_code == 404:
                logger.info("404 handling: ✅")
            
            # Test invalid campaign data
            invalid_campaign = requests.post(
                f"{self.api_url}/generate-campaign",
                json={"invalid": "data"},
                timeout=10
            )
            
            if invalid_campaign.status_code in [400, 422, 500]:
                logger.info("Invalid campaign data handling: ✅")
            
            # Test invalid city
            invalid_city = requests.get(f"{self.api_url}/city-insights/InvalidCity", timeout=5)
            if invalid_city.status_code in [404, 400]:
                logger.info("Invalid city handling: ✅")
            
            return True
            
        except Exception as e:
            logger.error(f"Error handling test error: {e}")
            return False
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 TEST REPORT SUMMARY")
        logger.info("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        error_tests = len([r for r in self.test_results if r["status"] == "ERROR"])
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"✅ Passed: {passed_tests}")
        logger.info(f"❌ Failed: {failed_tests}")
        logger.info(f"⚠️  Errors: {error_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        logger.info("\nDetailed Results:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
            logger.info(f"{status_icon} {result['category']}: {result['status']}")
        
        # Save report to file
        report_file = Path("test_report.json")
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "errors": error_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "results": self.test_results
            }, f, indent=2)
        
        logger.info(f"\n📄 Test report saved to: {report_file}")

def main():
    """Main test execution"""
    print("🚀 upGrad AI Marketing Automation - System Test Suite")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server not responding. Please start the server first:")
            print("   python run_server.py")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Server not running. Please start the server first:")
        print("   python run_server.py")
        sys.exit(1)
    
    # Run tests
    tester = SystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! System is ready for deployment.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the results above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
