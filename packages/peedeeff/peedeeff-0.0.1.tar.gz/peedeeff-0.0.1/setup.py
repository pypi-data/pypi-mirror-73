import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="peedeeff", 
    version="0.0.1",
    author="Charanjit Singh",
    author_email="charanjitdotsingh@gmail.com",
    description="Python Client for Peedeeff",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Peedeeff/python-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
