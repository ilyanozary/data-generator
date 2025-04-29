import re
from datetime import datetime, date
from typing import Optional, Dict, Any
from .config import Config

class Validator:
    def __init__(self):
        self.config = Config()
        self.validation_config = self.config.get_validation_config()

    def validate_email(self, email: str) -> bool:
        """Validate email format and domain"""
        if not email:
            return False
        
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False
        
        # Domain validation
        domain = email.split('@')[1]
        return domain in self.validation_config['email_domains']

    def validate_phone(self, phone: str, locale: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return False
        
        phone_format = self.validation_config['phone_formats'].get(locale)
        if not phone_format:
            return True  # Skip validation if no format specified for locale
        
        # Convert format to regex pattern
        pattern = phone_format.replace('#', r'\d')
        return bool(re.match(f'^{pattern}$', phone))

    def validate_age(self, birth_date: date) -> bool:
        """Validate age is within configured range"""
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return self.validation_config['min_age'] <= age <= self.validation_config['max_age']

    def validate_user(self, user_data: Dict[str, Any], locale: str) -> Dict[str, Any]:
        """Validate user data"""
        errors = []
        
        if not self.validate_email(user_data.get('email', '')):
            errors.append('Invalid email format or domain')
        
        if not self.validate_phone(user_data.get('phone', ''), locale):
            errors.append('Invalid phone number format')
        
        if not self.validate_age(user_data.get('birth_date', date.today())):
            errors.append('Age is outside valid range')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def validate_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate product data"""
        errors = []
        
        if not product_data.get('name'):
            errors.append('Product name is required')
        
        if not isinstance(product_data.get('price'), (int, float)) or product_data.get('price') <= 0:
            errors.append('Invalid price')
        
        if not isinstance(product_data.get('stock_quantity'), int) or product_data.get('stock_quantity') < 0:
            errors.append('Invalid stock quantity')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    def validate_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate order data"""
        errors = []
        
        if not order_data.get('user_id'):
            errors.append('User ID is required')
        
        if not order_data.get('product_id'):
            errors.append('Product ID is required')
        
        if not isinstance(order_data.get('quantity'), int) or order_data.get('quantity') <= 0:
            errors.append('Invalid quantity')
        
        if not isinstance(order_data.get('total_price'), (int, float)) or order_data.get('total_price') <= 0:
            errors.append('Invalid total price')
        
        if order_data.get('status') not in ['pending', 'completed', 'cancelled']:
            errors.append('Invalid status')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        } 