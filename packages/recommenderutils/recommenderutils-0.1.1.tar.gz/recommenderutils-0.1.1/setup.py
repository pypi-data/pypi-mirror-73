import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recommenderutils",
    version="0.1.1",
    author="Ron Medina",
    author_email="ron@brewedlogic.com",
    description="Recommender system for Crisp ML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/brewedlogic/hq-pos/crisp-ml/-/tree/master/recommender-builder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "scikit-learn>=0.23.0",
        "numpy>=1.18.4",
        "pandas>=1.0.3",
    ],
    python_requires='>=3.7',
)