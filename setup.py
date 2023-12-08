"""Automated course registration (for University of Louisiana - Lafayette).
"""

import os
from setuptools import find_packages, setup

setup(
    name =              "advisobot",
    version =           "1.0.0",
    author =            "Gabriel C. Trahan",
    author_email =      "gabriel.trahan1@louisiana.edu",
    description =       (
                        "Automated course registration (for University of Louisiana - Lafayette)."
                        ),
    license =           "MIT",
    url =               "https://github.com/theokoles7/Advisobot",
    long_description =  open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    packages =          find_packages()
)