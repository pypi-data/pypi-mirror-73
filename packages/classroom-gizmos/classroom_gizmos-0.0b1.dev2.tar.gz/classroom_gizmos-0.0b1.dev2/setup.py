import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="classroom_gizmos",
    version="0.0b1.dev2", # X.YaN.devM format
    author="Carl Schmiedekamp",
    author_email="cw2@psu.edu",
    description="Several small functions for classroom instruction.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #############################url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
	"Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.6',
)
