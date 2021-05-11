from itertools import product as iterprod
from .core import core, config
from .misc import new_ten, setorder
from .tensor_class import ordenar,construct
#from .LeviCivita import values, LeviCivita

def tdata_construct(elem,dim,n):

    string = ('%s,'%elem)*dim

    string = '['+string[:-1]+'],'

    for k in range(n-1):

        string = '['+(string*(dim))[:-1]+'],'  

    string = '[' + (string*(2**n))[:-1]+']'

    return eval(string)

