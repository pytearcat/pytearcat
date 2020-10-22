from core import Rational, sympify, factor, display, Latex
import tqdm
from itertools import product
from misc import new_ten,reload_all
from riemann import calculate_riemann
from ricci import calculate_ricci, calculate_ricci_scalar
import config
from tensor_class import construct
from tensor_class import tensor_series

def calculate_einstein_tensor(All = False):

    global Einstein

    dim = config.dim

    g = config.g.tensor

    if config.G is None:

        Einstein = new_ten('Einstein',2)

        config.G = Einstein


    else:

        Einstein = config.G

    if config.ricci is None:

        Ricci_local = calculate_ricci()

    else: 

        Ricci_local = config.ricci
    
    if config.ricciS is None:

        R = calculate_ricci_scalar()
    
    else:

        R = config.ricciS

        
    #---

    if Einstein.indexes[0] == False:

        Einstein_list = construct('False',dim,2)

        for p in tqdm.tqdm_notebook(product(range(config.dim),repeat=2),total=config.dim**2,desc= r'Einstein Tensor $G_{\alpha \beta}$'):

            m = p[0]
            n = p[1]

            if Einstein_list[m][n] == False:

                EinstTemp = Ricci_local.tensor[0][m][n] - Rational(1,2)*(g[0][m][n])*R.tensor

                if config.ord_status == True:

                    Einstein.tensor[0][m][n] = tensor_series(EinstTemp)

                else:

                    Einstein.tensor[0][m][n] = sympify(factor(EinstTemp))

                Einstein_list[m][n] = True

                # Simmetry

                Einstein.tensor[0][n][m] = Einstein.tensor[0][m][n]

                Einstein_list[n][m] = True

        Einstein.indexes[0] = True

    else:

        display(Latex(r"Einstein Tensor $G_{\alpha \beta}$ already calculated"))

    if All == True:

        Einstein.indexcomb('_,_')

    Einstein.space()

    return Einstein