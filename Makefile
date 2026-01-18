.PHONY: build clean install publish-test publish

build:
	cd packages/core && python setup.py sdist bdist_wheel
	cd packages/auth && python setup.py sdist bdist_wheel
	cd packages/rbac && python setup.py sdist bdist_wheel
	cd packages/observability && python setup.py sdist bdist_wheel
	cd packages/video-streaming && python setup.py sdist bdist_wheel
	cd packages/video-processing && python setup.py sdist bdist_wheel
	cd packages/camera-management && python setup.py sdist bdist_wheel
	cd packages/video-workers && python setup.py sdist bdist_wheel
	cd packages/video-player && python setup.py sdist bdist_wheel

clean:
	for /d /r . %%d in (build) do @if exist "%%d" rd /s /q "%%d"
	for /d /r . %%d in (dist) do @if exist "%%d" rd /s /q "%%d"
	for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
	for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

install:
	pip install -e packages/core
	pip install -e packages/auth
	pip install -e packages/rbac
	pip install -e packages/observability
	pip install -e packages/video-streaming
	pip install -e packages/video-processing
	pip install -e packages/camera-management
	pip install -e packages/video-workers
	pip install -e packages/video-player

publish-test: clean build
	twine upload --repository testpypi packages/*/dist/*

publish: clean build
	twine upload packages/*/dist/*
