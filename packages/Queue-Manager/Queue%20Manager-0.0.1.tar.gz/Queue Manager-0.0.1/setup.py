import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Queue Manager",
    version="0.0.1",
    author="Barad & Riftin & Ori",
    description="A library for using queues as both a producer and a consumer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/riftool/queue-manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
