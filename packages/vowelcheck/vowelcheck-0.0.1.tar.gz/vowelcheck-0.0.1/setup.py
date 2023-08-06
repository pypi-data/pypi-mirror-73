from setuptools import setup

with open ("README.md","r") as fh:
    long_description = fh.read()


setup(
    name = 'vowelcheck' ,
    version  = '0.0.1' ,
    description = 'Check the crater is vowel or not.',
    py_module = ["vowelcheck"],
    package_dir = {"" : 'src'},
    classifires = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License V2 or later (GPLV2+)",
        "Operating System :: OS Indipendent"
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/nabeelfahmi12/pypi_vowel_check/tree/master",
    author = "Nabeel Fahmi",
    author_email = "nabeelfahmi.12@gmail.com",

)
