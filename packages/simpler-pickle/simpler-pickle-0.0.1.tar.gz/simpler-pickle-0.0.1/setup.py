import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpler-pickle",
    version="0.0.1",
    author="Gari Ciodaro Guerra",
    author_email="gari.ciodaro.guerra@gmail.com",
    description="simpler pickle code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gariciodaro/simpler-pickle.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)