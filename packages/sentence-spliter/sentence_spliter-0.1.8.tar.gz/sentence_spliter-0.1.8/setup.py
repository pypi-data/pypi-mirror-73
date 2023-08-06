from setuptools import setup,find_packages
import os
def read_file(filename):
    # print(os.path.join(os.path.dirname(__file__), filename))
	return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name = "sentence_spliter",
    version = "0.1.8",
    long_description_content_type='text/markdown',
    description = "This is a sentence cutting tool that supports long sentence segmentation and short sentence merging.",
    long_description = read_file('sentence_spliter/README.md'),
    author = "Li Wang",
    author_email = "wa_li_li@126.com",
    # package_dir={"":"sentence_spliter"},
    packages=['sentence_spliter'],
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    REQUIRES_PYTHON = '>=2.6.0',
    install_requires=['attrd>=0.0.3',
                      'attrs>=19.3.0',
                      'importlib-metadata>=1.6.0',
                      'more-itertools>=8.2.0',
                      'packaging>=20.3',
                      'pluggy>=0.13.1',
                      'py>=1.8.1',
                      'pyparsing>=2.4.7',
                      'pytest>=5.4.1',
                      'six>=1.14.0',
                      'wcwidth>=0.1.9',
                      'zipp>=3.1.0',
                      'Cerberus>=1.3.2']
    )

