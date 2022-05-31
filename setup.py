from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["jupyter>=1.0.0", "numpy==1.19.0", "sympy>=1.7.1", "tqdm>=4.55.0", "jedi==0.17.2"]

ext_requirements = {"giacpy" : ["giacpy>=0.7.0"]}

setup(
    name="pytearcat",
    version="0.0.4",
    author="Joaquin Sureda",
    author_email="jmsureda@uc.cl",
    description="A package to perform tensor algebra calculations.",
    long_description=readme,
    long_description_content_type="text/markdown",
    licence="LICENCE",
    url="https://github.com/pytearcat/pytearcat",
    packages=find_packages(),
    install_requires=requirements,
    extras_require=ext_requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)