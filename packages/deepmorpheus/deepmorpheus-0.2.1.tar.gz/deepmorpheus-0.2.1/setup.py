import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepmorpheus",
    version="0.2.1",
    author="Mees Gelein, Jeroen Offerijns",
    description="Morphological tagger for Ancient Greek using deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/offerijns/deepmorpheus",
    packages=["deepmorpheus"],
    dependency_links=[
        "https://download.pytorch.org/whl/torch_stable.html",
    ],
    install_requires=["torch==1.5.0", "pyconll==2.2.1", "requests==2.23.0", "pytorch_lightning==0.8.4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
