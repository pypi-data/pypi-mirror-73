import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mrkdwn2html",
    version="0.0.2",
    author="John Montgomery",
    author_email="john@johnmontgomery.tech",
    description="Convert markdown to html.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/john-montgomery2003/mrkdwn2html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
