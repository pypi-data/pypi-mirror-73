import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="diga-olar",
    version="0.0.1",
    author="André Girol",
    author_email="andregirol@gmail.com",
    description="Diga olá da forma mais estilosa na língua brasileira",
    url="https://github.com/girol/diga-olar",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)