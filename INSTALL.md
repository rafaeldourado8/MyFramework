# Installation Guide

## For Users (Install as Library)

Install packages individually via pip:

```bash
# Core framework (required)
pip install myframework-core

# Authentication
pip install myframework-auth

# RBAC
pip install myframework-rbac

# Observability
pip install myframework-observability

# Video packages
pip install myframework-video-streaming
pip install myframework-video-processing
pip install myframework-camera-management
pip install myframework-video-workers

# React components (frontend)
npm install myframework-video-player
```

Or install all at once:

```bash
pip install myframework-core myframework-auth myframework-rbac myframework-observability myframework-video-streaming myframework-video-processing myframework-camera-management myframework-video-workers
```

## For Developers (Local Development)

Clone and install in editable mode:

```bash
git clone https://github.com/rafaeldourado8/MyFramework.git
cd MyFramework
make install
```

## Build Packages

```bash
# Install build tools
pip install build twine

# Build all packages
make build

# Clean build artifacts
make clean
```

## Publish to PyPI

```bash
# Test on TestPyPI first
make publish-test

# Publish to production PyPI
make publish
```

## Usage Example

```python
# Users only import, never see internal code
from myframework.core.domain import Entity, ValueObject
from myframework.auth import JWTService, Password
from myframework.rbac import RBACService, require_permission

# Framework code is installed in site-packages
# Users cannot accidentally modify it
```

## Benefits

✅ Users install via pip (like FastAPI, Django)  
✅ Code is in site-packages, not visible in project  
✅ Prevents accidental modifications  
✅ Easy updates with `pip install --upgrade`  
✅ Version control and dependency management  
✅ Professional distribution like any Python library
