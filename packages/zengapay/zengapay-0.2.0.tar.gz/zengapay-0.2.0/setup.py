import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="zengapay",
    version="0.2.0",
    description="Python Wrapper for the ZengaPay API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zengapay/zengapay-python",
    author="Patrick Walukagga",
    author_email="pwalukagga@gmail.com",
    python_requires=">=3.7.0",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["ZengaPay", "ZengaPay API", "ZengaPay Python Wrapper", "ZengaPay Python"],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=["requests", "phonenumbers"],
    # entry_points={
    #     "console_scripts": [
    #     ]
    # },
)
