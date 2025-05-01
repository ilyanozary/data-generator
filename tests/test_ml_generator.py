import pytest
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_generator import MLDataGenerator
from main import User, session, Base, engine

@pytest.fixture(autouse=True)
def setup_database():
    # Create all tables
    Base.metadata.create_all(engine)
    # Clean up the database before each test
    session.query(User).delete()
    session.commit()
    yield
    # Clean up after each test
    session.query(User).delete()
    session.commit()

@pytest.fixture
def ml_generator():
    return MLDataGenerator()

def test_train_user_pattern_model(ml_generator):
    # Create some test users
    test_users = [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'phone': '1234567890',
            'birth_date': datetime(1990, 1, 1),
            'is_active': True,
            'created_at': datetime.now()
        },
        {
            'id': 2,
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'address': '456 Oak Ave',
            'phone': '0987654321',
            'birth_date': datetime(1995, 2, 2),
            'is_active': False,
            'created_at': datetime.now()
        }
    ]
    
    # Train the model
    result = ml_generator.train_user_pattern_model(test_users)
    assert result is True
    assert 'user_pattern' in ml_generator.models

def test_generate_smart_user(ml_generator):
    # First train the model
    test_users = [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'phone': '1234567890',
            'birth_date': datetime(1990, 1, 1),
            'is_active': True,
            'created_at': datetime.now()
        }
    ]
    ml_generator.train_user_pattern_model(test_users)
    
    # Generate a smart user
    base_features = {
        'id': 2,
        'name': 'Test User',
        'email': 'test@example.com',
        'address': '789 Test St',
        'phone': '5555555555',
        'birth_date': datetime(2000, 1, 1),
        'is_active': False,
        'created_at': datetime.now()
    }
    
    enhanced_user = ml_generator.generate_smart_user(base_features)
    assert isinstance(enhanced_user, dict)
    assert 'is_active' in enhanced_user
    assert isinstance(enhanced_user['is_active'], bool)

def test_save_load_models(ml_generator, tmp_path):
    # Train a model first
    test_users = [
        {
            'id': 1,
            'name': 'John Doe',
            'email': 'john@example.com',
            'address': '123 Main St',
            'phone': '1234567890',
            'birth_date': datetime(1990, 1, 1),
            'is_active': True,
            'created_at': datetime.now()
        }
    ]
    ml_generator.train_user_pattern_model(test_users)
    
    # Save models
    save_result = ml_generator.save_models(tmp_path)
    assert save_result is True
    
    # Create a new generator and load models
    new_generator = MLDataGenerator()
    load_result = new_generator.load_models(tmp_path)
    assert load_result is True
    assert 'user_pattern' in new_generator.models 