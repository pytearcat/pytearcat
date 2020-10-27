from tqdm import tqdm_notebook
from itertools import product as iterprod
from pytensor.Tensor.misc import new_ten,reload_all
from pytensor.Tensor.core import config
from pytensor.Tensor.core.core import diff, Rational, sympify, factor, display, Latex, Math
from pytensor.Tensor.tensor_class import tensor_series

def D(element,i):

    '''
    Hasta ahora esta funcion deriva cualquier cosa del tipo "MutableDenseNDimArray" con respecto a una sola coordenada, ingresada en forma de numero.
    '''

    coord_index = config.coords

    # FIRST CASE: VECTOR DERIVATIVE WITH RESPECT TO ONE COORDINATE  d/dx^m Tensor[_i,^j,^k,_l,...etc]
    # WHERE x^m CORRESPOND TO i

    exec(reload_all('config'),globals(),locals()) # Import all the variables from config

    if type(i) == int:

        #coordinate = sympify(coord_index[i])

        str12 = "valor = diff(element,%s)"%(str(coord_index[i]))

        #str12 = "valor = diff(element,%s)"%str(coord_index[i])

        #str12 = str12.replace('XXXX',str(coordinate))

        #str12 = str12.replace('XXXX',str(coord_index[i]))

        exec(str12,locals(),globals())

        return valor

    else:

        print("ERROR IN THE DERIVATIVE D OF A TENSOR")


def calculate_christoffel(First_kind=True,Second_kind=True):
    
    global Christoffel
    
    g = config.g
    var = list(config.coords.values())
    dim = config.dim
    ord_status = config.ord_status
    coords = config.coords

    

    if config.christ is None:

        Christoffel = new_ten('Christoffel',3)

        config.christ = Christoffel

    else:

        Christoffel = config.christ

    # True if the first kind (second kind) symbol is already calculated. False if not.

    calc_fk = Christoffel.indexes[0] 

    calc_sk = Christoffel.indexes[4]

    

    description = r'Christoffel '

    if First_kind == True and Second_kind==True:

        if calc_fk == True:

            description += r'$\Gamma^{\alpha}_{\beta \gamma}$'

        elif calc_sk == True:

            description += r'$\Gamma_{\alpha \beta \gamma}$'

        else:

            description += r'$\Gamma_{\alpha \beta \gamma}$ and $\Gamma^{\alpha}_{\beta \gamma}$'

    elif First_kind == True:

        description += r'$\Gamma_{\alpha \beta \gamma}$'

    elif Second_kind == True:

        description += r'$\Gamma^{\alpha}_{\beta \gamma}$'

    coord_index = coords
    exec(reload_all('config'),globals(),locals()) # Import all the variables from config


    # Check if the program really needs to calculate a Christoffel Symbol

    if First_kind == False and Second_kind == False:

        print('You need to ask for at least one kind of Christoffel Symbol.')

        return Christoffel
    

    elif calc_fk == True and First_kind == True and Second_kind == False:

        #print('First Kind Christoffel already calculated.')

        display(Latex(r"First Kind Christoffel Symbol $\Gamma_{\alpha \beta \gamma}$ already calculated"))

        return Christoffel

    elif calc_sk == True and Second_kind == True and First_kind == False:

        #print('Second Kind Christoffel already calculated.')

        display(Latex(r"Second Kind Christoffel Symbol $\Gamma^{\alpha \beta \gamma}$ already calculated"))

        return Christoffel

    elif calc_fk == True and calc_sk == True:

        #print('First and Second kind Christoffel already calculated.')

        display(Latex(r"First and Second Kind Christoffel Symbol $\Gamma_{\alpha \beta \gamma}$ and $\Gamma^{\alpha \beta \gamma}$ already calculated"))

        return Christoffel


    for p in tqdm_notebook(iterprod(range(dim),repeat=3),total=dim**3,desc= description):

        if p[2] >= p[1]:

            countm = p[0]
            counti = p[1]
            countj = p[2]
            
            if First_kind==True and not(calc_fk):  #First Kind ('_,_,_')

                FirstTemp = Rational(1,2)*(diff(g.tensor[0][countm][countj],var[counti])+diff(g.tensor[0][countm][counti],var[countj])-diff(g.tensor[0][counti][countj],var[countm]))
                
                if ord_status == True:
                    
                    Christoffel.tensor[0][countm][counti][countj] = tensor_series(FirstTemp)

                else:

                    Christoffel.tensor[0][countm][counti][countj] = sympify(factor(FirstTemp))

                # Simetria
                Christoffel.tensor[0][countm][countj][counti] = Christoffel.tensor[0][countm][counti][countj]

                Christoffel.indexes[0] = True

            if Second_kind==True and not(calc_sk):  #Second Kind ('^,_,_')
                
                SecondTemp = 0
                    
                for countk in range(dim):
                        
                    SecondTemp += Rational(1,2)*g.tensor[3][countk][countm]*(diff(g.tensor[0][counti][countk],var[countj]) + diff(g.tensor[0][countj][countk],var[counti]) - diff(g.tensor[0][counti][countj],var[countk]) )
                
                if ord_status == True:

                    Christoffel.tensor[4][countm][counti][countj] = tensor_series(SecondTemp)

                else:

                    Christoffel.tensor[4][countm][counti][countj] = sympify(factor(SecondTemp))

                # Simetria
                Christoffel.tensor[4][countm][countj][counti] = Christoffel.tensor[4][countm][counti][countj]

                Christoffel.indexes[4] = True

    Christoffel.space()

    return Christoffel