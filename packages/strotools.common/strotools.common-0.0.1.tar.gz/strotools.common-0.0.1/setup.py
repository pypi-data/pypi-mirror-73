import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strotools.common", # Replace with your own username
    version="0.0.1",
    author="Matthew Strozyk",
    author_email="mstrozyk25@gmail.com",
    description="Strotools common packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrstrozy/strotools.common",
    packages=setuptools.find_packages(include=['strotools.common']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests',]
)