import pytest
from datetime import datetime
from main import DataGenerator, User, Product, Order, session

@pytest.fixture
def generator():
    return DataGenerator()

def test_generate_user(generator):
    user = generator.generate_user()
    assert isinstance(user, User)
    assert user.name
    assert user.email
    assert user.address
    assert user.phone
    assert isinstance(user.birth_date, datetime)
    assert isinstance(user.is_active, bool)
    assert isinstance(user.created_at, datetime)

def test_generate_product(generator):
    product = generator.generate_product()
    assert isinstance(product, Product)
    assert product.name
    assert product.description
    assert isinstance(product.price, float)
    assert product.category
    assert isinstance(product.stock_quantity, int)
    assert isinstance(product.created_at, datetime)

def test_generate_order(generator):
    # First create a user and product
    user = generator.generate_user()
    product = generator.generate_product()
    session.add_all([user, product])
    session.commit()
    
    order = generator.generate_order(user.id, product.id)
    assert isinstance(order, Order)
    assert order.user_id == user.id
    assert order.product_id == product.id
    assert isinstance(order.quantity, int)
    assert isinstance(order.total_price, float)
    assert order.status in ['pending', 'completed', 'cancelled']
    assert isinstance(order.created_at, datetime)

def test_generate_data(generator):
    num_users = 5
    num_products = 10
    num_orders = 15
    
    generator.generate_data(num_users, num_products, num_orders)
    
    # Verify the number of records
    assert session.query(User).count() == num_users
    assert session.query(Product).count() == num_products
    assert session.query(Order).count() == num_orders

def test_export_data(generator):
    # Generate some test data
    generator.generate_data(2, 2, 2)
    
    # Test JSON export
    generator.export_data('json')
    with open('exported_data.json', 'r') as f:
        data = f.read()
        assert 'users' in data
        assert 'products' in data
        assert 'orders' in data
    
    # Test CSV export
    generator.export_data('csv')
    for table in ['users', 'products', 'orders']:
        with open(f'{table}.csv', 'r') as f:
            data = f.read()
            assert data
    
    # Test YAML export
    generator.export_data('yaml')
    with open('exported_data.yaml', 'r') as f:
        data = f.read()
        assert 'users' in data
        assert 'products' in data
        assert 'orders' in data 