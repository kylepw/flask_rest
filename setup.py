from setuptools import setup

setup(
    name='flask_rest',
    packages=['flask_rest'],
    include_package_data=True,
    install_requires=[
        'Flask-PyMongo',
    ],
)