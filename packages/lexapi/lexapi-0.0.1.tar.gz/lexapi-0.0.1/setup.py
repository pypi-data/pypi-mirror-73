from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lexapi",
    version="0.0.1",
    author="Alex O'Leary",
    author_email="alexandria@inventati.org",
    description="An API for the Lex app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/finnoleary/lexapi",
    packages=find_packages(),
    install_requires=[
        "requests>=2.22.0",
        "pure-protobuf>=2.0.0"
    ],
    include_package_data=True,
    package_data={
        "": ["lex-api.org", "README.md"]
    },
    classifiers=[
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
