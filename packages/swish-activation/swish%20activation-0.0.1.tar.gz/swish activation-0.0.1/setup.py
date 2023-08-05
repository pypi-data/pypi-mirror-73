import setuptools

from setuptools import setup

 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="swish activation",
 
    #version of the module
    version="0.0.1",
 
    #Name of Author
    author="Sagnik Banerjee",
 
    #your Email address
    author_email="sagu7065@gmail.com",
 
    #Small Description about module
    description="swish activation function",
 
    long_description=long_description,
 
    #Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",
 
    #Any link to reach this module, if you have any webpage or github profile
    url="https://github.com/Sagu12",
    packages=setuptools.find_packages(),
 
    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
