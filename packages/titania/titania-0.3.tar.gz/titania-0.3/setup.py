
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='titania',
    version='0.3',
    author="Maciej Majewski",
    author_email="mmajewsk@cern.ch",
    description="Titania monitoring framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mmajewsk/titania",
    package_dir={'titania': 'core'},
    packages=['titania'],
    classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )