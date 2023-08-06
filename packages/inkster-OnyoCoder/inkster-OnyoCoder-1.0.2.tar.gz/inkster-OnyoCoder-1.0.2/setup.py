import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inkster-OnyoCoder", # Replace with your own username
    version="1.0.2",
    author="OnyoCoder",
    author_email="InksterPY@protonmail.com",
    description="Inkster is possible for many things.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OnyoCoder/inkster-py",
    project_urls={
        "Discord": "https://discord.gg/HUFtMsz"
    },
    License='MIT',
    keywords='splatter',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.8',
)
