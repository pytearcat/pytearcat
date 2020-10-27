from tqdm import tqdm_notebook
from itertools import product as iterprod 

from pytensor.Tensor.misc import new_ten,reload_all
from pytensor.Tensor.core.core import sympify, factor, display, Latex, Math
from pytensor.Tensor.core import config
from pytensor.Tensor.tensor_class import construct, tensor_series

from .christoffel import calculate_christoffel, D

def calculate_riemann(default = True, All = False):

    # Riemann (_,_,_,_)

    global Riemann

    dim = config.dim

    if config.riemann is None:

        Riemann = new_ten('Riemann',4)

        config.riemann = Riemann

    else:

        Riemann = config.riemann

    if config.christ is None:

        Christ_local = calculate_christoffel()

    else:

        Christ_local = config.christ
    
    Ch1 = Christ_local.tensor[0][:][:][:] # First kind Christoffel
    Ch2 = Christ_local.tensor[4][:][:][:] # Second Kind Christoffel

    gmet = config.g.tensor

    if Riemann.indexes[0] == False and default == False:

        Riemann_list = construct('False',dim,4)
        
        Riem0 = Riemann.tensor[0]

        #wolfram alpha = counta ; beta = countb ; gamma = countc ; delta = countd

        for p in tqdm_notebook(iterprod(range(dim),repeat=4),total=dim**4,desc= r'Riemann Tensor $R_{\alpha \beta \gamma \delta}$'):

            counta = p[0]
            countb = p[1]
            countc = p[2]
            countd = p[3]

            if Riemann_list[counta][countb][countc][countd] == False:

                Value = 0
                Right = 0

                for countk in range(dim):

                    Value += (gmet[0][counta][countk]*(D(Ch2[countk][countb][countd],countc) - D(Ch2[countk][countb][countc],countd)))#.simplify()

                    Right += (Ch2[countk][countb][countd]*Ch1[counta][countk][countc] - Ch2[countk][countb][countc]*Ch1[counta][countk][countd])#.simplify()

                Rie_val = sympify(factor((Value + Right)))#.simplify()

                if config.ord_status == True:

                    Riem0[counta][countb][countc][countd] = tensor_series(Rie_val)

                else:

                    Riem0[counta][countb][countc][countd] = Rie_val

                Riemann_list[counta][countb][countc][countd] = True 

                # Skew Symmetry

                if Riemann_list[counta][countb][countd][countc] == False:

                    #print('Skew1',[counta,countb,countc,countd],[counta,countb,countd,countc])

                    Riem0[counta][countb][countd][countc] = -Riem0[counta][countb][countc][countd]

                    Riemann_list[counta][countb][countd][countc] = True

                if Riemann_list[countb][counta][countc][countd] == False:
                    
                    #print('Skew2',[counta,countb,countc,countd],[countb,counta,countc,countd])

                    Riem0[countb][counta][countc][countd] = -Riem0[counta][countb][countc][countd]

                    Riemann_list[countb][counta][countc][countd] = True

                # Interchange Symmetry

                if Riemann_list[countc][countd][counta][countb] == False:
                    
                    #print('Interchange',[counta,countb,countc,countd],[countc,countd,counta,countb])

                    Riem0[countc][countd][counta][countb] = Riem0[counta][countb][countc][countd]

                    Riemann_list[countc][countd][counta][countb] = True

                # Bianchi Identity (First)

                if Riemann_list[counta][countc][countd][countb] == False and Riemann_list[counta][countd][countb][countc] == True:

                    #print('Bianchi1',[counta,countb,countc,countd],[counta,countc,countd,countb])

                    Riem0[counta][countc][countd][countb] = -Riem0[counta][countb][countc][countd] - Riem0[counta][countd][countb][countc]

                    Riemann_list[counta][countc][countd][countb] = True

                if Riemann_list[counta][countd][countb][countc] == False and Riemann_list[counta][countc][countd][countb] == True:
                    
                    #print('Bianchi2',[counta,countb,countc,countd],[counta,countd,countb,countc])

                    Riem0[counta][countd][countb][countc] = -Riem0[counta][countb][countc][countd] - Riem0[counta][countc][countd][countb]

                    Riemann_list[counta][countd][countb][countc] = True

        Riemann.indexes[0] = True

    #######################################

    if Riemann.indexes[8] == False:

        Riemann_list = construct('False',dim,4)

        Riem8 = Riemann.tensor[8]
        #wolfram alpha = counta ; beta = countb ; gamma = countc ; delta = countd

        for p in tqdm_notebook(iterprod(range(dim),repeat=4),total=dim**4,desc= r'Riemann Tensor $R^{\alpha}_{\beta \gamma \delta}$'):

            counta = p[0]
            countb = p[1]
            countc = p[2]
            countd = p[3]

            #print(Riemann_list)

            if Riemann_list[counta][countb][countc][countd] == False:

                Rie_val = 0

                Value = D(Ch2[counta][countb][countd],countc) - D(Ch2[counta][countb][countc],countd)

                Right = 0

                for count_mu in range(dim):

                    Right += Ch2[count_mu][countb][countd]*Ch2[counta][count_mu][countc] - Ch2[count_mu][countb][countc]*Ch2[counta][count_mu][countd]
                
                Rie_val = Value + Right


                if config.ord_status == True:

                    Riem8[counta][countb][countc][countd] = tensor_series(Rie_val)

                else:

                    Riem8[counta][countb][countc][countd] = sympify(factor(Rie_val))

                Riemann_list[counta][countb][countc][countd] = True 
                
                # Skew Symmetry
            
                if Riemann_list[counta][countb][countd][countc] == False:

                    #print('Skew1')

                    Riem8[counta][countb][countd][countc] = -Riem8[counta][countb][countc][countd]

                    Riemann_list[counta][countb][countd][countc] = True

        Riemann.indexes[8] = True

    else:

        display(Latex(r"Riemann Tensor $R_{\alpha \beta \gamma \delta}$ already calculated"))

    if All == True:

        Riemann.indexcomb('_,_,_,_')

    Riemann.space()

    return Riemann