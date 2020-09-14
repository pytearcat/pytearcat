from sympy import expand, latex, Matrix, nsimplify, sympify
from IPython.display import display, Math, Latex
import config
from misc import new_var,new_ten, n_order, reload_all
from tensor_class import Tensor, tensor_series
from itertools import product
from config import *
import symengine as se

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

    coords = ','.join([*config.coords.values()])

    g_matrix,line_element = metric(config.fun, coords, ds2)

    display_ds(g_matrix)
    
    display(Math(latex(sympify(Matrix(g_matrix)))))  

    return config.g

def display_ds(gmatrix):

    dim = config.dim
    coords = config.coords

    ds = r'ds^2 = '

    for p in product(range(dim),repeat=2):
    
        i = p[0]
        j = p[1]

        value = gmatrix[i,j]

        if value != 0:            

            if i == j:
                
                ds += r'%s*d%s^2+'%(latex(sympify(value)),coords[i])

            elif j > i:

                ds += r'%s*d%s*d%s+'%(latex(sympify(value*2)),coords[i],coords[j])

    ds = ds[:-1]

    ds = ds.replace(r'+-',r'-')
    ds = ds.replace(r'++',r'+')
    ds = ds.replace(r'**',r'^')
    ds = ds.replace(r'*',r' \cdot ')

    display(Math(ds))
        

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
        
    print('Metric was defined successfully: \n')
    
    print('Dimension = %d'%config.dim)
    
    print('Coordinates = %s'%variables_string)
    
    g_matrix, line_element = create_metric_matrix(config.dim, variables_string, ds2)      
    
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

        string = "d%s = se.Symbol('d%s')" % (COORDENADA[i],COORDENADA[i])
        
        exec(string,locals(),globals())
    
    #HERE WE ASSIGN A INDEX NUMBER TO EVERY COORDINATE CREATED BY DE USER 
    # IT IS ENUMERATED FROM 0 TO  DIM-1
    # THE INDEX COORDINATE CAN BE FOUND BY coord_index['x']
    
    exec(reload_all('config'),globals(),locals()) # Import all the variables from config

    # We execute the string ds3 that will define the line element for the metric
    
    exec(ds_input,locals(),globals())
    
    g_matrix=se.zeros(dim, dim)  #g_matrix=(row i, column j)

    c = config.coords
    
    for p in product(range(dim),repeat=2):
    
        i = p[0]
        j = p[1]

        factor='d%s*d%s'%(c[i],c[j])
        
        element = expand(ds2)

        coef = eval(r"element.coeff(%s)"%factor,locals(),globals())

        coef = se.sympify(nsimplify(coef))

        if i!=j:

            if config.ord_status == True:

                g_matrix[i,j] = tensor_series(coef/2)

            else:

                g_matrix[i,j] =coef/2
            
        else:

            if config.ord_status == True:

                g_matrix[i,j] = tensor_series(coef)

            else:

                g_matrix[i,j] =coef 

    g_matrix_inv = g_matrix.inv()

    g = new_ten('g',2)

    # SOLO EL TENSOR g uv TENDRA DOS OPCIONES DD Y UU, NO HAY DU Y UD PORQUE ESOS SIEMPRE SERAN IDENTIDAD, LUEGO
    
    identidad = se.eye(dim)

    for p in product(range(dim),repeat=2):

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
        b[i] = coord[i]

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
