import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="irismodel", 
    version="0.0.10",
    author="Lars Kjeldgaard",
    author_email="lars_kjeldgaard@hotmail.com",
    description="Slim Iris Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'sklearn',
        'numpy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
    )
