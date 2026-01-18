from setuptools import setup, find_packages

setup(
    name="rbac-package",
    version="1.0.0",
    description="Role-Based Access Control package",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.104.0",
    ],
)
