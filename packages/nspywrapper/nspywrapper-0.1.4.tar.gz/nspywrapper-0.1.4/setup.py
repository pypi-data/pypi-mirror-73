from distutils.core import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name = "nspywrapper",
    packages = ["nspywrapper"],
    version = "0.1.4",
    license = "Apache",
    description = "A python wrapper for the NationStates API",
    long_description = long_description,
    author = "Andrew Brown (aka SherpDaWerp)",
    author_email = "abrow425@gmail.com",
    url = "https://github.com/abrow425/nspy_wrapper",
    download_url = "https://github.com/abrow425/nspy_wrapper/archive/v0.1.4.tar.gz",
    keywords = ["NATIONSTATES", "NS", "API", "WRAPPER"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
