"""Setup pyiextract."""
from setuptools import setup, find_packages
from pathlib import Path
import typing

readme_path = Path(__file__).absolute().parent.joinpath('README.md')
long_description = readme_path.read_text(encoding='utf-8')


def install_requires() -> typing.List[str]:
    """Find the install requires strings from requirements.txt"""
    requires = []
    with open(
        Path(__file__).absolute().parent.joinpath('requirements.txt'), "r"
    ) as requirments_txt_handle:
        requires = [
            x
            for x in requirments_txt_handle
            if not x.startswith(".") and not x.startswith("-e") and not x.startswith("git+")
        ]
    return requires


setup(
    name='pyiextract',
    version='0.0.1',
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
    install_requires=install_requires() + [
        "opennre @ git+https://github.com/thunlp/OpenNRE@b8668d34db21672e7f2f952eab74843a96cd9b00#egg=opennre",
        "BLINK @ git+https://github.com/8W9aG/BLINK@5026de24c7e7e465955a04c17a799de5fb34866d#egg=BLINK"
    ],
    zip_safe=False,
    packages=find_packages()
)
