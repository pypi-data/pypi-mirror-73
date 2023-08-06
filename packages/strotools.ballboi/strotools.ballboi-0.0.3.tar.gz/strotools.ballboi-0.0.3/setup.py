import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strotools.ballboi", # Replace with your own username
    version="0.0.3",
    author="Matthew Strozyk",
    author_email="mstrozyk25@gmail.com",
    description="Package to retrieve sports information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrstrozy/BallBoi",
    packages=setuptools.find_packages(include=['strotools.ballboi']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['strotools.common',],
)