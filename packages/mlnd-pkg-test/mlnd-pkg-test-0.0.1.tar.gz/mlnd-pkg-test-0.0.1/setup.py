import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlnd-pkg-test", # Replace with your own username
    version="0.0.1",
    author="Olavo Sampaio",
    author_email="olavosamp@poli.ufrj.br",
    description="Small PyPi package building experiment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olavosamp/mlnd-pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)