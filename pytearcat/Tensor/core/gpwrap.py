import giacpy as gp
from giacpy import latex
from .tdata import Tdata

class Elem(gp.giacpy.Pygen):
 
    def __init__(self,x):
        
        super().__init__()
        
    def __mul__(self,other):
        
        if isinstance(other,Tdata):
        
            return other*self
        
        else:

            return Elem(super().__mul__(other))  
        
    def __rmul__(self,other):
        
        if isinstance(other,Tdata):
        
            return self*other
        
        else:
            
            return Elem(super().__rmul__(other))  
        
    def __add__(self,other):
        
        return Elem(super().__add__(other))  

    def __radd__(self,other):
        
        return Elem(super().__radd__(other))  
    
    def __sub__(self,other):
        
        return Elem(super().__sub__(other))  
    
    def __rsub__(self,other):
        
        return Elem(super().__rsub__(other))  
    
    def __truediv__(self,other):
        
        return Elem(super().__truediv__(other))  
    
    def __rtruediv__(self,other):
        
        return Elem(super().__rtruediv__(other))  
    
    def __pow__(self,other):
        
        return Elem(super().__pow__(other)) 
    
    def __rpow__(self,other):
        
        return Elem(super().__rpow__(other))  
    
    def simplify(self):
        
        return Elem(gp.simplify(self))

#trigonometric functions

def sin(x):

    return Elem(gp.sin(x))

def cos(x):

    return Elem(gp.cos(x))

def tan(x):

    return Elem(gp.tan(x))

def csc(x):

    return Elem(gp.csc(x))

def sec(x):

    return Elem(gp.sec(x))

def cot(x):

    return Elem(gp.cot(x))

# arc trigonometric functions

def asin(x):

    return Elem(gp.asin(x))

def acos(x):

    return Elem(gp.acos(x))

def atan(x):

    return Elem(gp.atan(x))

def acsc(x):

    return Elem(gp.acsc(x))

def asec(x):

    return Elem(gp.asec(x))

def acot(x):

    return Elem(gp.acot(x))

# hyperbolic functions

def sinh(x):

    return Elem(gp.sinh(x))

def cosh(x):

    return Elem(gp.cosh(x))

def tanh(x):

    return Elem(gp.tanh(x))

def csch(x):

    return Elem(gp.csch(x))

def sech(x):

    return Elem(gp.sech(x))

def coth(x):

    return Elem(gp.coth(x))

# arc hyperbolic functions

def asinh(x):

    return Elem(gp.asinh(x))

def acosh(x):

    return Elem(gp.acosh(x))

def atanh(x):

    return Elem(gp.atanh(x))

def acsch(x):

    return Elem(gp.acsch(x))

def asech(x):

    return Elem(gp.asech(x))

def acoth(x):

    return Elem(gp.acoth(x))

# exp

def exp(x):

    return Elem(gp.exp(x))

# log

def log(x):

    return Elem(gp.log(x))

def log10(x):

    return Elem(gp.log10(x))

def logb(x,b):

    return Elem(gp.logb(x,b))

# sqrt

def sqrt(x):

    return Elem(gp.sqrt(x))

# abs

def abs(x):

    return Elem(gp.abs(x))

# general functions

def simplify(x):

    return Elem(gp.simplify(x))

def series(f,epsilon,x0,n):

    return Elem(gp.series(f,epsilon,x0,n))

def giac(x):

    return Elem(gp.giac(x))

def expand(x):

    return Elem(gp.expand(x))

def diff(f,x,n = 1):

    return Elem(gp.diff(f,x,n))

def divide(a,b):

    return Elem(gp.divide(a,b))

def factor(x):

    return Elem(gp.factor(x))

def zeros(a,b):

    return Elem(gp.zeros(a,b))

def coeff(a,x,n):

    return Elem(gp.coeff(a,x,n))

def idn(n):

    return Elem(gp.idn(n))

def matrix(x):

    return Elem(gp.matrix(x))