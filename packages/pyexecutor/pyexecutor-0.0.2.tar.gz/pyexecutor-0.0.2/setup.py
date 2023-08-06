import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyexecutor",
    version="0.0.2",
    author="Herman",
    author_email="zijian0906@gmail.com",
    description="Command executor for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/actini/pyexecutor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
