from setuptools import setup
from setuptools import find_packages

from pysplitter import __version__ as v


with open('pysplitter/README.md', 'r') as fp:
    long_description = fp.read()
    
setup(
    name='pysplitter',
    version=v,
    author='Mark Todisco',
    description='A python package that splits large files into smaller chunks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marktodisco/pysplit',
    packages=find_packages(),
    install_requires=['numpy'],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
)
