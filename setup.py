from setuptools import setup, find_packages

setup(name='ideo_gcp_utils',
      version='0.0.1',
      description='Google Cloud API utils @ IDEO',
      url='https://github.com/ideo/ideo-gcp-utils',
      author='IDEO DS',
      license='MIT License',
      packages=find_packages(),
      install_requires=['google-cloud-storage', 'google-api-python-client'],
      zip_safe=False)