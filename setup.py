"""Setup pyiextract."""
from setuptools import setup, find_packages
from pathlib import Path
import typing
import os
import platform

import pip


readme_path = Path(__file__).absolute().parent.joinpath('README.md')
long_description = readme_path.read_text(encoding='utf-8')


if platform.system() == "Darwin":
    # Necessary for arm64 mac m1
    if "CLFAGS" in os.environ:
        os.environ["CFLAGS"] += " -Wno-implicit-function-declaration"
    else:
        os.environ["CFLAGS"] = "-Wno-implicit-function-declaration"
    os.environ["OPENBLAS"] = "$(brew --prefix openblas)"


def install_requires() -> typing.List[str]:
    """Find the install requires strings from requirements.txt"""
    requires = []
    with open(
        Path(__file__).absolute().parent.joinpath('requirements.txt'), "r"
    ) as requirments_txt_handle:
        for requires_line in requirments_txt_handle:
            if requires_line.startswith("-e") or requires_line.startswith("https://"):
                requires_components = requires_line.split()
                if pip.main(["install"] + requires_components) != 0:
                    raise Exception(f"Failed to install {requires_line}")
                continue
            requires.append(requires_line)
    return requires


setup(
    name='pyiextract',
    version='0.0.3',
    description='A library for end to end information extraction from raw text.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='information extraction nlp',
    url='https://github.com/8W9aG/pyiextract',
    author='Will Sackfield',
    author_email='will.sackfield@gmail.com',
    license='MIT',
    install_requires=install_requires(),
    zip_safe=False,
    packages=find_packages()
)
