import setuptools
import codecs
import os.path

##   ---- Time-stamp: <2020-07-12 19:31:52 hedfp> -----

## code to get version number from __init__.py

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")
## end version number extraction functions

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="classroom_gizmos",
    ####version="0.0b1.dev5", # X.YaN.devM format
    version=get_version("classroom_gizmos/__init__.py"),
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
