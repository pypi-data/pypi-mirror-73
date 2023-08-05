import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = ['requests','beautifulsoup4','pandas']
setuptools.setup(
    name="icd10_c2d",
    version="0.0.2",
    author="Kantheti Saket Ram",
    author_email="sakethaux1111@gmail.com",
    description="A package to get ICD10 Description from ICD10 Codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires = REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
