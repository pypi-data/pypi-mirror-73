from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Number-Square",
    version="1.0.1",
    description="A Python package to square a number.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jhansi-27/Number-Square",
    author="Jhansi Rani",
    author_email="jhansi.rc26@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Number_Square"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "Number-Square=Number_square.square:main",
        ]
    },
)