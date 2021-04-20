import giacpy as __gp
from giacpy import latex
from .tdata import Tdata as __Tdata

class gpcore(__gp.giacpy.Pygen):
 
    def __init__(self,x):
        
        super().__init__()
        
    def __mul__(self,other):
        
        if isinstance(other,__Tdata):
        
            return other*self
        
        else:

            return gpcore(super().__mul__(other))  
        
    def __rmul__(self,other):
        
        if isinstance(other,__Tdata):
        
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
        
        return gpcore(gp.simplify(self))

#trigonometric functions

def sin(x):

    return gpcore(gp.sin(x))

def cos(x):

    return gpcore(gp.cos(x))

def tan(x):

    return gpcore(gp.tan(x))

def csc(x):

    return gpcore(gp.csc(x))

def sec(x):

    return gpcore(gp.sec(x))

def cot(x):

    return gpcore(gp.cot(x))

# arc trigonometric functions

def asin(x):

    return gpcore(gp.asin(x))

def acos(x):

    return gpcore(gp.acos(x))

def atan(x):

    return gpcore(gp.atan(x))

def acsc(x):

    return gpcore(gp.acsc(x))

def asec(x):

    return gpcore(gp.asec(x))

def acot(x):

    return gpcore(gp.acot(x))

# hyperbolic functions

def sinh(x):

    return gpcore(gp.sinh(x))

def cosh(x):

    return gpcore(gp.cosh(x))

def tanh(x):

    return gpcore(gp.tanh(x))

def csch(x):

    return gpcore(gp.csch(x))

def sech(x):

    return gpcore(gp.sech(x))

def coth(x):

    return gpcore(gp.coth(x))

# arc hyperbolic functions

def asinh(x):

    return gpcore(gp.asinh(x))

def acosh(x):

    return gpcore(gp.acosh(x))

def atanh(x):

    return gpcore(gp.atanh(x))

def acsch(x):

    return gpcore(gp.acsch(x))

def asech(x):

    return gpcore(gp.asech(x))

def acoth(x):

    return gpcore(gp.acoth(x))

# exp

def exp(x):

    return gpcore(gp.exp(x))

# log

def log(x):

    return gpcore(gp.log(x))

def log10(x):

    return gpcore(gp.log10(x))

def logb(x,b):

    return gpcore(gp.logb(x,b))

# sqrt

def sqrt(x):

    return gpcore(gp.sqrt(x))

# abs

def abs(x):

    return gpcore(gp.abs(x))

# general functions

def simplify(x):

    return gpcore(gp.simplify(x))

def series(f,epsilon,x0,n):

    return gpcore(gp.series(f,epsilon,x0,n))

def giac(x):

    return gpcore(gp.giac(x))

def expand(x):

    return gpcore(gp.expand(x))

def diff(f,x,n = 1):

    return gpcore(gp.diff(f,x,n))

def divide(a,b):

    return gpcore(gp.divide(a,b))

def factor(x):

    return gpcore(gp.factor(x))

def zeros(a,b):

    return gpcore(gp.zeros(a,b))

def coeff(a,x,n):

    return gpcore(gp.coeff(a,x,n))

def idn(n):

    return gpcore(gp.idn(n))

def matrix(x):

    return gpcore(gp.matrix(x))