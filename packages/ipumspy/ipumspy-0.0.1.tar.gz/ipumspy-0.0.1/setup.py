import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipumspy",
    version="0.0.1",
    author="IPUMS",
    author_email="ipums@umn.edu",
    description="A placeholder for ipumspy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpc/ipumspy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
