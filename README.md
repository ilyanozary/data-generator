# 🚀 Advanced Data Generator

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
  <img src="https://img.shields.io/badge/Version-1.0.0-orange.svg" alt="Version">
</div>

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Web Interface](#web-interface)
- [Data Models](#data-models)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

Advanced Data Generator is a powerful, production-ready tool for generating realistic test data. It's designed to help developers, testers, and data scientists create high-quality synthetic data for various applications.

### Key Benefits
- 🎯 Generate realistic, consistent test data
- 🌍 Support for multiple languages and locales
- 📊 Rich data visualization capabilities
- 🔄 Multiple export formats
- 🚀 High performance and scalability
- 🔒 Data validation and integrity checks

## ✨ Features

### Core Features
- **Multi-Model Data Generation**
  - User profiles with realistic attributes
  - Product catalogs with detailed information
  - Order management with relationships
  - Custom data generation rules

- **Internationalization**
  - English (en_US) support
  - Persian (fa_IR) support
  - Extensible locale system

- **Data Export**
  - JSON format
  - CSV format
  - YAML format
  - Custom export configurations

- **Data Validation**
  - Email format validation
  - Phone number validation
  - Age verification
  - Data integrity checks

### Advanced Features
- **REST API**
  - Swagger documentation
  - Rate limiting
  - Authentication support
  - Error handling

- **Web Interface**
  - Interactive dashboard
  - Real-time data visualization
  - Data filtering and sorting
  - Export management

- **Containerization**
  - Docker support
  - Docker Compose orchestration
  - Environment isolation
  - Easy deployment

## 🛠 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/data-generator.git
cd data-generator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Installation
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📖 Usage

### Command Line Interface
```bash
# Generate data with default settings
python main.py

# Generate specific number of records
python main.py --users 100 --products 50 --orders 200

# Generate data with Persian locale
python main.py --locale fa_IR

# Export data to different formats
python main.py --export json
```

### API Usage
```bash
# Start the API server
uvicorn api:app --reload

# Access the API documentation
# Open http://localhost:8000/docs in your browser
```

### Web Interface
```bash
# Start the web interface
streamlit run web_interface.py

# Access the web interface
# Open http://localhost:8501 in your browser
```

## 📚 API Documentation

The API documentation is available at `http://localhost:8000/docs` when the server is running.

### Available Endpoints
- `POST /generate` - Generate new data
- `POST /export` - Export data
- `GET /users` - Retrieve users
- `GET /products` - Retrieve products
- `GET /orders` - Retrieve orders

## 🖥 Web Interface

The web interface provides:
- Interactive data generation
- Real-time data visualization
- Data filtering and sorting
- Export management
- Statistical analysis

## 📊 Data Models

### User Model
```python
class User:
    id: int
    name: str
    email: str
    address: str
    phone: str
    birth_date: datetime
    is_active: bool
    created_at: datetime
```

### Product Model
```python
class Product:
    id: int
    name: str
    description: str
    price: float
    category: str
    stock_quantity: int
    created_at: datetime
```

### Order Model
```python
class Order:
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime
```

## 🛠 Development

### Setting Up Development Environment
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_data_generator.py

# Run with coverage
pytest --cov=.
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings
- Add tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Faker](https://faker.readthedocs.io/) for realistic data generation
- [SQLAlchemy](https://www.sqlalchemy.org/) for database operations
- [FastAPI](https://fastapi.tiangolo.com/) for the REST API
- [Streamlit](https://streamlit.io/) for the web interface

## 📞 Support

For support, please:
1. Check the [documentation](docs/)
2. Open an [issue](https://github.com/yourusername/data-generator/issues)
3. Contact the maintainers

---

<div align="center">
  <p>Made with ❤️ by Your Name</p>
  <p>© 2024 Advanced Data Generator</p>
</div>
