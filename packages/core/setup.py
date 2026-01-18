from setuptools import setup, find_packages

setup(
    name="core-framework",
    version="1.0.0",
    description="Opiniated DDD framework with SOLID principles",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
    ],
)
