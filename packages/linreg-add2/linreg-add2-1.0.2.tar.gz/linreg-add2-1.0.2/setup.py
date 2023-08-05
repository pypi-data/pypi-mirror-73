from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="linreg-add2",
    version="1.0.2",
    description="A Python package to predict addmission chances using gre score tofel score and other details",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DexDand/linreg-add",
    author="Abhishek Dand",
    author_email="abhi080497@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["linreg_add2"],
    include_package_data=True,
)