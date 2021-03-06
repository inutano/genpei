#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
from typing import List

from setuptools import setup

BASE_DIR: Path = Path(__file__).parent.resolve()
REQUIREMNTS_TEXT: Path = BASE_DIR.joinpath("requirements.txt")


def read_requirements_txt() -> List[str]:
    with REQUIREMNTS_TEXT.open(mode="r") as f:
        packages: List[str] = \
            [str(line) for line in f.read().splitlines() if line != ""]

    return packages


def main() -> None:
    setup(name="genpei",
          version="1.0.1",
          description="Implementation of GA4GH WES OpenAPI specification " +
                      "using cwltool.",
          author="suecharo",
          author_email="suehiro619@gmail.com",
          url="https://github.com/suecharo/genpei",
          license="Apache2.0",
          python_requires=">=3.6",
          platforms="any",
          include_package_data=True,
          zip_safe=False,
          classifiers=["Programming Language :: Python"],
          packages=["genpei"],
          install_requires=read_requirements_txt(),
          entry_points={
              "console_scripts": [
                  "genpei=genpei.app:main",
              ]
          }
          )


if __name__ == "__main__":
    main()
