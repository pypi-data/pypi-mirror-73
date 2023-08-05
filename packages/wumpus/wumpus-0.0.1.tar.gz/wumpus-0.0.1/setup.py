import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wumpus",
    version="0.0.1",
    author="SamHDev",
    author_email="samfuckedup@samh.dev",
    description="Another Discord Wrapper that no-one needs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samhdev/wumpus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)