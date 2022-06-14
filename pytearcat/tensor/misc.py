'''
A collection of miscelaneous functions
'''

import numpy as np 
from re import findall,search
from .core import config
from .core import ptseries
from .core.core import get_name, simplify, factor, expand, series as Series,core_calc
from .core import core
from .core.error import TensorSyntaxError
from .tensor import Tensor

if core_calc == 'gp':

    import io
    from contextlib import redirect_stdout

def factor_pt(x):

    if core_calc == 'gp':

        iscoreobj = isinstance(x,core.gpcore)

    elif core_calc == 'sp':

        iscoreobj =  isinstance(x,core.Expr)

    isnumber = False

    if isinstance(x,int) or isinstance(x,float) or isinstance(x,np.number):

        isnumber = True

    elif isinstance(x,Tensor):

        return x.factor()

    elif iscoreobj or isnumber:

        return factor(x)

    else:

        raise TypeError("The arg is not a mathematical object.")


def simplify_pt(x):

    if core_calc == 'gp':

        iscoreobj = isinstance(x,core.gpcore)

    elif core_calc == 'sp':

        iscoreobj =  isinstance(x,core.Expr)

    isnumber = False

    if isinstance(x,int) or isinstance(x,float) or isinstance(x,np.number):

        isnumber = True

    elif isinstance(x,Tensor):

        return x.simplify()

    elif iscoreobj or isnumber:

        return simplify(x)

    else:

        raise TypeError("The arg is not a mathematical object.")

def expand_pt(x):

    if core_calc == 'gp':

        iscoreobj = isinstance(x,core.gpcore)

    elif core_calc == 'sp':

        iscoreobj =  isinstance(x,core.Expr)

    isnumber = False

    if isinstance(x,int) or isinstance(x,float) or isinstance(x,np.number):

        isnumber = True

    elif isinstance(x,Tensor):

        return x.expand()

    elif iscoreobj or isnumber:

        return expand(x)

    else:

        raise TypeError("The arg is not a mathematical object.")

    

def set_space_time(x=True):

    config.space_time = x

def not_intersection(L1,L2):
    '''
    example: not_intersection(conf_vars,new_vars)

    retorna las variables de L2 que no estan en L1
    '''
    return [i for i in L2 if i not in L1]

def intersection(L1,L2):
    '''
    example: not_intersection(conf_vars,new_vars)

    retorna las variables de L2 que estan en L1
    '''
    return [i for i in L2 if i in L1]

def setorder(var,n):

    '''
    Sets the expansion order equal to "n" around variable "var". 

    Note: 
    This sets the expansion order equal to "n", allowing the program to truncate
    all the calculations up to this order. You can also revert to a value lower
    than "n" without having to restart the kernel. However, this does not work
    if the new order is greater than the first defined order since all the 
    higher-order terms were discarded in the first execution of this function.

    '''

    if core_calc == 'gp' and not isinstance(var,core.gpcore):

        raise(TypeError("var must be a giacpy object."))

    elif core_calc == 'sp' and not isinstance(var,core.Expr):

        raise(TypeError("var must be a sympy object."))

    ptseries.ord_status = True
    config.ord_status = True

    ptseries.ord_var = var
    config.ord_var = var

    ptseries.ord_n = n
    config.ord_n = n

def series(element):

    '''
    Compute the series of an element.
    '''

    if core_calc == 'gp':

        string = "simplify(Series(element, x = config.ord_var, n = config.ord_n+1))"

    elif core_calc == 'sp':

        string = "simplify(expand(Series(element, x = config.ord_var, n = config.ord_n+1)))"

    result = eval(string,locals(),globals())

    return result

def new_var(*args):

    '''
    example: new_var('x','y',...)
    
    '''

    input_vars = list(args)

    if not all(isinstance(var, str) for var in input_vars):

        raise(TypeError("Arguments must be str."))

    if 'epsilon' in input_vars or 'Epsilon' in input_vars:

        raise(NameError("Pytearcat does not support 'epsilon' as a variable name. Please use another name."))

    if 'varepsilon' in input_vars or 'Varepsilon' in input_vars:

        raise(NameError("Pytearcat does not support 'varepsilon' as a variable name. Please use another name."))

    names = []

    for i in config.var:
        names.append(get_name(i))

    
    new_vars = not_intersection(names,input_vars)
    old_vars = intersection(names,input_vars)

    variables = []
    def_variables = [i for i in config.var if get_name(i) in old_vars]

    if len(new_vars) != 0:

        for i in new_vars:

            variables.append(config.create_var(i))
    
    if len(variables) == 1:

        return variables[0]

    elif len(variables) == 0:

        if len(def_variables) == 1:

            return def_variables[0]
        else:
            return def_variables

    else:
        
        return variables

