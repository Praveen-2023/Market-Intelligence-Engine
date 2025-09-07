"""
Performance Learning System for upGrad AI Marketing Automation
ML-based campaign optimization and performance prediction
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import json
import joblib

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("Scikit-learn not available. Install with: pip install scikit-learn")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CampaignOptimizer:
    """
    ML-powered campaign optimization system
    Predicts performance and suggests improvements
    """
    
    def __init__(self, data_path: str = "main idea"):
        self.data_path = Path(data_path)
        self.model = None
        self.encoders = {}
        self.scaler = None
        self.is_trained = False
        self.feature_importance = {}
        self.performance_history = []
        
        # Initialize models if sklearn is available
        if SKLEARN_AVAILABLE:
            self.model = RandomForestRegressor(
                n_estimators=100, 
                random_state=42,
                max_depth=10,
                min_samples_split=5
            )
            self.scaler = StandardScaler()
        
        # Load training data and train model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize and train the ML model"""
        try:
            # Load training data
            training_data = self._load_training_data()
            
            if training_data is not None and not training_data.empty:
                # Train the model
                self.train_model(training_data)
            else:
                # Create synthetic training data for development
                logger.warning("No training data found, creating synthetic data")
                synthetic_data = self._create_synthetic_training_data()
                self.train_model(synthetic_data)
                
        except Exception as e:
            logger.error(f"Error initializing model: {e}")
            self.is_trained = False
    
    def _load_training_data(self) -> Optional[pd.DataFrame]:
        """Load ML training data from Excel file"""
        try:
            excel_file = self.data_path / "intelligent_marketing_automation_data.xlsx"
            if excel_file.exists():
                # Try to load ML training data sheet
                df = pd.read_excel(excel_file, sheet_name="ML_Training_Data")
                logger.info(f"Loaded training data: {df.shape[0]} samples")
                return df
            else:
                logger.warning(f"Training data file not found: {excel_file}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            return None
    
    def _create_synthetic_training_data(self) -> pd.DataFrame:
        """Create synthetic training data for development"""
        
        np.random.seed(42)
        n_samples = 500
        
        # Define possible values for categorical features
        brands = ['upgrad', 'byju', 'unacademy', 'vedantu']
        content_themes = ['AI/ML Skills', 'Career Growth', 'Job Security', 'Salary Boost', 'Skill Development']
        visual_styles = ['Modern', 'Professional', 'Creative', 'Minimalist']
        emotions = ['Motivation', 'Urgency', 'Confidence', 'Aspiration']
        campaign_types = ['Email', 'Social Media', 'Display Ads']
        platforms = ['Facebook', 'Instagram', 'LinkedIn', 'Twitter', 'YouTube', 'Google Ads']
        cities = ['Bangalore', 'Mumbai', 'Delhi NCR', 'Hyderabad', 'Chennai', 'Pune']
        age_groups = ['22-28', '28-35', '35-42', '42-50']
        
        # Generate synthetic data
        data = []
        for i in range(n_samples):
            # Categorical features
            brand = np.random.choice(brands)
            content_theme = np.random.choice(content_themes)
            visual_style = np.random.choice(visual_styles)
            target_emotion = np.random.choice(emotions)
            campaign_type = np.random.choice(campaign_types)
            platform = np.random.choice(platforms)
            target_city = np.random.choice(cities)
            age_group = np.random.choice(age_groups)
            
            # Numerical features
            character_count = np.random.randint(50, 300)
            readability_score = np.random.uniform(6.0, 12.0)
            brand_consistency_score = np.random.uniform(7.0, 10.0)
            accessibility_score = np.random.uniform(8.0, 10.0)
            
            # Calculate performance score based on feature interactions
            performance_score = self._calculate_synthetic_performance(
                brand, content_theme, visual_style, target_emotion,
                campaign_type, platform, target_city, age_group,
                character_count, readability_score, brand_consistency_score, accessibility_score
            )
            
            data.append({
                'brand_id': brand,
                'content_theme': content_theme,
                'visual_style': visual_style,
                'target_emotion': target_emotion,
                'campaign_type': campaign_type,
                'platform': platform,
                'target_city': target_city,
                'target_age_group': age_group,
                'character_count': character_count,
                'readability_score': readability_score,
                'brand_consistency_score': brand_consistency_score,
                'accessibility_score': accessibility_score,
                'performance_score': performance_score
            })
        
        df = pd.DataFrame(data)
        logger.info(f"Created synthetic training data: {df.shape[0]} samples")
        return df
    
    def _calculate_synthetic_performance(self, brand, content_theme, visual_style, target_emotion,
                                       campaign_type, platform, target_city, age_group,
                                       character_count, readability_score, brand_consistency_score, accessibility_score) -> float:
        """Calculate synthetic performance score based on feature interactions"""
        
        base_score = 5.0
        
        # Brand multipliers
        brand_multipliers = {'upgrad': 1.2, 'byju': 1.0, 'unacademy': 0.9, 'vedantu': 0.8}
        base_score *= brand_multipliers.get(brand, 1.0)
        
        # Content theme impact
        theme_multipliers = {
            'Job Security': 1.3, 'Career Growth': 1.2, 'AI/ML Skills': 1.1,
            'Salary Boost': 1.1, 'Skill Development': 1.0
        }
        base_score *= theme_multipliers.get(content_theme, 1.0)
        
        # Platform performance
        platform_multipliers = {
            'Instagram': 1.4, 'LinkedIn': 1.3, 'YouTube': 1.2,
            'Facebook': 1.1, 'Google Ads': 1.1, 'Twitter': 0.9
        }
        base_score *= platform_multipliers.get(platform, 1.0)
        
        # City performance (based on market data)
        city_multipliers = {
            'Hyderabad': 1.2, 'Bangalore': 1.15, 'Chennai': 1.1,
            'Delhi NCR': 1.05, 'Mumbai': 1.0, 'Pune': 0.95
        }
        base_score *= city_multipliers.get(target_city, 1.0)
        
        # Age group preferences
        age_multipliers = {'35-42': 1.1, '28-35': 1.1, '22-28': 1.0, '42-50': 0.9}
        base_score *= age_multipliers.get(age_group, 1.0)
        
        # Numerical feature impacts
        if readability_score > 8:
            base_score *= 1.1
        if brand_consistency_score > 9:
            base_score *= 1.15
        if accessibility_score > 9:
            base_score *= 1.05
        
        # Character count optimization (sweet spot around 150-200)
        if 150 <= character_count <= 200:
            base_score *= 1.1
        elif character_count < 100 or character_count > 250:
            base_score *= 0.9
        
        # Add some noise
        base_score += np.random.normal(0, 0.3)
        
        # Ensure score is within reasonable bounds
        return max(1.0, min(10.0, base_score))
    
    def train_model(self, training_data: pd.DataFrame) -> Dict[str, Any]:
        """Train the optimization model on campaign data"""
        
        if not SKLEARN_AVAILABLE:
            logger.error("Scikit-learn not available for model training")
            return {"error": "ML libraries not available"}
        
        try:
            # Prepare features and target
            features_df = self._prepare_features(training_data)
            target = training_data['performance_score']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features_df, target, test_size=0.2, random_state=42
            )
            
            # Scale numerical features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train the model
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            # Cross-validation
            cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
            
            # Feature importance
            feature_names = features_df.columns.tolist()
            self.feature_importance = dict(zip(feature_names, self.model.feature_importances_))
            
            # Mark as trained
            self.is_trained = True
            
            # Save model
            self._save_model()
            
            results = {
                "model_trained": True,
                "training_samples": len(training_data),
                "train_r2": round(train_score, 3),
                "test_r2": round(test_score, 3),
                "cv_mean": round(cv_scores.mean(), 3),
                "cv_std": round(cv_scores.std(), 3),
                "feature_importance": {k: round(v, 3) for k, v in self.feature_importance.items()}
            }
            
            logger.info(f"Model trained successfully: R² = {test_score:.3f}")
            return results
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return {"error": str(e)}
    
    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for ML model"""
        
        categorical_features = [
            'brand_id', 'content_theme', 'visual_style', 'target_emotion',
            'campaign_type', 'platform', 'target_city', 'target_age_group'
        ]
        
        numerical_features = [
            'character_count', 'readability_score', 
            'brand_consistency_score', 'accessibility_score'
        ]
        
        processed_df = df.copy()
        
        # Encode categorical features
        for feature in categorical_features:
            if feature in processed_df.columns:
                if feature not in self.encoders:
                    self.encoders[feature] = LabelEncoder()
                    processed_df[feature] = self.encoders[feature].fit_transform(
                        processed_df[feature].astype(str)
                    )
                else:
                    # Handle unseen categories
                    le = self.encoders[feature]
                    processed_df[feature] = processed_df[feature].astype(str)
                    
                    # Map unseen categories to a default value
                    mask = ~processed_df[feature].isin(le.classes_)
                    processed_df.loc[mask, feature] = le.classes_[0]  # Use first class as default
                    
                    processed_df[feature] = le.transform(processed_df[feature])
        
        # Select available features
        available_features = []
        for feature in categorical_features + numerical_features:
            if feature in processed_df.columns:
                available_features.append(feature)
        
        return processed_df[available_features]

    def predict_performance(self, campaign_params: Dict[str, Any]) -> Dict[str, Any]:
        """Predict campaign performance based on parameters"""

        if not self.is_trained:
            # Try to load pre-trained model
            if not self._load_model():
                return {"error": "Model not trained and no saved model available"}

        try:
            # Create feature vector from parameters
            feature_df = self._create_feature_dataframe(campaign_params)

            # Scale features
            features_scaled = self.scaler.transform(feature_df)

            # Predict performance
            predicted_score = self.model.predict(features_scaled)[0]

            # Convert to business metrics
            business_metrics = self._convert_to_business_metrics(predicted_score, campaign_params)

            # Calculate confidence
            confidence = self._calculate_prediction_confidence(feature_df)

            return {
                "predicted_performance_score": round(predicted_score, 2),
                "business_metrics": business_metrics,
                "confidence_level": round(confidence, 2),
                "feature_contributions": self._get_feature_contributions(feature_df),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error predicting performance: {e}")
            return {"error": f"Prediction failed: {str(e)}"}

    def _create_feature_dataframe(self, params: Dict[str, Any]) -> pd.DataFrame:
        """Create feature dataframe from campaign parameters"""

        # Default values for missing parameters
        defaults = {
            'brand_id': 'upgrad',
            'content_theme': 'Career Growth',
            'visual_style': 'Professional',
            'target_emotion': 'Motivation',
            'campaign_type': 'Email',
            'platform': 'LinkedIn',
            'target_city': 'Bangalore',
            'target_age_group': '28-35',
            'character_count': 150,
            'readability_score': 8.0,
            'brand_consistency_score': 9.0,
            'accessibility_score': 8.5
        }

        # Merge with defaults
        feature_data = {**defaults, **params}

        # Create dataframe
        df = pd.DataFrame([feature_data])

        # Prepare features using the same method as training
        return self._prepare_features(df)

    def _convert_to_business_metrics(self, performance_score: float, params: Dict[str, Any]) -> Dict[str, str]:
        """Convert performance score to business metrics"""

        # Base metrics
        base_ctr = 0.025
        base_conversion = 0.05
        base_roas = 3.2
        base_cost = 300

        # Performance multiplier (normalize score to 0.5-2.0 range)
        multiplier = 0.5 + (performance_score / 10.0) * 1.5

        # Platform adjustments
        platform = params.get('platform', 'LinkedIn')
        platform_adjustments = {
            'Instagram': {'ctr': 1.8, 'conversion': 1.7, 'roas': 1.5},
            'LinkedIn': {'ctr': 1.3, 'conversion': 1.2, 'roas': 1.3},
            'YouTube': {'ctr': 1.6, 'conversion': 1.4, 'roas': 1.4},
            'Facebook': {'ctr': 1.1, 'conversion': 1.0, 'roas': 1.1},
            'Google Ads': {'ctr': 1.5, 'conversion': 1.3, 'roas': 1.3},
            'Twitter': {'ctr': 0.7, 'conversion': 0.6, 'roas': 0.8}
        }

        platform_adj = platform_adjustments.get(platform, {'ctr': 1.0, 'conversion': 1.0, 'roas': 1.0})

        # Calculate final metrics
        final_ctr = base_ctr * multiplier * platform_adj['ctr']
        final_conversion = base_conversion * multiplier * platform_adj['conversion']
        final_roas = base_roas * multiplier * platform_adj['roas']
        final_cost = base_cost / multiplier

        return {
            'ctr': f"{final_ctr * 100:.1f}%",
            'conversion_rate': f"{final_conversion * 100:.1f}%",
            'roas': f"{final_roas:.1f}x",
            'cost_per_conversion': f"₹{int(final_cost)}"
        }

    def _calculate_prediction_confidence(self, feature_df: pd.DataFrame) -> float:
        """Calculate confidence level for the prediction"""

        if not SKLEARN_AVAILABLE or not hasattr(self.model, 'estimators_'):
            return 0.75  # Default confidence

        try:
            # Get predictions from all trees
            features_scaled = self.scaler.transform(feature_df)
            tree_predictions = [tree.predict(features_scaled)[0] for tree in self.model.estimators_]

            # Calculate variance
            prediction_variance = np.var(tree_predictions)

            # Convert variance to confidence (lower variance = higher confidence)
            confidence = max(0.5, min(0.95, 1.0 - (prediction_variance / 10.0)))

            return confidence

        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.75

    def _get_feature_contributions(self, feature_df: pd.DataFrame) -> Dict[str, float]:
        """Get feature contributions to the prediction"""

        if not self.feature_importance:
            return {}

        # Get feature values
        feature_values = feature_df.iloc[0].to_dict()

        # Calculate contributions based on feature importance and values
        contributions = {}
        for feature, importance in self.feature_importance.items():
            if feature in feature_values:
                # Normalize contribution
                contribution = importance * (feature_values[feature] / 10.0)  # Rough normalization
                contributions[feature] = round(contribution, 3)

        return contributions

    def optimize_campaign(self, base_params: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest optimizations for campaign parameters"""

        if not self.is_trained:
            return {"error": "Model not trained"}

        try:
            base_prediction = self.predict_performance(base_params)
            base_score = base_prediction.get('predicted_performance_score', 0)

            optimizations = []

            # Test different content themes
            for theme in ['Job Security', 'Career Growth', 'AI/ML Skills', 'Salary Boost']:
                test_params = base_params.copy()
                test_params['content_theme'] = theme
                prediction = self.predict_performance(test_params)

                optimizations.append({
                    'parameter': 'content_theme',
                    'value': theme,
                    'predicted_score': prediction.get('predicted_performance_score', 0),
                    'improvement': prediction.get('predicted_performance_score', 0) - base_score
                })

            # Test different platforms
            for platform in ['Instagram', 'LinkedIn', 'YouTube', 'Facebook']:
                test_params = base_params.copy()
                test_params['platform'] = platform
                prediction = self.predict_performance(test_params)

                optimizations.append({
                    'parameter': 'platform',
                    'value': platform,
                    'predicted_score': prediction.get('predicted_performance_score', 0),
                    'improvement': prediction.get('predicted_performance_score', 0) - base_score
                })

            # Sort by improvement
            optimizations.sort(key=lambda x: x['improvement'], reverse=True)

            # Get top improvements
            top_optimizations = [opt for opt in optimizations if opt['improvement'] > 0][:5]

            return {
                "base_score": base_score,
                "optimizations": top_optimizations,
                "max_improvement": max([opt['improvement'] for opt in top_optimizations]) if top_optimizations else 0,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error optimizing campaign: {e}")
            return {"error": f"Optimization failed: {str(e)}"}

    def _save_model(self):
        """Save trained model and encoders"""
        try:
            if SKLEARN_AVAILABLE and self.model is not None:
                model_path = self.data_path / "campaign_optimizer_model.pkl"
                encoders_path = self.data_path / "campaign_encoders.pkl"
                scaler_path = self.data_path / "campaign_scaler.pkl"

                joblib.dump(self.model, model_path)
                joblib.dump(self.encoders, encoders_path)
                joblib.dump(self.scaler, scaler_path)

                logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")

    def _load_model(self) -> bool:
        """Load pre-trained model and encoders"""
        try:
            model_path = self.data_path / "campaign_optimizer_model.pkl"
            encoders_path = self.data_path / "campaign_encoders.pkl"
            scaler_path = self.data_path / "campaign_scaler.pkl"

            if all(path.exists() for path in [model_path, encoders_path, scaler_path]):
                self.model = joblib.load(model_path)
                self.encoders = joblib.load(encoders_path)
                self.scaler = joblib.load(scaler_path)
                self.is_trained = True

                logger.info("Model loaded successfully")
                return True
            else:
                logger.warning("Saved model files not found")
                return False

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the trained model"""

        return {
            "is_trained": self.is_trained,
            "model_type": "RandomForestRegressor" if SKLEARN_AVAILABLE else "Not Available",
            "feature_importance": self.feature_importance,
            "sklearn_available": SKLEARN_AVAILABLE,
            "last_updated": datetime.now().isoformat()
        }

    def add_performance_feedback(self, campaign_params: Dict[str, Any], actual_performance: float):
        """Add actual performance feedback for continuous learning"""

        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "campaign_params": campaign_params,
            "actual_performance": actual_performance,
            "predicted_performance": self.predict_performance(campaign_params).get('predicted_performance_score')
        }

        self.performance_history.append(feedback_entry)

        # Save feedback for future retraining
        feedback_file = self.data_path / "performance_feedback.json"
        try:
            with open(feedback_file, 'w') as f:
                json.dump(self.performance_history, f, indent=2)

            logger.info("Performance feedback added")
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")

# Global instance
campaign_optimizer = CampaignOptimizer()
