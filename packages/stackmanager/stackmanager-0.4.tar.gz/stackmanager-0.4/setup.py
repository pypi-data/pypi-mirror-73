from setuptools import setup

with open('README.md', 'r') as t:
    README = t.read()

setup(
    name='stackmanager',
    version='0.4',
    description='Utility to manage CloudFormation stacks using YAML configuration file',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/LeadingEDJE/stackmanager',
    author='Andrew May',
    packages=['stackmanager'],
    install_requires=[
        'Click',
        'boto3',
        'pyyaml',
        'tabulate',
        'jinja2'
    ],
    entry_points='''
        [console_scripts]
        stackmanager=stackmanager.cli:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)