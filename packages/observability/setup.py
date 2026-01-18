from setuptools import setup, find_packages

setup(
    name="observability-package",
    version="1.0.0",
    description="Observability package with metrics and logging",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "prometheus-client>=0.19.0",
        "fastapi>=0.104.0",
    ],
)
