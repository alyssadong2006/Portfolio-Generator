"""setup"""
import setuptools

with open("README.md", "r") as fh:
    LONGDESC = fh.read()

setuptools.setup(
    name="Portfolio-report-alyssadong2006", # Replace with your own username
    version="0.0.1",
    author="Alyssa",
    author_email="alydong2006@gmail.com",
    description="This is a portfolio report.",
    LONGDESC=LONGDESC,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
