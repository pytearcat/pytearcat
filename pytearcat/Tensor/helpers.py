from itertools import product as iterprod
from .core import core, config
from .misc import new_ten, setorder
from .tensor_class import ordenar,construct
#from .LeviCivita import values, LeviCivita

def tdata_construct(elem,dim,n):

    string = ('%s,'%elem)*dim

    string = '['+string[:-1]+'],'

    for k in range(n-1):

        string = '['+(string*(dim))[:-1]+'],'  

    string = '[' + (string*(2**n))[:-1]+']'

    return eval(string)

# def LeviCivita():
    
#     '''
#     LeviCivita Symbol.

#     By default as the spatial coordinates permutations i,j,k...

#     If time == True then it corresponds to the space-time coordinates permutations.
    
#     '''

#     rank = config.dim

#     Ten = LeviCivita()

#     vals, order = values(rank,rank)

#     for i,j in enumerate(order):

#         iterstring = '[0][' + ']['.join(j.astype(str)) + ']' 

#         string = 'Ten.tensor%s = vals[%d]'%(iterstring,i)

#         exec(string,locals(),globals())


#     for k in range(1,rank):

#         string = 'Ten.tensor[%d] = Ten.tensor[0]'%k

#         exec(string,locals(),globals())

#     rank = rank - 1

#     vals, order = values(rank,rank)

#     for i,j in enumerate(order):

#         iterstring = '[0][' + ']['.join(j.astype(str)) + ']' 

#         string = 'Ten.tensor_sp%s = vals[%d]'%(iterstring,i)

#         exec(string,locals(),globals())

#     for k in range(1,rank):

#         string = 'Ten.tensor_sp[%d] = Ten.tensor_sp[0]'%k

#         exec(string,locals(),globals())


#     return Ten

def KroneckerDelta(name='KroneckerDelta'):
    
    '''
    Kronecker Delta considered as a rank 2 tensor.
    
    '''
    
    dim = config.dim
    
    Ten = new_ten(name,2)
    
    Eye = core.eye(dim)
    
    Ten.assign(Eye.tolist(),'_,_')
    Ten.assign(Eye.tolist(),'^,_')
    Ten.assign(Eye.tolist(),'_,^')
    Ten.assign(Eye.tolist(),'^,^')
    
    Ten.space()
    
    return Ten

