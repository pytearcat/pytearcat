import numpy as np 
import tqdm
from itertools import product as iterprod 

from pytensor.Tensor.core.core import sympify, factor, Latex, display
from pytensor.Tensor.misc import new_ten,reload_all
from pytensor.Tensor.core import config
from pytensor.Tensor.tensor_class import tensor_series

from .christoffel import calculate_christoffel, D
from .riemann import calculate_riemann

def calculate_ricci(All = False):

    # Ricci Tensor

    global Ricci


    if config.ricci is None:

        Ricci = new_ten('Ricci',2)

        config.ricci = Ricci

    else: 

        Ricci = config.ricci


    if config.riemann is None:

        Riemann_local = calculate_riemann()

    else:

        Riemann_local = config.riemann
   


    if Ricci.indexes[0] == False:

        Ricci_list = np.full((config.dim,config.dim), False, dtype=bool)

        for p in tqdm.tqdm_notebook(iterprod(range(config.dim),repeat=2),total=config.dim**2,desc=r'Ricci Tensor $R_{\alpha \beta}$'):

            i = p[0]
            j = p[1]


            if Ricci_list[i][j] == False:

                Temp_Ricci = 0

                for k in range(config.dim):

                    Temp_Ricci += Riemann_local.tensor[8][k][i][k][j]

                if config.ord_status == True:

                    Ricci.tensor[0][i][j] = tensor_series(Temp_Ricci)

                else:

                    Ricci.tensor[0][i][j] = sympify(factor(Temp_Ricci))

                # Simetrias

                Ricci_list[i][j] = True

                Ricci.tensor[0][j][i] = Ricci.tensor[0][i][j] # Simetria de Ricci

                Ricci_list[j][i] = True

        Ricci.indexes[0] = True

    else:

        display(Latex(r"Ricci Tensor $R_{\alpha \beta}$ already calculated"))

    if All == True:

        Ricci.indexcomb('_,_')

    Ricci.space()

    return Ricci



def calculate_ricci_scalar():

    global Ricci_Scalar

    if config.ricciS is None:

        Ricci_Scalar = new_ten('Ricci',0)

        config.ricciS = Ricci_Scalar
    
    else:

        display(Latex(r"Ricci Scalar $R$ already calculated"))

        return config.ricciS

    if config.ricci is None:

        Ricci_local = calculate_ricci()
    
    else:

        Ricci_local = config.ricci

    for p in tqdm.tqdm_notebook(iterprod(range(config.dim),repeat=2),total=config.dim**2,desc= r'Ricci Scalar $R$'):

        i = p[0]
        j = p[1]

        Ricci_Scalar.tensor += config.g.tensor[3][i][j] * Ricci_local.tensor[0][i][j]

    if config.ord_status == True:

        Ricci_Scalar.tensor = tensor_series(Ricci_Scalar.tensor)


    else:

        Ricci_Scalar.tensor = sympify(factor(Ricci_Scalar.tensor))

    return Ricci_Scalar