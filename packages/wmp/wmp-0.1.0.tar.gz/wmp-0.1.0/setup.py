import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wmp",
    version="0.1.0",
    author="Frederick Corpuz",
    author_email="fcorpuz@wesleyan.edu",
    description="Module for face detection & recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wmp-face.readthedocs.io",
    packages=setuptools.find_packages(),
    package_data={"wmp": ["datasets/*.jpg", "datasets/*.mp4"]},
    install_requires=["dlib>=19.20.0", "numpy>=1.19.0", "Pillow>=7.2.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
