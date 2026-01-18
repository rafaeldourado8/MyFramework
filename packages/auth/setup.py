from setuptools import setup, find_packages

setup(
    name="auth-package",
    version="1.0.0",
    description="Authentication package with JWT and password hashing",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "passlib[bcrypt]>=1.7.4",
        "python-jose[cryptography]>=3.3.0",
        "fastapi>=0.104.0",
    ],
)
