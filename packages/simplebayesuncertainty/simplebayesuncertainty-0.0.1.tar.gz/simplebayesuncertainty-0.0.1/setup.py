import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplebayesuncertainty", # Replace with your own username
    version="0.0.1",
    author="Manuel Marschall",
    author_email="manuel.marschall@ptb.de",
    description="The paper provides a simple and easy method to employ the Bayesian paradigm for typical applications in metrology.  The suggested choice for the prior, the sampling methods and the analysis of the resulting posterior is covered in this repository.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuelmarschall/SimpleBayesUncertainty",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
