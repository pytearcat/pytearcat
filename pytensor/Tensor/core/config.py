from .core import Symbol, Function

# Quiero que las cosas se ejecuten en misc y pasarle el elemento listo a config para que lo guarde en las listas correspondientes
# la razon de esto es que si queremos guardar tensores, habría que hacer import de la clase tensor y tensorclass ya importa a config

def create_var(i):

    def_var = "%s = Symbol('%s', real=True)"%(i,i)
    exec(def_var,locals(),globals())
    
    append_str = "__all__.append('%s')"%i
    exec(append_str,globals())

    append_str = 'var.append(%s)'%i
    exec(append_str,globals())
    
    return var[-1]


def create_con(i):

    string = "%s = Symbol('%s', real=True, constant = True)"%(i,i)
    exec(string,locals(),globals())
    
    string = "__all__.append('%s')"%i
    exec(string,globals())

    string = 'con.append(%s)'%i
    exec(string,globals())

    return con[-1]


def create_fun(f_symbol,var_symbol):
    
    str5 = "%s=Function('%s', real=True)(%s)"%(f_symbol,f_symbol,var_symbol)

    exec(str5,locals(),globals())  

    assign = "__all__.append('%s')"%str(f_symbol)

    exec(assign,globals())

    assign = 'fun.append(%s)'%str(f_symbol)

    exec(assign,globals())

    return fun[-1]

def create_ten(T_name,T_obj):

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

fun = [] # Lista con funciones de tipo sympy

# Tensores tipicos -------- # Proteger estos nombres para que no puedan ser sobreescritos. Que newten arroje error 

g = None  # Metrica

christ = None  # Christoffel

riemann = None # Riemann

ricci = None # Ricci Tensor

ricciS = None # Ricci Scalar

G = None # Einstein Tensor

LeviCivita_Symbol = None # LeviCivita Symbol

LeviCivita_Tensor = None # LeviCivita Tensor

default_tensors = {'Christoffel' : '\Gamma' , 'Einstein' : 'G', 'Riemann': 'R', 'Ricci' : 'R', 'RicciS' : 'R'}

# ----------------------------

ten = [] # Lista de objetos de clase Tensor

temp = []

temp_name = []

# Order  (epsilon)

ord_status = False

ord_var = ''

ord_n = 0

# Greek Alphabet

greek = [r'\alpha',  r'\beta', r'\gamma', r'\delta',r'\mu', r'\nu', r'\rho',r'\sigma',r'\tau', r'\omega', r'\kappa', r'\lambda', r'\epsilon', r'\eta',  r'\theta', r'\iota',r'\zeta', r'\omicron', r'\pi', r'\upsilon',r'\phi',r'\chi',r'\psi']

greek_dict = {'alpha' : r'\alpha', 'beta' : r'\beta', 'gamma' : r'\gamma', 'delta': r'\delta', 'mu' : r'\mu', 'nu' : r'\nu', 'rho' : r'\rho', 'sigma' : r'\sigma', 'tau' : r'\tau', 'omega' : r'\omega', 'kappa' : r'\kappa', 'lambda' : r'\lambda', 'epsilon' : r'\epsilon', 'eta' : r'\eta', 'theta' : r'\theta', 'iota': r'\iota', 'zeta' : r'\zeta', 'omicron' : r'\omicron', 'pi' : r'\pi', 'upsilon' : r'\upsilon', 'phi': r'\phi', 'chi': r'\chi', 'psi' : r'\psi',\
    'Alpha' : r'\Alpha', 'Beta' : r'\Beta', 'Gamma' : r'\Gamma', 'Delta': r'\Delta', 'Mu' : r'\Mu', 'Nu' : r'\Nu', 'Rho' : r'\Rho', 'Sigma' : r'\Sigma', 'Tau' : r'\Tau', 'Omega' : r'\Omega', 'Kappa' : r'\Kappa', 'Lambda' : r'\Lambda', 'Epsilon' : r'\Epsilon', 'Eta' : r'\Eta', 'Theta' : r'\Theta', 'Iota': r'\Iota', 'Zeta' : r'\Zeta', 'Omicron' : r'\Omicron', 'Pi' : r'\Pi', 'Upsilon' : r'\Upsilon', 'Phi' : r'\Phi', 'Chi' : r'\Chi', 'Psi' : r'\Psi'}

__all__ = ['g','christ','riemann','ricci','ricciS','G']