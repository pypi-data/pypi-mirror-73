import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="modbus_config_tools",
    version="1.0.1",
    url="http://flask.pocoo.org/docs/tutorial/",
    license="BSD",
    maintainer="loop1905",
    maintainer_email="littlshenyun@outlook.com",
    description="modbus configure tools",
    packages=find_packages(),
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask","waitress","xlrd","flask_wtf"],
    extras_require={"test": ["pytest", "coverage"]},
)
