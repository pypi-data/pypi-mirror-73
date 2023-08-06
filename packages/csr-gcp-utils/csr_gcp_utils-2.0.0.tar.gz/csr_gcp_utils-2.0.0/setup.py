# from setuptools import setup
from distutils.core import setup
project_name = 'csr_gcp_utils'
project_ver = '2.0.0'
setup(
    name=project_name,
    packages=["csr_cloud"],  # this must be the same as the name above
    version=project_ver,
    description='Utilities for csr1000v on GCP',
    author='Avani Vyas',
    author_email='avvyas@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-gcp/' + project_name,
    download_url='https://github4-chn.cisco.com/csr1000v-gcp/' + project_name + '/archive/' + \
        project_ver + '.tar.gz',
    keywords=['cisco', 'gcp', 'guestshell', 'csr1000v'],
    install_requires=[
          'rsa==4.0',
          'httplib2==0.17.4',
          'oauth2client==4.1.3',
          'google-api-python-client==1.9.3',
          'ipaddress==1.0.23',
          'future==0.18.2'
      ],
    classifiers=[],
    license="MIT"
)
