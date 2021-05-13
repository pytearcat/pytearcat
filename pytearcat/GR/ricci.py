import numpy as np 
import tqdm
from itertools import product as iterprod 

from pytearcat.tensor.misc import new_ten,reload_all
from pytearcat.tensor.core import config
from pytearcat.tensor.tensor import tensor_series, Tensor

from .christoffel import calculate_christoffel, D
from .riemann import calculate_riemann

from pytearcat.tensor.core.core import core_calc,display_IP,Latex_IP

if core_calc == 'sp':

    from pytearcat.tensor.core.core import diff, sympify, factor

elif core_calc == 'gp':

    from pytearcat.tensor.core.core import diff, simplify

def calculate_ricci(All = False):

    # Ricci Tensor

    global Ricci


    if config.ricci is None:

        Ricci = config.create_ten('Ricci',Tensor('Ricci',2))

        config.ricci = Ricci

    else: 

        Ricci = config.ricci


    if config.riemann is None:

        Riemann_local = calculate_riemann()

    else:

        Riemann_local = config.riemann
   


    if Ricci.indexes[0] == False:

        Ricci_list = np.full((config.dim,config.dim), False, dtype=bool)

        display_IP(Latex_IP(r'Ricci Tensor $R_{\alpha \beta}$'))

        for p in tqdm.tqdm_notebook(iterprod(range(config.dim),repeat=2),total=config.dim**2):

            i = p[0]
            j = p[1]


            if Ricci_list[i][j] == False:

                Temp_Ricci = 0

                for k in range(config.dim):

                    Temp_Ricci += Riemann_local.tensor[8][k][i][k][j]

                if config.ord_status == True:

                    Ricci.tensor[0][i][j] = tensor_series(Temp_Ricci)

                else:

                    if core_calc == 'sp':

                        Ricci.tensor[0][i][j] = sympify(factor(Temp_Ricci))

                    elif core_calc == 'gp':

                        Ricci.tensor[0][i][j] = simplify(Temp_Ricci)

                # Simetrias

                Ricci_list[i][j] = True

                Ricci.tensor[0][j][i] = Ricci.tensor[0][i][j] # Simetria de Ricci

                Ricci_list[j][i] = True

        Ricci.indexes[0] = True

    else:

        display_IP(Latex_IP(r"Ricci Tensor $R_{\alpha \beta}$ already calculated"))

    if All == True:

        Ricci.indexcomb('_,_')

    Ricci.space()

    return Ricci



def calculate_ricci_scalar():

    global Ricci_Scalar

    if config.ricciS is None:

        Ricci_Scalar = config.create_ten('RicciS',Tensor('RicciS',0))

        config.ricciS = Ricci_Scalar
    
    else:

        display_IP(Latex_IP(r"Ricci Scalar $R$ already calculated"))

        return config.ricciS

    if config.ricci is None:

        Ricci_local = calculate_ricci()
    
    else:

        Ricci_local = config.ricci

    display_IP(Latex_IP(r'Ricci Scalar $R$'))

    for p in tqdm.tqdm_notebook(iterprod(range(config.dim),repeat=2),total=config.dim**2):

        i = p[0]
        j = p[1]

        Ricci_Scalar.tensor += config.g.tensor[3][i][j] * Ricci_local.tensor[0][i][j]

    if config.ord_status == True:

        Ricci_Scalar.tensor = tensor_series(Ricci_Scalar.tensor)


    else:

        if core_calc == 'sp':

            Ricci_Scalar.tensor = sympify(factor(Ricci_Scalar.tensor))

        elif core_calc == 'gp':

            Ricci_Scalar.tensor = simplify(Ricci_Scalar.tensor)

    return Ricci_Scalar