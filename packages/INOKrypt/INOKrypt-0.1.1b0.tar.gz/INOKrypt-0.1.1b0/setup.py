import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="INOKrypt",
    version="0.1.1.b",
    author="Shobhit Sharma",
    author_email="shobhit@technical0812.com",
    description="INOKrypt - For Secure Data Communication Between IoT Devices & IoT Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheThingsPlanet/INOKrypt",
    project_urls={
    'Documentation': 'https://inokrypt.readthedocs.io/',
    'Say Thanks!': 'https://twitter.com/ScriptKKiddie',
    'Source': 'https://github.com/TheThingsPlanet/INOKrypt',},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
