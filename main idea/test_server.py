#!/usr/bin/env python3
"""
Simple test server to verify the new UI design
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the new dashboard design"""
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>upGrad AI Marketing Automation - New Design</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
                color: #ffffff;
                line-height: 1.6;
                overflow-x: hidden;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                font-weight: 400;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .dashboard {
                display: grid;
                grid-template-columns: 420px 1fr 380px;
                min-height: 100vh;
                gap: 8px;
                padding: 8px;
                background: rgba(0, 0, 0, 0.1);
            }
            
            .sidebar, .main-content, .system-panel {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                padding: 32px;
                overflow-y: auto;
                border-radius: 24px;
                box-shadow: 
                    0 20px 60px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.8);
                border: 2px solid rgba(255, 255, 255, 0.3);
                color: #2d3748;
            }
            
            .header {
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 40px;
                padding: 28px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                border-radius: 24px;
                box-shadow: 
                    0 15px 40px rgba(102, 126, 234, 0.4),
                    inset 0 2px 0 rgba(255, 255, 255, 0.3);
                position: relative;
                overflow: hidden;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            
            .logo { 
                color: #ffffff; 
                font-size: 28px; 
                text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
                z-index: 1;
            }
            .title { 
                font-size: 20px; 
                font-weight: 800; 
                color: #ffffff;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                z-index: 1;
            }
            
            .content-type-selector {
                display: flex;
                gap: 8px;
                margin-bottom: 32px;
                background: rgba(255, 255, 255, 0.8);
                padding: 8px;
                border-radius: 20px;
                backdrop-filter: blur(20px);
                border: 2px solid rgba(102, 126, 234, 0.2);
            }
            
            .type-btn {
                flex: 1;
                padding: 16px 20px;
                border: none;
                border-radius: 16px;
                font-weight: 600;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.3s ease;
                background: transparent;
                color: #4a5568;
                font-family: 'Poppins', sans-serif;
            }
            
            .type-btn:hover {
                background: rgba(102, 126, 234, 0.1);
                color: #667eea;
                transform: translateY(-2px);
            }
            
            .type-btn.active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #ffffff;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            }
            
            .section {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                padding: 32px;
                margin-bottom: 32px;
                border: 2px solid rgba(102, 126, 234, 0.2);
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.1),
                    inset 0 2px 0 rgba(255, 255, 255, 0.8);
                position: relative;
                overflow: hidden;
            }
            
            .section-header {
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 24px;
                color: #667eea;
                font-weight: 800;
                font-size: 18px;
                text-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
            }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <!-- Left Sidebar -->
            <div class="sidebar">
                <div class="header">
                    <div class="logo">🚀</div>
                    <div class="title">upGrad AI Marketing</div>
                </div>
                
                <div class="section">
                    <div class="section-header">
                        <span>⚙️</span> Campaign Settings
                    </div>
                    <p>This is the new design with:</p>
                    <ul style="margin: 16px 0; padding-left: 20px;">
                        <li>Animated gradient background</li>
                        <li>Glass morphism panels</li>
                        <li>Modern Poppins font</li>
                        <li>Rounded corners (24px)</li>
                        <li>Enhanced shadows</li>
                    </ul>
                </div>
            </div>
            
            <!-- Main Content -->
            <div class="main-content">
                <div class="content-type-selector">
                    <button class="type-btn active">📧 Email Campaigns</button>
                    <button class="type-btn">📱 Social Media</button>
                    <button class="type-btn">🎨 Image Generation</button>
                    <button class="type-btn">💬 SMS/WhatsApp</button>
                </div>
                
                <div class="section">
                    <div class="section-header">
                        <span>📧</span> Email Campaign Generator
                    </div>
                    <p style="color: #4a5568; font-size: 16px; line-height: 1.6;">
                        This is the new main content area with dedicated sections for different content types.
                        The design features modern glass morphism effects, vibrant gradients, and professional typography.
                    </p>
                </div>
            </div>
            
            <!-- Right Panel -->
            <div class="system-panel">
                <div class="section">
                    <div class="section-header">
                        <span>📊</span> System Status
                    </div>
                    <p style="color: #4a5568;">
                        New design successfully loaded!<br>
                        ✅ Animated background<br>
                        ✅ Glass morphism<br>
                        ✅ Modern typography<br>
                        ✅ Content type tabs
                    </p>
                </div>
            </div>
        </div>
        
        <script>
            console.log('New design loaded successfully!');
            console.log('Features:');
            console.log('- Animated gradient background');
            console.log('- Glass morphism panels');
            console.log('- Modern Poppins font');
            console.log('- Content type selector');
        </script>
    </body>
    </html>
    """
    
    # Create response with cache-busting headers
    response = HTMLResponse(content=html_content, status_code=200)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    print("🎨 Starting Test Server with New Design")
    print("📱 Dashboard: http://localhost:8001")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )
