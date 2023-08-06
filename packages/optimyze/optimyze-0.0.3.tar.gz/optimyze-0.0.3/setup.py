import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="optimyze",
    version="0.0.3",
    author="Saed SayedAhmed",
    author_email="saadmtsa@gmail.com",
    description="Hyperparamter optimization package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SaadMTSA/optimyze",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pyDOE>=0.3.8",
        "scikit-learn>=0.22"
    ],
    python_requires=">=3.6",
)
