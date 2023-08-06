import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genwal",
    version="0.0.1",
    author="Aleksa Ognjanovic",
    author_email="alexa.ognjanovic@gmail.com",
    description="Little python script to generate Gentoo wallpapers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GrbavaCigla/genwal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.4",
)