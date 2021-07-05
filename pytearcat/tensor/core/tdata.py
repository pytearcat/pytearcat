from .core import *
from pytearcat.tensor.core import config
from itertools import product as iterprod
from .interp import add_examine, mul_examine

def reload_all(new_module):

    ''' x

    This function reloads all the variables in __all__ from module
        
    Thanks to hurturk on https://stackoverflow.com/questions/44492803/python-dynamic-import-how-to-import-from-module-name-from-variable?newreg=9312458d429647fc8ec2a72e5655d197
        
    '''

    string = "globals().update({{n: getattr(module, n) for n in module.__all__}} if hasattr(module, '_all_') else {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')})"

    string = string.replace('module',new_module)

    return string

def out_intersection(L1,I1,L2,I2):
    '''
    example: not_intersection(conf_vars,new_vars)

    retorna las variables que no son compartidas en L1 y L2
    '''
    L = L1+L2
    
    I = I1+I2

    lista_intersection = [i for i in L2 if i in L1]

    lista = [x for x in L if x not in lista_intersection]

    out = {lista[i] : i for i in range(len(lista))}

    ind_dict =  dict((k,i) for i,k in enumerate(L))

    ind_out = [ I[ind_dict[x]] + L[ind_dict[x]] for x in out ]

    string = ','.join(ind_out)

    return out, string

def in_intersection(L1,I1,L2,I2):

    '''
    example: in_intersection(conf_vars,new_vars)  ['^i','_j'] ['_i','^l']

    ['i','j','i','l']

    retorna un diccionario con la interseccion
    '''

    L = L1+L2
    
    I = I1+I2

    lista_intersection = [i for i in L2 if i in L1]

    in_dict = {lista_intersection[i] : i for i in range(len(lista_intersection))}

    full_rep = []

    for i in range(len(L)):

        if L[i] in lista_intersection:

            full_rep.append('%s%s'%(I[i],L[i]))

    return in_dict, full_rep

def construct(elem,dim,n):
    
    '''
    It builds a nested list filled with elem on every item. 
    It returns an object with shape (dim,dim,dim,...,dim) of n entries.
    elem must be a string and you can recover each elem by using result[i][j][k] with i,j,k integers < dim
    '''
    
    string = ('%s,'%elem)*dim

    string = '['+string[:-1]+'],'

    for k in range(n-1):

        string = '['+(string*dim)[:-1]+'],' 
    
    return eval(string[:-1])

