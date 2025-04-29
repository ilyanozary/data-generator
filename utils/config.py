import os
import yaml
from typing import Dict, Any

class Config:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self.load_config()

    @classmethod
    def load_config(cls, config_path: str = 'config.yaml'):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                cls._config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing configuration file: {e}")

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = cls._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    @classmethod
    def get_database_path(cls) -> str:
        """Get database path from configuration"""
        db_path = cls.get('database.path')
        if not os.path.isabs(db_path):
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_path)
        return db_path

    @classmethod
    def get_export_directory(cls) -> str:
        """Get export directory from configuration"""
        export_dir = cls.get('export.output_directory')
        if not os.path.isabs(export_dir):
            export_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), export_dir)
        os.makedirs(export_dir, exist_ok=True)
        return export_dir

    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """Get logging configuration"""
        return {
            'level': cls.get('logging.level'),
            'file': cls.get('logging.file'),
            'format': cls.get('logging.format')
        }

    @classmethod
    def get_validation_config(cls) -> Dict[str, Any]:
        """Get validation configuration"""
        return {
            'email_domains': cls.get('validation.email_domains', []),
            'phone_formats': cls.get('validation.phone_formats', {}),
            'min_age': cls.get('validation.min_age', 18),
            'max_age': cls.get('validation.max_age', 100)
        } 