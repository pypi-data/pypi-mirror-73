import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordfrequency", 
    version="0.1",
    author="Magnus Svensson",
    author_email="magnus@massivemonster.org",
    license='Apache License 2.0',
    description="A small utility script to count frequencies of words in a text file including options to stem,remove uoms, remove numerics, remove decimals, lemmitization ",
    long_description="A utility library using Python NLTK to process a text and count occurences of words. Includes the possibility to perform cleaning prior to counting such as e.g. remove numerics, stemming, remove uoms, remove decimals ++",
    url = "https://github.com/magsv/wordfreq",
    packages=setuptools.find_packages(),
    install_requires=[
        'nltk>=3.5',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5"
    ],
    python_requires='>=3.6',
)