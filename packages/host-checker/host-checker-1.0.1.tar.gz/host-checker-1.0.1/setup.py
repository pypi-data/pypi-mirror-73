import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="host-checker",
    version="1.0.1",
    description="Simple CLI tool to check who is hosting a website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SimoneCorazza/HostChecker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)