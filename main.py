import os
import logging
import argparse
from typing import List, Dict, Any
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
import json
import csv
import yaml
from ml_generator import MLDataGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Faker with multiple locales
fake = Faker(['en_US', 'fa_IR'])

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'sample_data.db')
engine = create_engine(f'sqlite:///{db_path}')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address = Column(String)
    phone = Column(String)
    birth_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category = Column(String)
    stock_quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class DataGenerator:
    def __init__(self, locale: str = 'en_US', use_ml: bool = False):
        self.fake = Faker(locale)
        self.session = Session()
        self.use_ml = use_ml
        if use_ml:
            self.ml_generator = MLDataGenerator()
            # Train ML models with existing data if available
            self._train_ml_models()

    def _train_ml_models(self):
        """Train ML models with existing data"""
        try:
            # Get historical data
            users = [user.__dict__ for user in self.session.query(User).all()]
            if users:
                self.ml_generator.train_user_pattern_model(users)
                logger.info("ML models trained successfully")
        except Exception as e:
            logger.error(f"Error training ML models: {str(e)}")

    def generate_user(self) -> User:
        base_user = User(
            name=self.fake.name(),
            email=self.fake.email(),
            address=self.fake.address().replace('\n', ', '),
            phone=self.fake.phone_number(),
            birth_date=self.fake.date_of_birth(),
            is_active=self.fake.boolean(),
            created_at=datetime.now(timezone.utc)
        )
        
        if self.use_ml and hasattr(self, 'ml_generator'):
            try:
                enhanced_user = self.ml_generator.generate_smart_user(base_user.__dict__)
                return User(**enhanced_user)
            except Exception as e:
                logger.error(f"Error generating smart user: {str(e)}")
                return base_user
        return base_user

    def generate_product(self) -> Product:
        return Product(
            name=self.fake.word(),
            description=self.fake.text(),
            price=self.fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            category=self.fake.word(),
            stock_quantity=self.fake.random_int(min=0, max=1000),
            created_at=datetime.now(timezone.utc)
        )

    def generate_order(self, user_id: int, product_id: int) -> Order:
        quantity = self.fake.random_int(min=1, max=10)
        price = self.session.query(Product).filter_by(id=product_id).first().price
        return Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=quantity * price,
            status=self.fake.random_element(elements=('pending', 'completed', 'cancelled')),
            created_at=datetime.now(timezone.utc)
        )

    def generate_data(self, num_users: int = 10, num_products: int = 20, num_orders: int = 50):
        logger.info(f"Generating {num_users} users, {num_products} products, and {num_orders} orders")
        
        # Generate users
        users = [self.generate_user() for _ in range(num_users)]
        self.session.add_all(users)
        self.session.commit()
        logger.info(f"Generated {len(users)} users")

        # Generate products
        products = [self.generate_product() for _ in range(num_products)]
        self.session.add_all(products)
        self.session.commit()
        logger.info(f"Generated {len(products)} products")

        # Generate orders
        orders = []
        for _ in range(num_orders):
            user_id = self.fake.random_element(elements=[u.id for u in users])
            product_id = self.fake.random_element(elements=[p.id for p in products])
            orders.append(self.generate_order(user_id, product_id))
        
        self.session.add_all(orders)
        self.session.commit()
        logger.info(f"Generated {len(orders)} orders")

    def export_data(self, format: str = 'json'):
        """Export data to various formats"""
        data = {
            'users': [user.__dict__ for user in self.session.query(User).all()],
            'products': [product.__dict__ for product in self.session.query(Product).all()],
            'orders': [order.__dict__ for order in self.session.query(Order).all()]
        }

        if format == 'json':
            with open('exported_data.json', 'w') as f:
                json.dump(data, f, default=str)
        elif format == 'csv':
            for table_name, records in data.items():
                with open(f'{table_name}.csv', 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=records[0].keys())
                    writer.writeheader()
                    writer.writerows(records)
        elif format == 'yaml':
            with open('exported_data.yaml', 'w') as f:
                yaml.dump(data, f, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(description='Advanced Data Generator')
    parser.add_argument('--users', type=int, default=10, help='Number of users to generate')
    parser.add_argument('--products', type=int, default=20, help='Number of products to generate')
    parser.add_argument('--orders', type=int, default=50, help='Number of orders to generate')
    parser.add_argument('--locale', type=str, default='en_US', help='Locale for data generation')
    parser.add_argument('--export', type=str, choices=['json', 'csv', 'yaml'], help='Export format')
    parser.add_argument('--use-ml', action='store_true', help='Use ML-enhanced data generation')
    
    args = parser.parse_args()
    
    generator = DataGenerator(locale=args.locale, use_ml=args.use_ml)
    generator.generate_data(args.users, args.products, args.orders)
    
    if args.export:
        generator.export_data(args.export)
        logger.info(f"Data exported to {args.export} format")

if __name__ == '__main__':
    main() 