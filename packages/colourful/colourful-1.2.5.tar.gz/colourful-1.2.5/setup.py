import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colourful",
    version="1.2.5",
    author="toxicrecker",
    author_email="reck.channel.mainlead@gmail.com",
    description="colourful is a package to colorize any greyscale image.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toxicrecker/colourful",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)