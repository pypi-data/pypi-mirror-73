import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdl",
    version="0.0.0",
    author="Yam",
    author_email="haoshaochun@gmail.com",
    description="Structured Data DeepLearning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hscspring/sdl",
    packages=setuptools.find_packages(),
    install_requires=[
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)