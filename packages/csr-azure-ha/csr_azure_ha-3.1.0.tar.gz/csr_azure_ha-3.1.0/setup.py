from distutils.core import setup
from setuptools.command.install import install
from subprocess import check_call
import subprocess, sys

project_name = 'csr_azure_ha'
project_ver = '3.1.0'

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print ("Installing packages for ha")
        pip = "pip"
        py = sys.executable
        if "3"  in  py:
            pip = "pip3"
        subprocess.call([pip, 'install', 'csr_azure_utils~=2.0', '--user', '--force', '--no-cache-dir'])
        subprocess.call([pip, 'install', 'csr_ha~=2.0','--user', '--force', '--no-cache-dir'])
        install.run(self)

setup(
    name=project_name,
    version=project_ver,
    description='Package for the high availability (HA) on Azure',
    author='Cisco Systems Inc.',
    author_email='csr-cloud-dev@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-azure/csr_azure_ha',
    download_url='https://github4-chn.cisco.com/csr1000v-azure/csr_azure_ha',
    keywords=['cisco', 'azure', 'ha', 'high availability', 'csr1000v'],
    classifiers=[],
    license="MIT",
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
    }
)
