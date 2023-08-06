#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup  # type: ignore


def read(fname):
    # type: (str) -> str
    with open(os.path.join(os.path.dirname(__file__), fname), "rb") as fid:
        return fid.read().decode("utf-8")


ENTRYPOINT = "pandocfilters_sh.__main__:main"

setup(
    name="pandocfilter-sh",
    version="0.1",
    description="Pandocfilters wrapper project to install as a script",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    url="https://github.com/miki725/pandocfilters-sh",
    license="MIT",
    packages=find_packages(),
    install_requires=["pandocfilters"],
    entry_points={
        "console_scripts": [f"pandocfilters.sh = {ENTRYPOINT}"],
    },
    keywords=" ".join(["pandoc", "pandocfilters"]),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
    ],
)
