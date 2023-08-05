import setuptools

with open("../README.md", "r") as fh:
    long_discription = fh.read()

setuptools.setup(
    name="pymlmodels-MeatBoyed",
    version="0.1.0",
    author="MeatBoyed",
    author_email="charlie2meat@yahoo.com",
    description="Collection of easy to use Machine Learning Models.",
    long_description=long_discription,
    long_description_content_type="text/markdown",
    url="https://github.com/MeatBoyed/pymlmodels",
    packages=setuptools.find_packages(),
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