class Tdata:

    '''
    A class to represent the data of a Tensor.
    

    ...

    Attributes 
    -----------

    str_index : str
        String indicating the corresponding index combination of the Tensor, i.e. "^i,_j"

    elements : list or array
        list containing the data elements of the corresponding index combination.

    Methods
    ----------
    factor():
        Factors the Tensor data
    
    simplify():
        Simplifies the Tensor data
    

    '''

    def __init__(self,str_index,elements):

        
        self.full_index = str_index # '^i,_j' 

        self.full_list = self.full_index.split(',')
        
        self.updn = [symbol[0] for symbol in self.full_list]
            
        self.index_names = [symbol[1:] for symbol in self.full_list]
            
        self.elements = elements # T

    def __getitem__(self,item):

        return self.elements[item]

    def auto_sum(self):

        '''
        recibe tdata

        se fija en el index_names y busca los indices repetidos. Suma sobre si mismo una sola vez.
        Un solo indice repetido

        '''

        exec(reload_all('config'),locals(),globals())

        if config.space_time == True:

            dim = config.dim

        else:

            dim = config.dim - 1

        # AGREGAR UN EXAMINE PARA AUTO_SUM

        lista = self.index_names

        rep = False

        #print('en el auto_sum',self.full_list)

        for i,name_i in enumerate(lista):

            for j,name_j in enumerate(lista):

                if name_i == name_j and i != j:

                    pos_i,pos_j = i,j

                    rep = True
                    #print(pos_i,pos_j,name_i,name_j)

                    break

        self_index = ''

        return_index = ''

        full_index = ''

        k = 0

        if rep == True: # Si encuentra un indice repetido

            for i in range(len(self.updn)):

                if i == pos_i or i == pos_j:
                
                    self_index += '[q]'
                
                else:
                    
                    self_index += '[p[%d]]'%k

                    return_index += '[p[%d]]'%k

                    full_index += '%s,'%self.full_list[i]

                    k += 1

            full_index = full_index[:-1]

            return_tensor = construct(0,dim,len(self.updn)-2)

            for p in iterprod(range(dim),repeat=len(self.updn)-2): # for para ir asignarlo

                temp = 0

                for q in range(dim):

                    string = 'self.elements%s'%(self_index)

                    temp += eval(string,locals(),globals())
                
                string = 'return_tensor%s = temp'%return_index

                exec(string,locals(),globals())
                
            return Tdata(full_index,return_tensor)   #se retorna como el self

        else:

            return self



        
    def __mul__(self,other):

        exec(reload_all('config'),locals(),globals())

        if config.space_time == True:

            dim = config.dim

        else:

            dim = config.dim - 1
        
        if isinstance(other,Tdata):
        
            rep_index, rep_list = in_intersection(self.index_names,self.updn,other.index_names,other.updn)

            mul_examine(rep_list)

            new_index, return_string = out_intersection(self.index_names,self.updn,other.index_names,other.updn)

            new_rank = len(new_index)

            if new_rank != 0:
                
                return_tensor = construct(0,dim,new_rank)

            if len(rep_index) != 0: # Si hay indices repetidos

                new_iterstr = ''

                for i in range(new_rank):

                    new_iterstr += '[p[%d]]'%i

                self_iterstr = ''

                for i, name in enumerate(self.index_names):

                    if name in rep_index:

                        self_iterstr += '[q[%d]]'%rep_index[name]

                    else:

                        self_iterstr += '[p[%d]]'%new_index[name]

                other_iterstr = ''

                for i, name in enumerate(other.index_names):

                    if name in rep_index:

                        other_iterstr += '[q[%d]]'%rep_index[name]

                    else:

                        other_iterstr += '[p[%d]]'%new_index[name]

                if new_rank != 0:

                    for p in iterprod(range(dim),repeat=new_rank): # for para ir asignarlo

                        temp = 0

                        for q in iterprod(range(dim), repeat = len(rep_index)):

                            string = 'self.elements%s*other.elements%s'%(self_iterstr,other_iterstr)

                            temp += eval(string,locals(),globals())

                        string = 'return_tensor%s = temp'%new_iterstr

                        exec(string,locals(),globals())
                
                else:

                    temp = 0

                    for q in iterprod(range(dim), repeat = len(rep_index)):

                        string = 'self.elements%s*other.elements%s'%(self_iterstr,other_iterstr)

                        temp += eval(string,locals(),globals())

                    return temp

            else:

                return_string = '%s,%s'%(self.full_index,other.full_index)

                new_iterstr = ''

                for i in range(new_rank):

                    new_iterstr += '[p[%d]]'%i

                self_iterstr = ''

                k = 0

                while k < len(self.updn):

                    self_iterstr += '[p[%d]]'%k

                    k += 1

                other_iterstr = ''

                while k < len(self.updn)+len(other.updn):

                    other_iterstr += '[p[%d]]'%k
                    
                    k += 1

                for p in iterprod(range(dim),repeat=new_rank): # for para ir asignarlo

                    temp = 0
                    
                    string = 'self.elements%s*other.elements%s'%(self_iterstr,other_iterstr)

                    temp = eval(string,locals(),globals())

                    string = 'return_tensor%s = temp'%new_iterstr

                    exec(string,locals(),globals())

            return  Tdata(return_string,return_tensor)            

        else: # Not Tdata * Tdata

            same_rank = len(self.updn)
            
            return_tensor = construct(0,dim,same_rank)

            index = ''

            for i in range(same_rank):

                index += '[p[%d]]'%i

            for p in iterprod(range(dim),repeat = same_rank):

                string = 'return_tensor%s = self.elements%s*other'%(index,index)

                exec(string,locals(),globals())

            return Tdata(self.full_index,return_tensor)
        
    def __rmul__(self,other):

        exec(reload_all('config'),locals(),globals())

        if config.space_time == True:

            dim = config.dim

        else:

            dim = config.dim - 1

        same_rank = len(self.updn)
            
        return_tensor = construct(0,dim,same_rank)

        index = ''

        for i in range(same_rank):

            index += '[p[%d]]'%i

        for p in iterprod(range(dim),repeat = same_rank):

            string = 'return_tensor%s = self.elements%s*other'%(index,index)

            exec(string,locals(),globals())

        return Tdata(self.full_index,return_tensor)

    def __add__(self,other):

        exec(reload_all('config'),locals(),globals())

        if config.space_time == True:

            dim = config.dim

        else:

            dim = config.dim - 1

        add_examine(self.full_index,other.full_index)

        self_lista = self.full_index.split(',')
        other_lista = other.full_index.split(',')

        if set(self_lista) == set(other_lista): 

            self_index = ''
            other_index = ''

            for i in range(len(self.updn)):

                self_index += '[p[%d]]'%i

            for j in range(len(other.updn)):

                i = 0

                while other_lista[j][1:] != self_lista[i][1:]:

                    i += 1

                other_index += '[p[%d]]'%i

            return_tensor = construct(0,dim,len(self.updn))

            for p in iterprod(range(dim),repeat=len(self.updn)): # for para ir asignarlo

                temp = 0

                string = 'self.elements%s+other.elements%s'%(self_index,other_index)

                temp = eval(string,locals(),globals())

                string = 'return_tensor%s = temp'%self_index   # se ordena como el self

                exec(string,locals(),globals())
            
            return Tdata(self.full_index,return_tensor)   #se retorna como el self

        else:

            print('ERROR')

    def __sub__(self,other):

        exec(reload_all('config'),locals(),globals())

        if config.space_time == True:

            dim = config.dim

        else:

            dim = config.dim - 1

        self_lista = self.full_index.split(',')
        other_lista = other.full_index.split(',')

        if set(self_lista) == set(other_lista): 

            self_index = ''
            other_index = ''

            for i in range(len(self.updn)):

                self_index += '[p[%d]]'%i

            for j in range(len(other.updn)):

                i = 0

                while other_lista[j][1:] != self_lista[i][1:]:

                    i += 1

                other_index += '[p[%d]]'%i

            return_tensor = construct(0,dim,len(self.updn))

            for p in iterprod(range(dim),repeat=len(self.updn)): # for para ir asignarlo

                temp = 0

                string = 'self.elements%s - other.elements%s'%(self_index,other_index)

                temp = eval(string,locals(),globals())

                string = 'return_tensor%s = temp'%self_index   # se ordena como el self

                exec(string,locals(),globals())
            
            return Tdata(self.full_index,return_tensor)   #se retorna como el self

        else:

            print('error')

    def __truediv__(self,other):
        
        exec(reload_all('config'),locals(),globals())

        if config.space_time == True:

            dim = config.dim

        else:

            dim = config.dim - 1
        
        if not isinstance(other,Tdata):

            same_rank = len(self.updn)
            
            return_tensor = construct(0,dim,same_rank)

            index = ''

            for i in range(same_rank):

                index += '[p[%d]]'%i

            for p in iterprod(range(dim),repeat = same_rank):

                string = 'return_tensor%s = self.elements%s/other'%(index,index)

                exec(string,locals(),globals())

            return Tdata(self.full_index,return_tensor)

    def factor(self):

        '''
        Factor the Tensor data.
        '''

        self.elements = sympify(factor(self.elements))

    def simplify(self):

        '''
        Simplify the Tensor data.
        '''

        self.elements = sympify(simplify(np.array(self.elements)).tolist())