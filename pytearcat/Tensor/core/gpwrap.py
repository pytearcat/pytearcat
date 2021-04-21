import giacpy as __gp
from giacpy import latex
from .tdata import Tdata as _Tdata
from .display import tolatex, gp_pretty_latex, display_IP, Math_IP

class gpcore(__gp.giacpy.Pygen):
 
    def __init__(self,x):
        
        super().__init__()

    def __repr__(self):    
        '''
        a is an element from giacpy
        b is a string e.g. "T^{a}_{b}^{c}"

        '''

        string = tolatex(self)

        string = gp_pretty_latex(string)

        display_IP(Math_IP(string))
        
    def __mul__(self,other):
        
        if isinstance(other,_Tdata):
        
            return other*self
        
        else:

            return gpcore(super().__mul__(other))  
        
    def __rmul__(self,other):
        
        if isinstance(other,_Tdata):
        
            return self*other
        
        else:
            
            return gpcore(super().__rmul__(other))  
        
    def __add__(self,other):
        
        return gpcore(super().__add__(other))  

    def __radd__(self,other):
        
        return gpcore(super().__radd__(other))  
    
    def __sub__(self,other):
        
        return gpcore(super().__sub__(other))  
    
    def __rsub__(self,other):
        
        return gpcore(super().__rsub__(other))  
    
    def __truediv__(self,other):
        
        return gpcore(super().__truediv__(other))  
    
    def __rtruediv__(self,other):
        
        return gpcore(super().__rtruediv__(other))  
    
    def __pow__(self,other):
        
        return gpcore(super().__pow__(other)) 
    
    def __rpow__(self,other):
        
        return gpcore(super().__rpow__(other))  
    
    def simplify(self):
        
        return gpcore(__gp.simplify(self))

#trigonometric functions

def sin(x):

    return gpcore(__gp.sin(x))

def cos(x):

    return gpcore(__gp.cos(x))

def tan(x):

    return gpcore(__gp.tan(x))

def csc(x):

    return gpcore(__gp.csc(x))

def sec(x):

    return gpcore(__gp.sec(x))

def cot(x):

    return gpcore(__gp.cot(x))

# arc trigonometric functions

def asin(x):

    return gpcore(__gp.asin(x))

def acos(x):

    return gpcore(__gp.acos(x))

def atan(x):

    return gpcore(__gp.atan(x))

def acsc(x):

    return gpcore(__gp.acsc(x))

def asec(x):

    return gpcore(__gp.asec(x))

def acot(x):

    return gpcore(__gp.acot(x))

# hyperbolic functions

def sinh(x):

    return gpcore(__gp.sinh(x))

def cosh(x):

    return gpcore(__gp.cosh(x))

def tanh(x):

    return gpcore(__gp.tanh(x))

def csch(x):

    return gpcore(__gp.csch(x))

def sech(x):

    return gpcore(__gp.sech(x))

def coth(x):

    return gpcore(__gp.coth(x))

# arc hyperbolic functions

def asinh(x):

    return gpcore(__gp.asinh(x))

def acosh(x):

    return gpcore(__gp.acosh(x))

def atanh(x):

    return gpcore(__gp.atanh(x))

def acsch(x):

    return gpcore(__gp.acsch(x))

def asech(x):

    return gpcore(__gp.asech(x))

def acoth(x):

    return gpcore(__gp.acoth(x))

# exp

def exp(x):

    return gpcore(__gp.exp(x))

# log

def log(x):

    return gpcore(__gp.log(x))

def log10(x):

    return gpcore(__gp.log10(x))

def logb(x,b):

    return gpcore(__gp.logb(x,b))

# sqrt

def sqrt(x):

    return gpcore(__gp.sqrt(x))

# abs

def abs(x):

    return gpcore(__gp.abs(x))

# general functions

def simplify(x):

    return gpcore(__gp.simplify(x))

def series(f,epsilon,x0,n):

    return gpcore(__gp.series(f,epsilon,x0,n))

def giac(x):

    return gpcore(__gp.giac(x))

def expand(x):

    return gpcore(__gp.expand(x))

def diff(f,x,n = 1):

    return gpcore(__gp.diff(f,x,n))

def divide(a,b):

    return gpcore(__gp.divide(a,b))

def factor(x):

    return gpcore(__gp.factor(x))

def zeros(a,b):

    return gpcore(__gp.zeros(a,b))

def coeff(a,x,n):

    return gpcore(__gp.coeff(a,x,n))

def idn(n):

    return gpcore(__gp.idn(n))

def matrix(x):

    return gpcore(__gp.matrix(x))