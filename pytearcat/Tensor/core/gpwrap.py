import giacpy as __gp
from giacpy import latex
import io
from re import findall, search
from IPython.display import display as display_IP, Math as Math_IP
from contextlib import redirect_stdout
from .tdata import Tdata as _Tdata
from pytearcat.Tensor.core import series_expansion 
from pytearcat.Tensor.core import greek
from pytearcat.Tensor.core import fun
#import sys

import sys

def in_notebook():
    """
    Returns ``True`` if the module is running in IPython kernel,
    ``False`` if in IPython shell or other Python shell.
    """
    return 'ipykernel' in sys.modules

# later I found out this:

def ipython_info():

    ip = False
    if 'ipykernel' in sys.modules:
        ip = 'notebook'
    elif 'IPython' in sys.modules:
        ip = 'terminal'
    
    print(ip)
    return ip

def get_name(element):
        
    f = io.StringIO()
    with redirect_stdout(f):
        print(element)
    element = f.getvalue()

    return element[:-1]

def tolatex(element):

    f = io.StringIO()
    with redirect_stdout(f):
        print(latex(element))
    element = f.getvalue()

    string =  element[1:-2]

    return string

def gp_pretty_order(element):
    
    ord_n = series_expansion.ord_n
    ord_var = get_name(series_expansion.ord_var)
    
    if ord_var in greek.greek_dict:

        ord_var = r"\%s"%ord_var

    structure = r"\%s\^\{(\d+)\} \\operatorname\{\\mathrm\{order\\_size\} \}\\left\(\%s\\right\)"%(ord_var,ord_var)

    exponent = findall(structure,element)

    if len(exponent) > 0:

        structure = r"%s^{%s} \operatorname{\mathrm{order\_size} }\left(%s\right)"%(ord_var,exponent[0],ord_var)

        final = element.replace(r"%s"%structure,r"\mathrm{O}\left(%s^{%s}\right)"%(ord_var,exponent[0]))
        
    elif len(exponent) == 0:

        structure = r"%s \operatorname{\mathrm{order\_size} }\left(%s\right)"%(ord_var,ord_var)

        final = element.replace(r"%s"%structure,r"\mathrm{O}\left(%s\right)"%ord_var)

    return final

def gp_pretty_latex(element):
    
    '''
    It takes a giacpy latex expression and returns a latex string that is similar to the sympy notation.
    
        - It rewrites the derivatives
        - It rewrites the expansion order
    
    '''
    
    names = {}
    variables = []

    result = element[:]
    
    greek_dict =greek.greek_dict

    for i in fun.fun:

        x = r'%s'%str(latex(i))[1:].split("\left")[0].replace('\\','').replace('{','\\{').replace('}','\\}').replace('mathrm','\\\\mathrm')

        names[x] = str(i).split('(')[1][:-1]

    for i in names:

        j = findall(r'(?<=\W)%s\^\{\\left\((.*?)\\right\)\}'%i,element)
        
        for k in j:

            ind = k.split(',')

            ini,fin = search(r'%s\^\{\\left\(%s\\right\)\}'%(i,k),element).span()
            
            while element[ini] != ' ' and element[ini] != ',' and element[ini] != '\\' and element[ini] != '-' and element[ini] != '+':

                ini -= 1

            string = ''

            l_dict = {}

            for l in ind: 

                l_dict[l] = ind.count(l)  
                
            for l in l_dict:  # L = '1'

                y = names[i].split(',')[int(l)-1]
                    
                if y in greek_dict.keys():
                        
                    y = r'\\%s'%y
                
                if l_dict[l] == 1:
                    
                    string += r'\frac{\partial }{\partial %s}'%y

                else:

                    string += r'\frac{\partial^%d }{\partial %s^%d}'%(l_dict[l],y,l_dict[l])

            string+= i

            result = result.replace(element[ini:fin],string)    

    for func in names:

        if func in greek_dict.keys():

            result = result.replace(func,greek_dict[func])
            
    if series_expansion.ord_status == True:

        result = gp_pretty_order(result)

    return result.replace('\\\\','\\').replace("\"","").replace("\\{","{").replace("\\}","}")


    def tolatex(element):

        f = io.StringIO()
        with redirect_stdout(f):
            print(latex(element))
        element = f.getvalue()

        string =  element[1:-2]

        return gp_pretty_latex(string)


class gpcore(__gp.giacpy.Pygen):
 
    def __init__(self,x):
        
        super().__init__()

    def __getitem__(self,rollno):

        return gpcore(super().__getitem__(rollno))

    def __setitem__(self,rollno,name):

        return gpcore(super().__setitem__(rollno,name))

    def __str__(self):

        #print("STR")

        return super().__str__()

    def _repr_html_(self):

        #print("llamando a html")

        string = tolatex(self)

        string = gp_pretty_latex(string)

        #display_IP(Math_IP(string))

        return "$$ %s $$"%string


    #def __repr_latex_(self):

    #    print("llamando a latex")

    #    return "llamando a latex"

    #def __call__(self):

    #    print("llamando a call")

    #    return "llamando al call"

    #def printf(self):

    #    print("llamando a printf")
    #    return " llamando a printf"

    #def print(self):

    #    print("llamando a print")
    #    return " llamando a printf"

    #def about(self):

    #    print("llamando a about")

    #    return "about"

    def __repr__(self):    

        #print("llamando a repr")

        

        return ""
        #return "llamando a repr" #str(self)
        
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