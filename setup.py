from setuptools import setup, find_packages

try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

VERSION = '1.0.0'
DESCRIPTION = 'package to solve separable non linear optimization problems'
URL = 'https://github.com/uichathurika/laptimize'
INSTALL_REQUIRES = [
    'numpy',
    'pandas',
    'pulp'
]
LICENSE = 'MIT'

setup(
    name="laptimize",
    version=VERSION,
    author="Ishanga Udatiyawala",
    author_email="uichathurika@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,

    keywords=['python', 'non linear optimization', 'separable programming', 'branch and bound', 'global solution'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Mathematics"
    ]
)
