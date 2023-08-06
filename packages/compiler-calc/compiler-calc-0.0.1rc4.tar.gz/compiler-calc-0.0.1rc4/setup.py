import setuptools
from compiler_calc import simple_calc

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="compiler-calc",
    version=simple_calc.__version__,
    author=simple_calc.__author__,
    author_email=simple_calc.__email__,
    description="A simple calculator programme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tq010or/compiler_calc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)