from setuptools import setup, find_packages


setup(
    name='netbox_file_upload',
    version='0.1',
    description='A file upload plugin for Netbox',
    author='Seam Collins',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    package_data={'mypackages': ['templates/*.html']},
    include_package_data=True,
)

