from setuptools import setup

def readme():
    with open("README.md") as f:
        README = f.read()
    return README

setup(
    name="ArithmeticOperations",
    version="1.0.0",
    description="Basic Calculator App",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jhansi-27/Calculator",
    author="JhansiRani",
    author_email="jhansi.rc26@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7"
    ],
    packages=["arithmeticapp"],
    include_package_data=True,
    install_requires=["requests"],
)