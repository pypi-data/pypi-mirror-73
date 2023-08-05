import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rushia-clipper",
    version="0.0.1",
    author="George Miao",
    author_email="gm@georgemiao.com",
    description="Download, trim, normalize, upload and publish audio clips to Rushia-btn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rushia-cn/Clipper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
