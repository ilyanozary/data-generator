# Advanced Data Generator

A powerful and flexible data generation tool that creates realistic test data for various use cases. This tool supports multiple data models, export formats, and locales.


## Features

- Generate realistic test data for users, products, and orders
- Support for multiple locales (English and Persian)
- Multiple export formats (JSON, CSV, YAML)
- SQLite database storage
- Comprehensive logging
- Command-line interface
- Type hints and documentation

## Installation

1. Clone the repository:```bash
git clone https://github.com/yourusername/data-generator.git
cd data-generator
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python main.py
```

Generate specific number of records:
```bash
python main.py --users 100 --products 50 --orders 200
```

Generate data with Persian locale:
```bash
python main.py --locale fa_IR
```

Export data to different formats:
```bash
python main.py --export json
python main.py --export csv
python main.py --export yaml
```

## Data Models

### User
- name
- email
- address
- phone
- birth_date
- is_active
- created_at

### Product
- name
- description
- price
- category
- stock_quantity
- created_at

### Order
- user_id
- product_id
- quantity
- total_price
- status
- created_at

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Faker](https://faker.readthedocs.io/) for realistic data generation
- [SQLAlchemy](https://www.sqlalchemy.org/) for database operations 
