
__core = 'sp' # sympy
#__core = 'se' # symengine

if __core == 'sp':

    from sympy import *
    # import sympy as sp
    # from sympy import sympify
    # from sympy import Symbol, Function
    # from sympy import diff, Rational
    # from sympy import zeros, eye
    # from sympy import init_printing, latex
    def get_name(f):

        return f.name

elif __core == 'se':

    from symengine import *
    # import symengine as se
    # from symengine import sympify
    # from symengine import Symbol, Function 
    # from symengine import diff, Rational
    # from symengine import zeros, eye
    # from symengine import init_printing, latex
    def get_name(f):

        return f.get_name()

from sympy import factor, simplify, series, nsimplify, expand, Matrix # Si o si deben ser de sympy
from sympy.tensor.array import Array
from IPython.display import display, Math, Latex








