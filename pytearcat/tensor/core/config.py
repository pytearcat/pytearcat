from .greek import *

from .core import core_calc
from .fun import fun
from .ptseries import *

if core_calc == 'sp':

    from .core import Symbol, Function

elif core_calc == 'gp':

    from .core import giac

# Quiero que las cosas se ejecuten en misc y pasarle el elemento listo a config para que lo guarde en las listas correspondientes
# la razon de esto es que si queremos guardar tensores, habría que hacer import de la clase tensor y tensorclass ya importa a config

def create_var(i):

    if core_calc == 'sp':

        def_var = "%s = Symbol('%s', real=True)"%(i,i)

    elif core_calc == 'gp':

        def_var = "%s = giac('%s')"%(i,i)

    exec(def_var,locals(),globals())
    
    append_str = "__all__.append('%s')"%i
    exec(append_str,globals())

    append_str = 'var.append(%s)'%i
    exec(append_str,globals())
    
    return var[-1]

def create_con(i):

    if core_calc == 'gp':

        string = "%s = giac('%s')"%(i,i)

    elif core_calc == 'sp':

        string = "%s = Symbol('%s', real=True, constant = True)"%(i,i)

    exec(string,locals(),globals())
    
    string = "__all__.append('%s')"%i
    exec(string,globals())

    string = 'con.append(%s)'%i
    exec(string,globals())

    return con[-1]

def create_fun(f_symbol,var_symbol):

    if core_calc == 'gp':

        str5 = "%s=giac('%s(%s)')"%(f_symbol,f_symbol,var_symbol)

    elif core_calc == 'sp':
    
        str5 = "%s=Function('%s', real=True, nonzero=True)(%s)"%(f_symbol,f_symbol,var_symbol)

    exec(str5,locals(),globals())  

    assign = "__all__.append('%s')"%str(f_symbol)

    exec(assign,globals())

    assign = 'fun.append(%s)'%str(f_symbol)

    exec(assign,globals())

    return fun[-1]


def create_default(T_name,T_obj):

    if T_name == 'Christoffel':

        christ = T_obj

        ten.append(christ)

    elif T_name == 'Riemann':

        riemann = T_obj

        ten.append(riemann)

    elif T_name == 'Ricci':

        ricci = T_obj

        ten.append(ricci)

    elif T_name == 'RicciS':

        ricciS = T_obj

        ten.append(ricciS)

    elif T_name == 'Einstein':

        G = T_obj

        ten.append(G)




def create_ten(T_name,T_obj):

    if T_name in default_tensors:

        create_default(T_name,T_obj)

    string = "%s = T_obj"%T_name
    exec(string,locals(),globals())

    string = "__all__.append('%s')"%str(T_name)
    exec(string,globals())

    string = 'ten.append(%s)'%T_name
    exec(string,globals())

    #Este return es para que retorne el objeto que quedo definido aca en config.

    return ten[-1]

def create_temp(name,obj):

    string = "%s = obj"%name
    exec(string,locals(),globals())

    string = "__all__.append('%s')"%str(name)
    exec(string,globals())

    string = "temp.append('%s')"%str(name)
    exec(string,globals())

    string = "temp_name.append('%s')"%str(name)
    exec(string,globals())

    #Este return es para que retorne el objeto que quedo definido aca en config.

    return temp[-1]

# Manifold dimension
dim = 0

# Defined Metric

g_status = False

ds = ''

coords = {}

coords_sp = {}

geo = None

geocoords = {}

space_time = True

var = [] # Lista con variables de tipo sympy

con = [] # Lista con constantes de tipo sympy

#fun = [] # Lista con funciones de tipo sympy

# Tensores tipicos -------- # Proteger estos nombres para que no puedan ser sobreescritos. Que newten arroje error 

g = None  # Metrica

christ = None  # Christoffel

riemann = None # Riemann

ricci = None # Ricci Tensor

ricciS = None # Ricci Scalar

G = None # Einstein Tensor

LeviCivita_Symbol = None # LeviCivita Symbol

LeviCivita_Tensor = None # LeviCivita Tensor

default_tensors = {'Christoffel' : '\Gamma' , 'Einstein' : 'G', 'Riemann': 'R', 'Ricci' : 'R', 'RicciS' : 'R','g':'g','G' :'G'}

# ----------------------------

ten = [] # Lista de objetos de clase Tensor

temp = []

temp_name = []

# Order  (epsilon)

#ord_status = False

#ord_var = ''

#ord_n = 0

__all__ = ['g','christ','riemann','ricci','ricciS','G','space_time']