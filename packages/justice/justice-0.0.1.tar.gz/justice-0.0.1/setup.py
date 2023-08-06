import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="justice",
    version="0.0.1",
    author="Jakub Boukal",
    author_email="www.bagr@gmail.com",
    description="A package to download company information from justice.cz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SukiCZ/justice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
