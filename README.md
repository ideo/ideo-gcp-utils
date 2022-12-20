# IDEO Google Cloud Utilities

A IDEO maintained package for interfacing the Google Cloud Storage and Compute Engine tools through Python.

## Description

The package is based on existing methods from the ```google-cloud-storage``` and ```google-api-python-client``` libraries,
organized in common workflows for loading and saving data files (storage), and creating, deleting, starting and stopping 
VM instances on the Compute Engine, based on examples found in [this repo](https://github.com/alfonsof/google-cloud-python-examples/tree/master/gcloudcomputeengine).

## Installation

The `setup.py` file is manually maintained. This reposity can be installed as an editable package into other projects, via ssh, with:
```bash
pipenv install -e git+ssh://git@github.com/ideo/ideo-gcp-utils.git#egg=ideo_gcp_utils
```

## Usage
To use the library, you need to first locally create or download your GCP credentials. One option is to install the [Google Could CLI](https://cloud.google.com/sdk/docs/install) and follow the [instructions](https://cloud.google.com/sdk/docs/authorizing) for authorizing. Another option is or manually download the `credentials.json` file from the Google Cloud Console and store the path to that file in the ```GOOGLE_APPLICATION_CREDENTIALS``` environment variable. 

### Google Cloud Storage methods

* Initialize a bucket instance
```python
from ideo_gcp_utils import Bucket
bucket = Bucket(bucket_name = "your_bucket_name")
```

List files in bucket
```python
bucket.list_bucket_objects()
```

Download a file from Google Cloud Storage:
```python
bucket.download_file(filename, local_directory_for_download)
```

Upload a file to Google Cloud Storage:
```python
bucket.upload(filename, local_directory_of_file)
```

### Google Cloud Compute Engine methods

Initialize a ComputeEngine instance by providing the project name and zone:
```python
from ideo_gcp_utils import ComputeEngine
ce = ComputeEngine(project='YOUR_PROJECT_NAME', zone='ZONE_NAME')
```
Optionally, you can also provide the ```image_family```, ```image_project```, ```instance_type``` and ```instance_name``` here. The first three keywords are only necessary if you'll be using this API to create and instance, while the ```instance_name``` is needed for all other methods, but can also be provided in the call to each method.

List all available instances
```python
ce.list_instances()
```

Start an instance
```python
ce.start_instance(instance_name='your_instance_name')
```

Stop an instance
```python
ce.stop_instance(instance_name='your_instance_name')
```

## Development

This project is developed in python 3.10 and uses `pipenv` to manage dependencies. To install the dependencies, run
```bash
pipenv install
```
