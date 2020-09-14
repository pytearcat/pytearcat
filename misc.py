import numpy as np 
import config 
from tensor_class import Tensor
from errors import TensorSyntaxError
from re import findall

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

def order(var,n):

    # Esto define el orden al que se va a trabajar considerando una expansion

    config.ord_status = True

    config.ord_var = new_var(str(var))

    config.ord_n = n


def new_var(*args):

    '''
    example: new_var('x','y',...)
    
    '''
    # revisar que cada elemento de args sea un string, de lo contrario arrojar error.
    # var_symbol siempre debe ser un string

    input_vars = list(args)

    names = []

    for i in config.var:
        names.append(i.name)

    
    new_vars = not_intersection(names,input_vars)
    old_vars = intersection(names,input_vars)

    variables = []
    def_variables = [i for i in config.var if i.name in old_vars]

    if len(new_vars) != 0:

        for i in new_vars:

            variables.append(config.create_var(i))
    
    if len(variables) == 1:

        return variables[0]

    elif len(variables) == 0:

        #print('Variable(s) already defined.')  # Quizas permitir este print cuando sea __name_ = 'main'

        if len(def_variables) == 1:

            return def_variables[0]
        else:
            return def_variables

    else:
        
        return variables

def new_con(*args):

    input_const = list(args)

    names = []

    for i in config.con:
        names.append(i.name)

    
    new_const = not_intersection(names,input_const)
    old_const = intersection(names,input_const)

    constants = []
    def_constants = [i for i in config.con if i.name in old_const]

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

    existing_names = []

    for i in config.fun:

        existing_names.append(i.get_name())

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


def n_order(var,n):

    '''
    The program will work up to order 'n' in the variable 'var'.
    
    '''
    # Falta ver que var sea string y n sea un entero.

    config.ord_status = True

    str4="config.ord_var = sp.Symbol('xVAR', real=True)"
    str4=str4.replace('xVAR',var)
    exec(str4,globals())

    config.ord_n = n

def get_name(elem):

        return elem.name

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

# def reload_all(module):

    # version penita de joaquin
    
    #     string = 'from XXXX import *'
    
    #     string = string.replace('XXXX',module)
    
    #     exec(string,locals(),globals())

    # reload_all('config')