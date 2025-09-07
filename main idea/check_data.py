#!/usr/bin/env python3
"""
Check and convert data files to CSV for better real-time processing
"""

import pandas as pd
import os
from pathlib import Path

def check_and_convert_data():
    """Check Excel files and convert to CSV"""
    
    data_dir = Path("data/raw")
    
    # Check company hiring data
    hiring_file = data_dir / "company_hiring_data.xlsx"
    if hiring_file.exists():
        print("📊 Loading company hiring data...")
        try:
            df = pd.read_excel(hiring_file)
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns)}")
            
            # Convert to CSV
            csv_file = data_dir / "company_hiring_data.csv"
            df.to_csv(csv_file, index=False)
            print(f"   ✅ Converted to CSV: {csv_file}")
            
            # Show sample
            print("   Sample data:")
            print(df.head(3))
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("❌ Company hiring data not found")
    
    print("-" * 60)
    
    # Check marketing automation data
    marketing_file = data_dir / "marketing_automation_data.xlsx"
    if marketing_file.exists():
        print("📈 Loading marketing automation data...")
        try:
            # Try to read different sheets
            xl_file = pd.ExcelFile(marketing_file)
            print(f"   Sheets: {xl_file.sheet_names}")
            
            for sheet in xl_file.sheet_names:
                df = pd.read_excel(marketing_file, sheet_name=sheet)
                print(f"   Sheet '{sheet}': {df.shape}")
                
                # Convert to CSV
                csv_file = data_dir / f"marketing_{sheet.lower()}.csv"
                df.to_csv(csv_file, index=False)
                print(f"   ✅ Converted to CSV: {csv_file}")
                
                if df.shape[0] > 0:
                    print(f"   Columns: {list(df.columns)}")
                    print("   Sample data:")
                    print(df.head(2))
                print()
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("❌ Marketing automation data not found")

if __name__ == "__main__":
    check_and_convert_data()
