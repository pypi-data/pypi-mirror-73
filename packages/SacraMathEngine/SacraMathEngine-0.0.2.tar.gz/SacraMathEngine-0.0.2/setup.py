from setuptools import setup, find_packages

with open("readme.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name = "SacraMathEngine",
    version = "0.0.2",
    author = "Andreas Evensen",
    author_email = "Andreas.evensen11@gmail.com",
    description = "A lightweight 3-d vector package with intents of being used in Sacra Game Engine",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules = ["Matrix", "Vector", "Triangle"],
    #package_dir = {'':'src'},
    include_package_data = True,
    packages = find_packages(),
    license = "MIT",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
)
