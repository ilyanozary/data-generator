import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import joblib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MLDataGenerator:
    def __init__(self):
        self.models = {}
        self.label_encoders = {}
        
    def train_user_pattern_model(self, historical_data):
        """Train a model to generate realistic user patterns"""
        try:
            # Convert data to DataFrame
            df = pd.DataFrame(historical_data)
            
            # Convert datetime fields to timestamps
            if 'birth_date' in df.columns:
                df['birth_date'] = pd.to_datetime(df['birth_date']).astype(np.int64)
            
            # Encode categorical features
            for col in ['name', 'email', 'address', 'phone']:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col])
            
            # Prepare features and target
            X = df.drop(['id', 'created_at'], axis=1)
            y = df['is_active']
            
            # Train model
            model = RandomForestRegressor()
            model.fit(X, y)
            
            self.models['user_pattern'] = model
            logger.info("User pattern model trained successfully")
            return True
        except Exception as e:
            logger.error(f"Error training user pattern model: {str(e)}")
            return False
            
    def generate_smart_user(self, base_features):
        """Generate a user with ML-enhanced features"""
        try:
            if 'user_pattern' not in self.models:
                raise ValueError("User pattern model not trained")
                
            # Prepare features
            features = pd.DataFrame([base_features])
            
            # Convert datetime fields to timestamps
            if 'birth_date' in features.columns:
                features['birth_date'] = pd.to_datetime(features['birth_date']).astype(np.int64)
            
            # Encode categorical features
            for col, encoder in self.label_encoders.items():
                if col in features.columns:
                    features[col] = encoder.transform(features[col])
            
            # Drop unnecessary columns
            features = features.drop(['id', 'created_at'], axis=1, errors='ignore')
            
            # Generate enhanced features
            enhanced_features = self.models['user_pattern'].predict(features)
            
            return {
                **base_features,
                'is_active': bool(enhanced_features[0] > 0.5)
            }
        except Exception as e:
            logger.error(f"Error generating smart user: {str(e)}")
            return base_features
            
    def train_sequence_model(self, historical_data):
        """Train a model to generate sequential data patterns"""
        try:
            # Convert data to sequence format
            sequences = self._prepare_sequences(historical_data)
            
            # Create and train LSTM model
            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(sequences.shape[1], sequences.shape[2])),
                LSTM(50),
                Dense(1)
            ])
            
            model.compile(optimizer='adam', loss='mse')
            model.fit(sequences, epochs=10, batch_size=32)
            
            self.models['sequence'] = model
            logger.info("Sequence model trained successfully")
            return True
        except Exception as e:
            logger.error(f"Error training sequence model: {str(e)}")
            return False
            
    def _prepare_sequences(self, data):
        """Prepare data for sequence model"""
        # Implementation for sequence preparation
        pass
        
    def save_models(self, path):
        """Save trained models to disk"""
        try:
            joblib.dump(self.models, f"{path}/models.joblib")
            joblib.dump(self.label_encoders, f"{path}/encoders.joblib")
            logger.info("Models saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving models: {str(e)}")
            return False
            
    def load_models(self, path):
        """Load trained models from disk"""
        try:
            self.models = joblib.load(f"{path}/models.joblib")
            self.label_encoders = joblib.load(f"{path}/encoders.joblib")
            logger.info("Models loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            return False 


            