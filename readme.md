# Requirements
CKAN version 2.5.2

CKAN gSTAR Data Portal Theme


# Setup Steps

1. Clone the repository.

2. In the `settings` directory create a file named `local.py`. In the `local.py` define the following settings to override them.
```python
CKAN_HOST = 'http://my-ckan-app.com'

CKAN_USERNAME = 'my-ckan-username'
CKAN_PASSWORD = 'my-ckan-password'
```

3. Once the correct configuration in place, install the requirements:

```python
pip install -r requirements.txt
```

# Usage

```python
python bulkupload.py <dataset_id> </directory/path>
```
