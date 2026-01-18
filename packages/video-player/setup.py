from setuptools import setup, find_packages

setup(
    name="myframework-video-player",
    version="0.1.0",
    author="Rafael Dourado",
    author_email="your.email@example.com",
    description="React video player components with Mosaic support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rafaeldourado8/MyFramework",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[],
)
