from setuptools import setup, find_packages

with open("README.md") as readmeFile:
    readmeStr = readmeFile.read()

setup(
    name="pipfilemerge",
    version="0.0.5",
    metadata_version="1.0",
    description="Merge the Pipfiles into a single global Pipfile",
    author="Laurkan Rodriguez",
    author_email="laurkan@engineer.com",
    long_description=readmeStr,
    long_description_content_type="text/markdown",
    url="https://github.com/lorkaan/merge-pipfile.git",
    download_url="https://github.com/lorkaan/pipfilemerge/archive/v0.0.5.tar.gz",
    install_requires =[
        'toml'
    ],
    packages=['pipfilemerge'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ]
)
