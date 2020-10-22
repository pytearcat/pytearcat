from tqdm import tqdm_notebook
from itertools import product as iterprod
from christoffel import calculate_christoffel
from core import sympify, factor, diff
from misc import new_var, new_fun
import config
from tensor_class import tensor_series

def geodesic():

    global geo

    dim = config.dim

    coords = config.geocoords

    if config.geo is None:

        geo = []

        config.geo = geo

    else:

        print("Geodesic already calculated.")

        geo = config.geo

        return geo, coords

    if config.christ is None:

        Christ_local = calculate_christoffel()

    else:

        Christ_local = config.christ
    
    Ch2 = Christ_local.tensor[4][:][:][:] # Second Kind Christoffel

    s = new_var('s') # proteger la variable s
    
    confcoords = list(config.coords.values())

    for i, elem in enumerate(confcoords):
        
        coords[elem] = new_fun('x__%d'%i,'s')

    geocoords = list(coords.values())

    for i,j,k in tqdm_notebook(iterprod(range(dim),repeat=3),total=dim**3):

        if (j+k) == 0:

            result = diff(geocoords[i],s,2)
        
        result += Ch2[i][j][k] * diff(geocoords[j],s) * diff(geocoords[k],s)

        if (j+k) == 2*(dim-1):

            if config.ord_status == True:

                result = tensor_series(result)

            else:

                result = sympify(factor(result))

            geo.append(result)

    return geo, coords



