import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Reff", # Replace with your own username
    version="0.0.2",
    author="Takahiro Nakamura",
    author_email="a41757@gmail.com",
    description="effective reproduction number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tt-nakamura/Reff",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
