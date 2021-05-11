from itertools import product as iterprod
from pytearcat.tensor.core import config
from pytearcat.tensor.core.core import *
from pytearcat.tensor.misc import new_var, reload_all
from pytearcat.tensor.tensor_class import Tensor, tensor_series
from pytearcat.tensor.core.config import *

if core_calc == 'gp':

    import io
    from contextlib import redirect_stdout
    from pytearcat.tensor.core.display import gp_pretty_latex


def create_metric(ds2 = ''):

    global g

    if config.g_status == True:

        answer = input('The metric has already been defined. Do you want to overwrite it? (yes/no)')

        if answer == 'yes' or answer == 'y' or answer == 'Y' or answer == 'YES':

            print('The metric has been redefined. Standard tensors have been deleted.')

            config.g_status = False

            config.g = None

            config.christ = None

            config.ricci = None

            config.ricciS = None

            config.riemann = None

            config.G = None

            config.__all__.remove('g')

    if core_calc == 'sp':

        coords = ','.join(list(map(str,config.coords.values())))

    elif core_calc == 'gp':

        temp = ''

        for i in list(config.coords.values()):
            
            lol = "%s"%str(i)

            temp = temp[:] + lol[:] + ','
            
        coords = temp[:-1]

    g_matrix,line_element = metric(config.fun, coords, ds2)

    display_ds(g_matrix)
    
    if core_calc == 'gp':

        f = io.StringIO()
        with redirect_stdout(f):
            print(latex(matrix(g_matrix)))
        out = f.getvalue()

        out = out.replace(r"\\",r"\\\\").replace("\\text{","").replace("\"}\"","").replace('\"','').replace('\\}','}').replace('\\{','{')#.replace('\\\\','\\')

        display_IP(Math_IP(gp_pretty_latex(r"%s"%out)))

    elif core_calc == 'sp':

        display(Matrix(g_matrix))

    return config.g

def display_ds(gmatrix):

    dim = config.dim
    coords = config.coords.copy()
    greek = config.greek_dict

    for i in coords:

        if core_calc == 'sp':

            if str(coords[i]) in list(greek.keys()):

                coords[i] = greek[str(coords[i])]

        elif core_calc == 'gp':

            gpcoord = tolatex(coords[i]).replace("\\","")

            if gpcoord in list(greek.keys()):

                coords[i] = greek[gpcoord]

            del(gpcoord)

    ds = r'ds^2 = '

    for i,j in iterprod(range(dim),repeat=2):

        value = gmatrix[i,j]

        if value != 0:            

            if i == j:

                if core_calc == 'gp':

                    ds += r"\left(%s\right)*d%s^2+"%(tolatex(value),coords[i])

                elif core_calc == 'sp':

                    if value.is_Add:

                        ds += r"\left(%s\right)*d%s^2+"%(latex(value),coords[i])

                    else:
                    
                        ds += r"%s*d%s^2+"%(latex(value),coords[i])

            elif j > i:

                if core_calc == 'gp':

                    ds += r"\left(%s\right)*d%s*d%s+"%(tolatex(2*value),coords[i],coords[j])

                elif core_calc == 'sp':

                    if value.is_Add:

                        ds += r"\left(%s\right)*d%s*d%s+"%(latex(value*2),coords[i],coords[j])

                    else:

                        ds += r"%s*d%s*d%s+"%(latex(value*2),coords[i],coords[j])

    ds = ds[:-1]

    ds = ds.replace(r'+-',r'-')
    ds = ds.replace(r'++',r'+')
    ds = ds.replace(r'**',r'^')
    ds = ds.replace(r'*',r' \cdot ')

    if core_calc == 'gp':

        display_IP(Math_IP(gp_pretty_latex(ds)))
        
    elif core_calc == 'sp':

        display_IP(Math_IP(ds))
        

def metric(functions, coords, ds2):

    '''
    It creates the metric matrix. Receives te functions defined (as sympy functions),
    the coordinates separated by comma and the line element ds^2.
    '''   
    # if coords == '':

    #     # If the user does not enter the coordinates, it asks for them.
        
    #     variables_string = coordinates() 
    #     config.dim = len(variables_string.split(','))
    #     config.coords = coord_index(variables_string)
        
    # else:
        
    #     variables_string = coords
    #     config.dim = len(variables_string.split(','))
    #     config.coords = coord_index(variables_string)
    
    variables_string = coords

    if ds2 == '':
        
        ds2 = input('Enter the metric in the form: ds2=-dt*dt+a**2*(dx**2+dy**2+dz**2): \n' )
    
        config.ds = ds2 ####--!!! Guarda el string ds en el archivo config.
    
    print('\nDimension = %d'%config.dim)
    
    print('Coordinates = %s'%variables_string)
    
    g_matrix, line_element = create_metric_matrix(config.dim, variables_string, ds2)  

    print('Metric was defined successfully: \n')    
    
    return g_matrix, line_element

