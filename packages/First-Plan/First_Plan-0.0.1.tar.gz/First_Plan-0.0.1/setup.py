import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="First_Plan", # Replace with your own username
    version="0.0.1",
    author="First_Plan",
    author_email="author@example.com",
    description="First_Plan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['numpy'],
    python_requires='>=3.6',
)