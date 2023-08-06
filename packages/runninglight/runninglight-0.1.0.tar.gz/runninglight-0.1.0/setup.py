import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="runninglight", # Replace with your own username
    version="0.1.0",
    author="Tim Hanewich",
    author_email="tahanewich@live.com",
    description="Package for controlling an LED running light that is hooked up to a Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TimHanewich/RunningLightControl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)