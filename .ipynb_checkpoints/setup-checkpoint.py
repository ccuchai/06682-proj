"""Setup file for package"""

from setuptools import setup

setup(
    name="s23openalex",
    version="0.0.1",
    description="s23openalex package",
    maintainer="Tricia Chang",
    maintainer_email="tsuiyunc@andrew.cmu.edu",
    license="GPL",
    packages=["s23openalex"],
    entry_points={"console_scripts": ["oaa = s23openalex.main:main"]},
    scripts=[],
    long_description="""\
Handy functions for a project.""",
)
