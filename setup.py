import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pytsa',
    author="Thimo Visser",
    author_email="thimo.visser@gmail.com",
    description="simple, human readable decorators package to ensure your method abides to it's contract",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thimovss/pytsa",
    license="MIT",
    packages=setuptools.find_packages(),
    keywords="type strict arguments rules",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    project_urls={
        "Source Code": "https://github.com/thimovss/pytsa",
    }
)
