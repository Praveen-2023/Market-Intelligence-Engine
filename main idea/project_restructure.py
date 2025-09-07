#!/usr/bin/env python3
"""
Project Restructuring Script for upGrad AI Marketing Automation
Converts current structure to industry-standard Python project layout
"""

import os
import shutil
from pathlib import Path

def create_industry_structure():
    """Create industry-standard project structure"""
    
    # Define the new structure
    structure = {
        'src': {
            'upgrad_ai_marketing': {
                '__init__.py': '',
                'api': {
                    '__init__.py': '',
                    'routes': {
                        '__init__.py': '',
                        'health.py': '',
                        'campaigns.py': '',
                        'analytics.py': '',
                        'market_intel.py': ''
                    },
                    'dependencies.py': '',
                    'middleware.py': ''
                },
                'core': {
                    '__init__.py': '',
                    'config.py': '',
                    'exceptions.py': '',
                    'logging.py': ''
                },
                'services': {
                    '__init__.py': '',
                    'ai_engine.py': '',
                    'image_generator.py': '',
                    'market_intelligence.py': '',
                    'localization.py': '',
                    'ml_optimizer.py': ''
                },
                'models': {
                    '__init__.py': '',
                    'campaign.py': '',
                    'market_data.py': '',
                    'analytics.py': ''
                },
                'utils': {
                    '__init__.py': '',
                    'helpers.py': '',
                    'validators.py': ''
                }
            }
        },
        'frontend': {
            'static': {
                'css': {},
                'js': {},
                'images': {},
                'fonts': {}
            },
            'templates': {}
        },
        'tests': {
            '__init__.py': '',
            'unit': {
                '__init__.py': '',
                'test_ai_engine.py': '',
                'test_market_intel.py': '',
                'test_campaigns.py': ''
            },
            'integration': {
                '__init__.py': '',
                'test_api_endpoints.py': '',
                'test_full_workflow.py': ''
            },
            'fixtures': {
                'sample_data.json': '',
                'test_campaigns.json': ''
            }
        },
        'data': {
            'raw': {},
            'processed': {},
            'models': {}
        },
        'docs': {
            'api': {},
            'deployment': {},
            'user_guide': {}
        },
        'scripts': {
            'setup.py': '',
            'deploy.py': '',
            'migrate_data.py': ''
        },
        'config': {
            'development.yaml': '',
            'production.yaml': '',
            'testing.yaml': ''
        }
    }
    
    # Create directory structure
    base_path = Path('.')
    
    def create_dirs(structure, current_path):
        for name, content in structure.items():
            new_path = current_path / name
            if isinstance(content, dict):
                new_path.mkdir(exist_ok=True)
                create_dirs(content, new_path)
            else:
                # Create file
                new_path.parent.mkdir(parents=True, exist_ok=True)
                if not new_path.exists():
                    new_path.write_text(content)
    
    create_dirs(structure, base_path)
    print("✅ Industry-standard directory structure created!")

def move_existing_files():
    """Move existing files to new structure"""
    
    # File mappings: old_path -> new_path
    file_mappings = {
        # Backend files
        'backend/app.py': 'src/upgrad_ai_marketing/main.py',
        'backend/ai_engine.py': 'src/upgrad_ai_marketing/services/ai_engine.py',
        'backend/image_generator.py': 'src/upgrad_ai_marketing/services/image_generator.py',
        'backend/market_intel.py': 'src/upgrad_ai_marketing/services/market_intelligence.py',
        'backend/localization.py': 'src/upgrad_ai_marketing/services/localization.py',
        'backend/ml_optimizer.py': 'src/upgrad_ai_marketing/services/ml_optimizer.py',
        
        # Frontend files
        'MI/index.html': 'frontend/templates/index.html',
        'MI/style.css': 'frontend/static/css/main.css',
        'MI/app.js': 'frontend/static/js/app.js',
        'backend/dashboard_connector.js': 'frontend/static/js/dashboard_connector.js',
        
        # Data files
        'comprehensive_company_hiring_data (2).xlsx': 'data/raw/company_hiring_data.xlsx',
        'intelligent_marketing_automation_data.xlsx': 'data/raw/marketing_automation_data.xlsx',
        
        # Config files
        '.env': 'config/.env',
        'requirements.txt': 'requirements.txt',
        
        # Documentation
        'DEPLOYMENT_GUIDE.md': 'docs/deployment/guide.md',
        'Complete-upGrad-AI-Marketing-System.md': 'docs/system_overview.md',
        'Augment-AI-Implementation-Guide.md': 'docs/implementation_guide.md',
        
        # Tests
        'test_system.py': 'tests/integration/test_full_system.py',
        
        # Scripts
        'run_server.py': 'scripts/run_server.py'
    }
    
    moved_files = []
    for old_path, new_path in file_mappings.items():
        old_file = Path(old_path)
        new_file = Path(new_path)
        
        if old_file.exists():
            # Create parent directories
            new_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            shutil.move(str(old_file), str(new_file))
            moved_files.append(f"{old_path} -> {new_path}")
            print(f"✅ Moved: {old_path} -> {new_path}")
    
    return moved_files

if __name__ == "__main__":
    print("🚀 Restructuring upGrad AI Marketing Automation to Industry Standards...")
    print("=" * 70)
    
    # Create new structure
    create_industry_structure()
    
    # Move existing files
    print("\n📁 Moving existing files...")
    moved_files = move_existing_files()
    
    print(f"\n✅ Project restructured successfully!")
    print(f"📊 Moved {len(moved_files)} files to new structure")
    print("\n🎯 Next steps:")
    print("1. Update import paths in Python files")
    print("2. Update configuration files")
    print("3. Test the restructured application")
