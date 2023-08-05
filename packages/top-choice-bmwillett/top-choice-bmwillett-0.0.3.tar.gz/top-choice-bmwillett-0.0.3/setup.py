import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="top-choice-bmwillett",
    version="0.0.3",
    author="Brian Willett",
    author_email="bmwillett1@gmail.com",
    description="A package using topological data analysis to achieve robust product recommendations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bmwillett/topological-recommendations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
