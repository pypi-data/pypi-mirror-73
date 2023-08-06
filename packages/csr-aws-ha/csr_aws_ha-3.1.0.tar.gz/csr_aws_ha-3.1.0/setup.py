from distutils.core import setup
from setuptools.command.install import install
from subprocess import check_call
import subprocess, sys

project_name = 'csr_aws_ha'
project_ver = '3.1.0'


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print ("Installing packages for ha")
        pip = "pip"
        py = sys.executable
        if "3"  in  py:
            pip = "pip3"
        check_call([pip, 'install', 'csr_aws_utils~=2.0', '--user', '--force', '--no-cache-dir'])
        check_call([pip, 'install', 'csr_ha~=2.0','--user', '--force', '--no-cache-dir'])
        install.run(self)


setup(
    name=project_name,
    version=project_ver,
    description='Package enabling HA functionality on AWS',
    author='Christopher Reder',
    author_email='creder@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-aws/csr_aws_ha',
    download_url='https://github4-chn.cisco.com/csr1000v-aws/csr_aws_ha',
    keywords=['cisco', 'aws', 'guestshell', 'csr1000v'],
    classifiers=[],
    license="MIT",
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
    }
)
