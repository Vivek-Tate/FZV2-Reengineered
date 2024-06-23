from setuptools import setup, find_packages

setup(
    name='FZ',
    version='2.1.2',
    description='A tool for gathering information about files and directories',
    author='PGT04-TeamProject',
    author_email='',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'finderz = FZV2:main'
        ]
    },
    install_requires=[
        'sphinx-rtd-theme',
    ],
)
