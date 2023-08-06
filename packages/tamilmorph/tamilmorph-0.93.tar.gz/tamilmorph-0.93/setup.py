import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tamilmorph", # Replace with your own username
    version="0.93",
    author="Kengatharaiyer Sarveswaran",
    author_email="sarvesk@uom.lk",
    description="A FST based Morphological analyser and generator for Tamil",
    long_description="Thamizhi morph (Tamil morph) is a rule based morphological analyser and generator for Tamil nouns and verbs",
    long_description_content_type="text/markdown",
    url="https://github.com/sarves/thamizhi-morph",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        'tamilmorph': ['fsts/*.fst']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: Tamil"
    ],
    python_requires='>=3.6',
)