def create_metric_matrix(dim, variables_string, ds_input):
    
    # CREAMOS UNA VARIABLE POR CADA DIMENSION Y VERIFICAMOS QUE CALCEN, 
    # QUEDAN ASIGNADAS CON LAS LETRAS QUE SE INGRESARON COMO INPUT 
    
    for i in range(0,dim):

        COORDENADA = variables_string.split(',')

        if len(COORDENADA) != dim:
            print('ERROR: Number of coordinates and dimension are different')
            break

        # HERE WE CREATE THE DIFFERENTIAL COORDINATES WITH THE INPUT NAMES: e.g. dt,dx,dy,dz

        if core_calc == 'gp':

            string = "d%s = giac('d%s')" % (COORDENADA[i],COORDENADA[i])
        
        elif core_calc == 'sp':

            string = "d%s = Symbol('d%s')" % (COORDENADA[i],COORDENADA[i])

        exec(string,locals(),globals())
    
    #HERE WE ASSIGN A INDEX NUMBER TO EVERY COORDINATE CREATED BY DE USER 
    # IT IS ENUMERATED FROM 0 TO  DIM-1
    # THE INDEX COORDINATE CAN BE FOUND BY coord_index['x']
    
    exec(reload_all('config'),globals(),locals()) # Import all the variables from config

    # We execute the string ds3 that will define the line element for the metric
    
    exec(ds_input,locals(),globals())
    
    g_matrix=zeros(dim, dim)  #g_matrix=(row i, column j)

    c = config.coords
    
    for i,j in iterprod(range(dim),repeat=2):
        
        if core_calc == 'sp':

            factor='d%s*d%s'%(c[i],c[j])

            element = expand(ds2)
            
            coef = eval(r"element.coeff(%s)"%factor,locals(),globals())

            coef = nsimplify(coef)

        elif core_calc == 'gp':

            factor0='d%s'%c[i]
            factor1='d%s'%c[j]


        if i!=j:

            if core_calc == 'gp':

                coef = eval(r"simplify(coeff(coeff(ds2,%s,1),%s,1))"%(factor0,factor1),locals(),globals())


            g_matrix[i,j] =coef/2
            
        else:

            if core_calc == 'gp':

                coef = eval(r"simplify(coeff(ds2,%s,2))"%factor0,locals(),globals())

            g_matrix[i,j] =coef 
    
    g_matrix_inv = g_matrix.inv()

    if config.ord_status == True:

        for i,j in iterprod(range(dim),repeat=2):

            g_matrix[i,j] = tensor_series(g_matrix[i,j])
            g_matrix_inv[i,j] = tensor_series(g_matrix_inv[i,j])

    g = config.create_ten('g',Tensor('g',2))

    # SOLO EL TENSOR g uv TENDRA DOS OPCIONES DD Y UU, NO HAY DU Y UD PORQUE ESOS SIEMPRE SERAN IDENTIDAD, LUEGO
    if core_calc == 'gp':

        identidad = idn(dim)

    elif core_calc == 'sp':

        identidad = eye(dim)

    for p in iterprod(range(dim),repeat=2):

        i = p[0]
        j = p[1]

        if j >= i:

            g.tensor[0][i][j] = g_matrix[i,j]
            g.tensor[3][i][j] = g_matrix_inv[i,j]
            g.tensor[1][i][j] = identidad[i,j]
            g.tensor[2][i][j] = identidad[i,j]

            # Simetria
            g.tensor[0][j][i] = g.tensor[0][i][j]
            g.tensor[3][j][i] = g.tensor[3][i][j]
            g.tensor[1][j][i] = identidad[i,j]
            g.tensor[2][j][i] = identidad[i,j]
    
    config.g_status = True
    
    config.g = g

    config.g.space()
    
    return g_matrix, ds2



def ask_dim():
    
    config.dim = int(input("Enter a the dimension:\n"))

    return config.dim


def coord_index(coordinates):

    '''
    It defines a dictionary { 0 : 'x' , 1 : 'y' ...}
    
    '''

    dim = config.dim
    
    coord = coordinates.split(',')

    a = [None]*dim  # ARRAY OF INDEX
    b = [None]*dim  # ARRAY OF COORDINATES

    for i in range(0,dim):

        a[i] = i
        b[i] = new_var(coord[i])

    return dict(zip(a,b))


def coordinates():

    return input("Enter the coordinates separated by comma (,):\n")


def def_coords(coords=''):

    '''
    coords = 't,x,y,z'
    
    '''

    print('Remember that the time coordinate must be the first coordinate.')

    coordinates = []

    variables_string = coords

    config.dim = len(variables_string.split(','))

    config.coords = coord_index(variables_string)

    config.coords_sp = {i-1 : config.coords[i] for i in config.coords if i != 0}

    coordinates.append(new_var(*coords.split(',')))

    if len(coordinates) == 1:

        return coordinates[0]

    else:

        return coordinates
