import os
import setuptools
from atmo_logger.version import get_version

with open("README.md") as f:
    readme = f.read()

long_description = """
atmo_logger %s
Logging for Atmosphere, modeled after jmatt's threepio.
To install use pip install git+git://github.com/cyverse/atmo_logger
----
%s
----
For more information, please see: https://github.com/cyverse/atmo_logger
""" % (get_version('short'), readme)

setuptools.setup(
    name='atmo_logger',
    version=get_version('short'),
    author='cyverse',
    author_email='atmodevs@gmail.com',
    description="Logging for Atmosphere, modeled after threepio by jmatt.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="The University of Arizona",
    url="https://github.com/cyverse/atmo_logger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Logging"
    ])
