from itertools import product as iterprod
from .core import core, config
from .misc import new_ten, setorder
from .tensor_class import ordenar,construct

def tdata_construct(elem,dim,n):

    string = ('%s,'%elem)*dim

    string = '['+string[:-1]+'],'

    for k in range(n-1):

        string = '['+(string*(dim))[:-1]+'],'  

    string = '[' + (string*(2**n))[:-1]+']'

    return eval(string)

def LeviCivita(name='LeviCivita'):
    
    '''
    LeviCivita Symbol.

    By default as the spatial coordinates permutations i,j,k...

    If time == True then it corresponds to the space-time coordinates permutations.
    
    '''

    rank = config.dim

    Ten = new_ten(name,rank)

    iterstring = ''
    Larg = ''
    
    for i in range(rank):
            
        iterstring += '[p[%d]]'%i
        Larg += 'p[%d],'%i
    
    Larg = Larg[:-1]
    
    for k in range(2**rank):

        for p in iterprod(range(rank), repeat = rank):
            
            string = 'Ten.tensor[k]%s = core.LeviCivita(%s)'%(iterstring,Larg)
            
            exec(string,locals(),globals())

    rank = rank - 1

    
    Ten.tensor_sp = tdata_construct(0,rank,rank)

    iterstring = ''
    Larg = ''
    
    for i in range(rank):
            
        iterstring += '[p[%d]]'%i
        Larg += 'p[%d],'%i
    
    Larg = Larg[:-1]


    
    for k in range(2**rank):

        for p in iterprod(range(rank), repeat = rank):

            string = 'Ten.tensor_sp[k]%s = core.LeviCivita(%s)'%(iterstring,Larg)
            
            exec(string,locals(),globals())

    return Ten

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

