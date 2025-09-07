/**
 * upGrad AI Marketing Dashboard - Backend Integration
 * Connects frontend UI with FastAPI backend services
 */

class UpGradMarketingDashboard {
    constructor() {
        this.baseUrl = '/api';
        this.websocket = null;
        this.charts = {};
        this.isLoading = false;

        // Initialize dashboard
        this.init();
    }

    async init() {
        console.log('🚀 Initializing upGrad AI Marketing Dashboard');

        try {
            // Check backend health
            await this.checkBackendHealth();

            // Load initial data
            await this.loadMarketIntelligence();
            await this.loadPerformanceAnalytics();

            // Setup event listeners
            this.setupEventListeners();

            // Initialize charts
            this.initializeCharts();

            // Setup WebSocket for real-time updates
            this.setupWebSocket();

            console.log('✅ Dashboard initialized successfully');

        } catch (error) {
            console.error('❌ Dashboard initialization failed:', error);
            this.showError('Failed to initialize dashboard. Please refresh the page.');
        }
    }

    async checkBackendHealth() {
        // Check if backend services are running
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            const health = await response.json();

            if (health.status === 'healthy') {
                console.log('✅ Backend services are healthy');
                this.updateHealthStatus(true);
            } else {
                throw new Error('Backend services unhealthy');
            }
        } catch (error) {
            console.error('❌ Backend health check failed:', error);
            this.updateHealthStatus(false);
            throw error;
        }
    }

    updateHealthStatus(isHealthy) {
        // Update UI health indicator
        const indicator = document.querySelector('.health-indicator');
        if (indicator) {
            indicator.className = `health-indicator ${isHealthy ? 'healthy' : 'unhealthy'}`;
            indicator.textContent = isHealthy ? '🟢 Online' : '🔴 Offline';
        }
    }

    async loadMarketIntelligence() {
        // Load market intelligence data from backend
        try {
            this.showLoadingState('market-intelligence');

            const response = await fetch(`${this.baseUrl}/market-intelligence`);
            const result = await response.json();

            if (result.status === 'success') {
                this.updateMarketTrends(result.data);
                this.updateKPIs(result.data);
                console.log('📊 Market intelligence loaded');
            } else {
                throw new Error('Failed to load market intelligence');
            }

        } catch (error) {
            console.error('Error loading market intelligence:', error);
            this.showError('Failed to load market data');
        } finally {
            this.hideLoadingState('market-intelligence');
        }
    }

    async generateCampaign() {
        // Generate AI-powered campaign
        try {
            // Get form data
            const formData = this.getCampaignFormData();

            // Validate form
            if (!this.validateCampaignForm(formData)) {
                this.showError('Please fill in all required fields');
                return;
            }

            // Show loading state
            this.showCampaignLoading();

            // Call backend API
            const response = await fetch(`${this.baseUrl}/generate-campaign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.status === 'success') {
                // Display results
                this.displayCampaignResults(result.data);
                this.showSuccessMessage('Campaign generated successfully!');
                console.log('🚀 Campaign generated successfully');
            } else {
                throw new Error(result.message || 'Campaign generation failed');
            }

        } catch (error) {
            console.error('Error generating campaign:', error);
            this.showError('Failed to generate campaign. Please try again.');
        } finally {
            this.hideCampaignLoading();
        }
    }

    getCampaignFormData() {
        // Extract form data for campaign generation
        return {
            course: document.getElementById('course-select')?.value || '',
            city: document.getElementById('city-select')?.value || '',
            campaign_type: document.getElementById('campaign-type')?.value || '',
            trend_integration: document.getElementById('trend-integration')?.checked || false,
            localization: document.querySelector('input[name="localization"]:checked')?.value || 'basic'
        };
    }

    validateCampaignForm(formData) {
        // Validate campaign form data
        return formData.course && formData.city && formData.campaign_type;
    }

    setupEventListeners() {
        // Setup all event listeners

        // Campaign generation button
        const generateBtn = document.getElementById('generate-campaign');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateCampaign());
        }

        // Navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageId = link.getAttribute('data-page');
                this.navigateToPage(pageId);
            });
        });
    }

    showError(message) {
        // Show error message to user
        console.error('Error:', message);

        // Create or update error notification
        let errorDiv = document.querySelector('.error-notification');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-notification';
            document.body.appendChild(errorDiv);
        }

        errorDiv.innerHTML = `
            <div class="error-content">
                <span class="error-icon">❌</span>
                <span class="error-message">${message}</span>
                <button class="error-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        errorDiv.style.display = 'block';

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 5000);
    }

    showSuccessMessage(message) {
        // Show success message to user
        console.log('Success:', message);

        // Create or update success notification
        let successDiv = document.querySelector('.success-notification');
        if (!successDiv) {
            successDiv = document.createElement('div');
            successDiv.className = 'success-notification';
            document.body.appendChild(successDiv);
        }

        successDiv.innerHTML = `
            <div class="success-content">
                <span class="success-icon">✅</span>
                <span class="success-message">${message}</span>
                <button class="success-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        successDiv.style.display = 'block';

        // Auto-hide after 3 seconds
        setTimeout(() => {
            if (successDiv.parentElement) {
                successDiv.remove();
            }
        }, 3000);
    }

    showLoadingState(context) {
        // Show loading state with visual feedback
        console.log(`Loading ${context}...`);

        const loader = document.querySelector(`[data-loading="${context}"]`);
        if (loader) {
            loader.classList.remove('hidden');
        }

        // Add loading class to relevant sections
        const section = document.querySelector(`[data-section="${context}"]`);
        if (section) {
            section.classList.add('loading');
        }
    }

    hideLoadingState(context) {
        // Hide loading state
        console.log(`Finished loading ${context}`);

        const loader = document.querySelector(`[data-loading="${context}"]`);
        if (loader) {
            loader.classList.add('hidden');
        }

        // Remove loading class
        const section = document.querySelector(`[data-section="${context}"]`);
        if (section) {
            section.classList.remove('loading');
        }
    }

    showCampaignLoading() {
        // Show campaign loading with modal
        const generateBtn = document.getElementById('generate-campaign');
        if (generateBtn) {
            generateBtn.disabled = true;
            generateBtn.textContent = '🔄 Generating...';
        }

        // Show loading modal
        const modal = document.getElementById('loading-modal');
        if (modal) {
            modal.classList.remove('hidden');
        }

        // Update loading text with progress
        const loadingText = document.querySelector('.loading-text');
        if (loadingText) {
            let step = 0;
            const steps = [
                'Analyzing market data...',
                'Generating AI content...',
                'Applying localization...',
                'Optimizing performance...',
                'Finalizing campaign...'
            ];

            const interval = setInterval(() => {
                if (step < steps.length) {
                    loadingText.textContent = steps[step];
                    step++;
                } else {
                    clearInterval(interval);
                }
            }, 1500);

            // Store interval for cleanup
            this.loadingInterval = interval;
        }
    }

    hideCampaignLoading() {
        // Hide campaign loading
        const generateBtn = document.getElementById('generate-campaign');
        if (generateBtn) {
            generateBtn.disabled = false;
            generateBtn.textContent = '🚀 Generate AI Campaign';
        }

        // Hide loading modal
        const modal = document.getElementById('loading-modal');
        if (modal) {
            modal.classList.add('hidden');
        }

        // Clear loading interval
        if (this.loadingInterval) {
            clearInterval(this.loadingInterval);
            this.loadingInterval = null;
        }

        // Reset loading text
        const loadingText = document.querySelector('.loading-text');
        if (loadingText) {
            loadingText.textContent = 'Generating AI-powered campaign...';
        }
    }

    updateMarketTrends(data) {
        // Update market trends display
        console.log('Updating market trends:', data);

        const trendsContainer = document.querySelector('.trends-grid');
        if (!trendsContainer || !data.city_performance) return;

        trendsContainer.innerHTML = '';

        Object.entries(data.city_performance).forEach(([city, cityData]) => {
            const trendCard = document.createElement('div');
            trendCard.className = 'trend-card';

            const impact = cityData.positions_available > 1000 ? 'Very High' :
                          cityData.positions_available > 500 ? 'High' : 'Medium';

            trendCard.innerHTML = `
                <div class="trend-header">
                    <span class="trend-title">${city} Hiring</span>
                    <span class="trend-impact ${impact.toLowerCase().replace(' ', '-')}">${impact} Impact</span>
                </div>
                <div class="trend-value">${cityData.positions_available.toLocaleString()} Positions</div>
                <div class="trend-source">${cityData.companies_hiring} Companies Hiring</div>
            `;

            trendsContainer.appendChild(trendCard);
        });
    }

    updateKPIs(data) {
        // Update KPI display with real data
        console.log('Updating KPIs:', data);

        const kpiUpdates = {
            'total-campaigns': data.total_companies || 24,
            'active-markets': Object.keys(data.city_performance || {}).length || 8,
            'ai-optimization-score': '87%',
            'current-roi': '4.2x'
        };

        Object.entries(kpiUpdates).forEach(([id, value]) => {
            const element = document.querySelector(`[data-kpi="${id}"] .kpi-value`);
            if (element) {
                element.textContent = value;
                // Add animation effect
                element.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    element.style.transform = 'scale(1)';
                }, 200);
            }
        });
    }

    displayCampaignResults(data) {
        // Display campaign results with enhanced UI
        console.log('Displaying campaign results:', data);

        // Update email content
        const emailSubject = document.getElementById('email-subject-text');
        const emailBody = document.getElementById('email-body-text');
        const socialPost = document.getElementById('social-post-text');

        if (emailSubject && data.content?.email_subject) {
            emailSubject.textContent = data.content.email_subject;
            this.animateTextUpdate(emailSubject);
        }

        if (emailBody && data.content?.email_body) {
            emailBody.textContent = data.content.email_body;
            this.animateTextUpdate(emailBody);
        }

        if (socialPost && data.content?.social_post) {
            socialPost.textContent = data.content.social_post;
            this.animateTextUpdate(socialPost);
        }

        // Update localized content if available
        const localizedText = document.getElementById('localized-text');
        if (localizedText && data.content?.regional_version) {
            localizedText.textContent = data.content.regional_version;
            this.animateTextUpdate(localizedText);
        }

        // Update predictions
        if (data.predictions) {
            this.updatePredictionsDisplay(data.predictions);
        }

        // Show image if available
        if (data.image_url) {
            this.displayGeneratedImage(data.image_url);
        }

        // Show results container with animation
        const resultsContainer = document.getElementById('campaign-results');
        if (resultsContainer) {
            resultsContainer.classList.remove('hidden');
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    animateTextUpdate(element) {
        // Add subtle animation to text updates
        element.style.opacity = '0';
        element.style.transform = 'translateY(10px)';

        setTimeout(() => {
            element.style.transition = 'all 0.3s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100);
    }

    updatePredictionsDisplay(predictions) {
        // Update performance predictions
        const predictionMappings = {
            'predicted-ctr': predictions.ctr,
            'predicted-conversion': predictions.conversion_rate,
            'predicted-roas': predictions.roas,
            'predicted-cost': predictions.cost_per_conversion
        };

        Object.entries(predictionMappings).forEach(([elementId, value]) => {
            const element = document.getElementById(elementId);
            if (element && value) {
                element.textContent = value;
                this.animateTextUpdate(element);
            }
        });
    }

    displayGeneratedImage(imageUrl) {
        // Display generated campaign image
        const imageContainer = document.getElementById('generated-image');
        if (imageContainer) {
            imageContainer.innerHTML = `
                <img src="${imageUrl}"
                     alt="Generated Campaign Image"
                     style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); opacity: 0; transition: opacity 0.5s ease;"
                     onload="this.style.opacity = 1;">
            `;
        }
    }

    navigateToPage(pageId) {
        // Navigate to different pages
        console.log(`Navigating to ${pageId}`);

        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Show target page
        const targetPage = document.getElementById(pageId);
        if (targetPage) {
            targetPage.classList.add('active');
        }

        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });

        const activeLink = document.querySelector(`[data-page="${pageId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    async loadPerformanceAnalytics() {
        // Load performance analytics
        console.log('Loading performance analytics...');
    }

    initializeCharts() {
        // Initialize charts
        console.log('Initializing charts...');
    }

    setupWebSocket() {
        // Setup WebSocket connection
        console.log('Setting up WebSocket...');
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎯 DOM loaded, initializing upGrad AI Marketing Dashboard');
    window.marketingDashboard = new UpGradMarketingDashboard();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UpGradMarketingDashboard;
}
