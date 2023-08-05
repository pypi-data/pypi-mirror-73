import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logging_dl1244ssk2", # Replace with your own username
    version="0.0.1",
    author="Alex X.T. Wang",
    author_email="xintong.wang@riotinto.com",
    description="Utilities package for function logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexXTW/logging_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
