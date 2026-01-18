from setuptools import setup, find_packages

setup(
    name="video-streaming",
    version="1.0.0",
    description="Video streaming with MediaMTX and FFmpeg",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "httpx>=0.25.0",
    ],
)
