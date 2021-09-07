# Pytearcat: PYthon TEnsor AlgebRa calCulATor<br /> A python package for general relativity and tensor calculus

Pytearcat is an open-source Python package created to work with general tensor operations, either in the field of General Relativity (GR) or others that need to use tensor calculus. It provides the basic GR tensors built in the package and uses a standard syntax for the Einstein notation. 

## Installation

As a Python package, Pytearcat can be installed through pip using

```bash
pip install pytearcat
```
To use the Giacpy core in Pytearcat, the user must explicitly indicate during the package installation that the installer must include the Giacpy module in the process. This is done through

```bash
pip install pytearcat[giapy]
```

## File structure summary
Inside the Pytearcat package, there are two sub-packages named _gr_ and _tensor_. Inside the first one, there are six modules related to GR expressions. These libraries allow calculating quantities that are very common in GR, such as the Christoffel symbols (first and the second kind, _christoffel.py_), the Ricci tensor and the Ricci scalar (_ricci.py_), the Riemann tensor (_riemann.py_) and the Einstein tensor (_einstein.py_). Also, there is a module to define the metric (_metric.py_) and another to calculate the geodesics (_geodesic.py_).
The second sub-package named _tensor_ contains modules that allow to define tensors and operate with them. The _misc.py_ module contains functions that allow defining symbolic functions, variables, and constants. It also contains other functions to work with series expansions and to simplify expressions. The _kdelta.py_ and _lcivita.py_ modules contain the data classes which define the Kronecker Delta symbol and the Levi-Civita symbol, respectively. 
The _tensor.py_ module contains the code related with the class _tensor_ and many functions that are useful to define a tensor, operate tensors, recognise the contravariant and covariant indices, lower and raise indices and expand a tensor like a series up to a specific order. Inside this sub-package, there is another one named _core_ which contains essential information that the program needs to operate tensors. All the functions required by the user are located at the top level of the package. 

## Usage

Pytearcat works using Jupyter Notebooks to give the outputs in mathematical form. To use the package the user should import Pytearcat within a Jypyter Notebook

```python
import pytearcat as pt
```

Later, it is possible to access the functions and methods of the package within the notebook. Different usage examples can be found in the top directory of the GitHub repository.

## How to cite this work

To cite this work, please refer to Pytearcat's release paper [San Martin & Sureda (2021)](https://arxiv.org/abs/2106.15016) and use the following Bibtex citation:


```bib
@misc{pytearcat2021,
      title={Pytearcat: PYthon TEnsor AlgebRa calCulATor}, 
      author={Marco San Martín and Joaquin Sureda},
      year={2021},
      eprint={2106.15016},
      archivePrefix={arXiv},
      primaryClass={gr-qc}
      }
```

