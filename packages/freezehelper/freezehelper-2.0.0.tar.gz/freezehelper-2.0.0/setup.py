import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="freezehelper",
    version="2.0.0",
    author="Brandon M. Pace",
    author_email="brandonmpace@gmail.com",
    description="A Python package to simplify checks for frozen state and executable directory",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    keywords="freeze frozen PyInstaller parent child process executable directory path",
    license="GNU Lesser General Public License v3 or later",
    platforms=['any'],
    python_requires=">=3.6.5",
    url="https://github.com/brandonmpace/freezehelper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ]
)