def new_con(*args):

    input_const = list(args)

    if not all(isinstance(var, str) for var in input_const):

        raise(TypeError("Arguments must be str."))

    if 'epsilon' in input_const or "Epsilon" in input_const:

        raise(NameError("Pytearcat does not support 'epsilon' as a variable name. Please use another name."))

    if 'varepsilon' in input_const or "Varepsilon" in input_const:

        raise(NameError("Pytearcat does not support 'varepsilon' as a variable name. Please use another name."))

    names = []

    for i in config.con:
        names.append(get_name(i))
    
    new_const = not_intersection(names,input_const)
    old_const = intersection(names,input_const)

    constants = []
    def_constants = [i for i in config.con if get_name(i) in old_const]

    if len(new_const) != 0:

        for i in new_const:

            constants.append(config.create_con(i))
    
    if len(constants) == 1:

        return constants[0]

    elif len(constants) == 0:

        print('Constant(s) already defined.')

        if len(def_constants) == 1:

            return def_constants[0]
        else:
            return def_constants

    else:
        
        return constants

def new_fun(fun_symbol,var_symbol,overwrite=False):

    '''
    Defines a new function receiving the name and the variables respectively. new_fun('f','t,x,y')
    '''

    # Aca se puede definir con un kwargs para que entren n funciones de la forma (f,variables)

    if not isinstance(fun_symbol,str):

        raise(TypeError("Function symbol must be a string"))

    if 'epsilon' in fun_symbol or "Epsilon" in fun_symbol:

        raise(NameError("Pytearcat does not support 'epsilon' as a variable name. Please use another name."))

    if 'varepsilon' in fun_symbol or "Varepsilon" in fun_symbol:

        raise(NameError("Pytearcat does not support 'varepsilon' as a variable name. Please use another name."))

    existing_names = []

    for i in config.fun:

        existing_names.append(get_name(i))

    new_var(*var_symbol.split(',')) # creates the variables if they not exist

    if fun_symbol not in existing_names or (fun_symbol in existing_names and overwrite == True) :

        function = config.create_fun(fun_symbol,var_symbol)

    else:

        print('Function %s(%s) is already defined'%(fun_symbol,var_symbol))

        fun_index = existing_names.index(fun_symbol)

        function = config.fun[fun_index]

    return function

def new_ten(tname,index):

    if len(findall('([^A-Za-z0-9])',tname)) != 0:

        raise TensorSyntaxError('The tensor name cannot contain any special character.')

    if tname in config.default_tensors:

        raise NameError("%s is protected as a default tensor name."%tname)

    if 'epsilon' == tname or "Epsilon" == tname:

        raise(NameError("Pytearcat does not support 'epsilon' as a variable name. Please use another name."))

    if 'varepsilon'  == tname or "Varepsilon"  == tname:

        raise(NameError("Pytearcat does not support 'varepsilon' as a variable name. Please use another name."))

    A = Tensor(tname,index)


    exec(reload_all('config'))

    return config.create_ten(tname,A)

def new_temp(temp_name,t_obj):

    return config.create_temp(temp_name,t_obj)

def delete_temp():

    for i in config.temp_name:

        exec('del(config.%s)'%i,locals(),globals())

        config.__all__.remove(i)

    
    config.temp = []

    config.temp_name = []


def in_var(name):

    var_list = list(map(get_name,config.var))

    if name in var_list:

        return True

    else:

        return False

def in_fun(name):

    fun_list = list(map(get_name,config.fun))

    if name in fun_list:

        return True

    else:

        return False

def in_ten(name):

    ten_list = list(map(get_name,config.ten))

    if name in ten_list:

        return True

    else:

        return False

def in_temp(name):

    temp_list = config.temp_name

    if name in temp_list:

        return True

    else:

        return False


def name_handler(string, name):

    # Revisar esto, deberia ser con un for i in config.var revisar si config.var[i].name == name.

    

    var_list = list(map(get_name,config.var))

    fun_list =list(map(get_name,config.fun))

def reload_all(new_module):

    ''' 

    This function reloads all the variables in __all__ from module
        
    Thanks to hurturk on https://stackoverflow.com/questions/44492803/python-dynamic-import-how-to-import-from-module-name-from-variable?newreg=9312458d429647fc8ec2a72e5655d197
        
    '''

    string = "globals().update({{n: getattr(module, n) for n in module.__all__}} if hasattr(module, '_all_') else {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')})"

    string = string.replace('module',new_module)

    return string