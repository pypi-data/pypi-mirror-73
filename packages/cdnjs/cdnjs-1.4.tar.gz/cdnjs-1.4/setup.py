import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cdnjs',
    version='1.4',
    author='Maxym Papezhuk',
    author_email='cods.max@gmail.com',
    packages=setuptools.find_packages(),
    url='https://gitlab.com/geany.been/django-cdnjs',
    description='CDNJS API Django Template tag, which allows to simply use cdns.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'django',
        'requests',
        'fuzzywuzzy[speedup]'
    ],
    classifiers=[
        'Framework :: Django',
    ]
)
