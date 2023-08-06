### SE4AI Group 4 Common Utils

#### Dependencies
Python packages to build: `setuptools` and `wheel`  
Python packages to deploy: `twine`  
To install: `python3 -m pip install --upgrade setuptools wheel twine`

#### Building & deploy the package
1. `python3 setup.py sdist bdist_wheel`
2. `python3 -m twine upload dist/*`