import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fdfs-client-py3",
    version="1.0.0",
    author="smartli",
    author_email="smartli_it@163.com",
    description="python3 fastdfs package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smartlz/fdfs-client-py3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
