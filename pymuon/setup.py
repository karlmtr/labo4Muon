import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymuon",
    version="0.1.0",
    author="Sacha Medaer, Edward Galantay, Brayan Reyes Alvarado",
    author_email="sacha.medaer@etu.unige.ch",
    python_requires=">=3.9.0",
    description="Muon Attenuation Simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='WTFPL',
    include_package_data=True,	# controls whether non-code files are copied when package is installed
    install_requires=["scipy", "numpy", "matplotlib"],
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
