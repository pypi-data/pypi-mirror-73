import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dishevel",
    version="0.0.2",
    author="Kaecy",
    author_email="keacy@earth.org",
    description="a telegram bot framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gist.github.com/kaecy/3c1a6a6f2d39d9df907f6935d8b2ba40",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)