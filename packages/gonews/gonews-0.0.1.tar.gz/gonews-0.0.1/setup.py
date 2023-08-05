import os

from setuptools import find_namespace_packages, setup

PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, 'README.md')) as fin:
    README = fin.read()

setup(
    name='gonews',
    version='0.0.1',
    packages=find_namespace_packages(include=['gonews', 'gonews.*']),
    include_package_data=True,
    description='A simple to use CLI for viewing Google News top stories and searching for specific stories',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://www.github.com/tannerburns/gonews',
    author='Tanner Burns',
    author_email='tjburns102@gmail.com',
    install_requires=[
        'click',
        'xmltodict',
        'modutils'
    ],
    entry_points={
        "console_scripts": [
            'gonews=gonews.cli:cli'
        ]
    }
)