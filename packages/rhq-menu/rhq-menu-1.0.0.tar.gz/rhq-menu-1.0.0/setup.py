import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rhq-menu",
    version="1.0.0",
    author="RHQ-Rusty",
    author_email="rusty@rhq.pw",
    description="A Modular, Extensible and Highly Scalable Menu Framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://rhq.pw/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)