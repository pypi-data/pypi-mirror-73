import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Medeina",
    version="2.0",
    author="Daniel Davies",
    author_email="dd16785@bristol.ac.uk",
    description="A automated solution for building of cumulative interacion web",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Daniel-Davies/Medeina",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["Food Webs", "Species networks", "Cumulative Networks"],
    install_requires=[
        "pycountry",
        "taxon_parser",
        "networkx",
        "numpy",
        "msgpack",
        "EcoNameTranslator",
        "requests",
        "pandas",
    ],
)
