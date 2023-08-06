import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="badminton",
    version="0.0.6",
    description="Badminton data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/badminton",
    author="microprediction",
    author_email="info@microprediction.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["badminton"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["getjson"],
    entry_points={
        "console_scripts": [
            "badminton=badminton.__main__:main",
        ]
     },
     )
