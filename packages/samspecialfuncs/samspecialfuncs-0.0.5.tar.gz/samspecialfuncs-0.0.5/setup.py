#https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html for details

from setuptools import setup, find_packages, Extension
import numpy as np



extensions = [
    Extension(name="samspecialfuncs.bessellike.nufuncs",
              sources=["src/bessellike/c_to_py.c",
                       "src/bessellike/nufuncs.c",
                       "src/bessellike/static_s1.c",
                       "src/bessellike/static_s2.c",
                       "src/bessellike/static_q1.c",
                       "src/bessellike/static_q2.c",
                       "src/bessellike/chbevl.c"],
              include_dirs=["src/bessellike/",np.get_include()])]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="samspecialfuncs",
    version="0.0.5",
    author="Sam Cameron",
    author_email="samuel.j.m.cameron@gmail.com",
    description="Special functions that Sam needs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samueljmcameron/samspecialfuncs",
    packages=find_packages(),
    ext_modules = extensions,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy']
)
