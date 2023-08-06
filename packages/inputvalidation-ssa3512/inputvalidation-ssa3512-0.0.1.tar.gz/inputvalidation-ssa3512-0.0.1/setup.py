import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inputvalidation-ssa3512", # Replace with your own username
    version="0.0.1",
    author="Steve Ashman",
    author_email="steve@ash.mn",
    description="Simply console input validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssa3512/input-validation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)