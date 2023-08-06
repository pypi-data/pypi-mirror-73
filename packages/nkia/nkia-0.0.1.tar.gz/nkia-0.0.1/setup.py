import os
from pathlib import Path
from setuptools import setup


def read(file_name):
    with open(os.path.join(Path(os.path.dirname(__file__)), file_name)) as _file:
        return _file.read()


long_description = read("README.md")

setup(
    name='nkia',
    version='0.0.1',
    description='This is a module to predict the products category using artificial inteligence.',
    url='https://bitbucket.org/nksistemasdeinformacao/servicos-biodigital/src/master/',
    download_url='https://bitbucket.org/nksistemasdeinformacao/servicos-biodigital/src/master/',
    license='Apache License 2.0',
    author='NK Sistemas de Informacao em Saude',
    author_email="ti@nkodontologia.com.br",

    py_modules=["nkia"],
    package_dir={"": "src/ml"},

    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['tensorflow', 'nlp', 'nk',
              'python3', 'python-3', 'food-products'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
    python_requires='>=3.6',
    install_requires=[
    ],
    extras_require={
        "dev": [
            "pytest>=3.7"
        ]
    }
)