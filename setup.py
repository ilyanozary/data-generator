from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="advanced-data-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "faker==19.13.0",
        "sqlalchemy==2.0.25",
        "pandas==2.1.4",
        "streamlit==1.29.0",
        "plotly==5.18.0",
        "pyyaml==6.0.1",
        "python-dateutil==2.8.2",
        "pytest>=7.4.0",
        "black>=23.7.0",
        "flake8>=6.1.0",
        "python-dotenv>=1.0.0"
    ],
    author="ilyanozary",
    author_email="ilyanozary.dynamic@gmail.com",
    description="Advanced Data Generator - A powerful tool for generating realistic test data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilyanozary/advanced-data-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "data-generator=main:main",
        ],
    },
) 


