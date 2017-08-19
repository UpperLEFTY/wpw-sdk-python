from setuptools import setup, find_packages

setup(
    name="wpwithinpy",
    version="0.1",
    packages=['wpwithinpy'],
    install_requires=[
        'thrift'
    ],
    include_package_data=True
)
