from setuptools import setup, find_packages

setup(
    name='MautinoaGeo',
    version='1.0',
    packages=find_packages(),
    install_requires=['Flask','GeoAlchemy2','geopandas','SQLAlchemy'],
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
)
