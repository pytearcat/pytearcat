'''
Implementation of the 'Tensor' Class and helper functions
'''


import numpy as np 
from itertools import product as iterprod
from numpy import isin
from tqdm import tqdm_notebook
from warnings import warn
from .core import config
from .core.core import *
from .core.display import display
from .core.interp import syntax, add_examine, mul_examine, der_examine
from .core.tdata import Tdata, construct

if core_calc == 'gp':

    import io
    from contextlib import redirect_stdout
    from .core.display import gp_pretty_latex
    from .core.core import sp_simplify, sp_sympify, sp_latex, sp_Array

def reload_all(new_module):

    '''

    This function reloads all the variables in __all__ from module
        
    Thanks to hurturk on https://stackoverflow.com/questions/44492803/python-dynamic-import-how-to-import-from-module-name-from-variable?newreg=9312458d429647fc8ec2a72e5655d197
        
    '''

    string = "globals().update({{n: getattr(module, n) for n in module.__all__}} if hasattr(module, '_all_') else {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')})"

    string = string.replace('module',new_module)

    return string

def ordenar(n):

    '''
    Returns a list with all the possible combinations of indices for a tensor of n indices [['_','_'],['^','_'],['_','^'],['^','^']]
    '''

    return [','.join(i) for i in iterprod(['_','^'],repeat = n)]


class gError(Exception):

    pass

def compare(n,string):

    '''
    Returns de index corresponding to the element in the list of all the combination of indices that mathces string
    '''

    if n == 0:

        return None

    lista = ordenar(n)

    if string not in lista:

        raise ValueError('Bad index definition') # Verificar que se levante el error correcto

    for i in range(len(lista)):

        if lista[i] == string:

            return i # esto es un numero

        else:
            pass


def bajarindice(tensor,i,kstring,kstring2):

    '''
    tensor: Tensor object for which we want to lower their indices

    i: first position that has an upper index i.e. in a string of indices '_,^,^' -> i = 1 (counting from 0)

    kstring: original string containing the tensor indices e.g. '_,^,^'

    kstring2: target string (with the i string down) for the tensor indices e.g.  '_,_,^'

    TODO: This function should be implemented as a method of the tensor class
    '''

    index = compare(tensor.n,kstring)

    index2 = compare(tensor.n,kstring2)

    dim = config.dim

    greek = config.greek

    g = config.g.tensor

    NAME = tensor.name

    if NAME in config.default_tensors:

        NAME = config.default_tensors[NAME]

    #---

    iterstring = ''

    greek_desc = ''

    iterg = ''

    count2 = 0

    for count in range(tensor.n):

        if count == i:

            iterstring += '[j]'

            iterg += '[p[%d]][j]'%i

            count2 += 1

        else:

            iterstring += '[p[%d]]'%count2

            count2 += 1

    iterstring2 = ''

    for count in range(tensor.n):

        greek_desc += '{%s%s}'%(kstring2.split(',')[count],greek[count])

        iterstring2 += '[p[%d]]'%count

    #---

    description =  '%s Tensor $%s%s$'%(tensor.name,NAME,greek_desc)

    for p in tqdm_notebook(iterprod(range(dim),repeat=tensor.n),total=dim**tensor.n,desc= description):

        temporal = 0

        for j in range(dim):

            bla2 = 'g[0]%s*tensor.tensor[index]%s'%(iterg,iterstring)

            temporal += eval(bla2)

        if config.ord_status == True:

            bla = 'tensor.tensor[index2]%s = tensor_series(temporal)'%iterstring2 

        else:

            bla = 'tensor.tensor[index2]%s = temporal'%iterstring2       # Esto asigna a los indices que queremos llegar

        exec(bla,globals(),locals())

    tensor.indices[index2] = True



def subirindice(tensor,kstring):

    '''
    Receives 

    1) Tensor object for which we want to raise their indices

    2) string like '_,^,_'
    

    TODO: This function should be implemented as a method of the tensor class
    '''

    index = compare(tensor.n,kstring)

    klista = kstring.split(',') # ['_','^','_']

    NAME = tensor.name

    dim = config.dim

    greek = config.greek

    g = config.g.tensor

    if NAME in config.default_tensors:

        NAME = config.default_tensors[NAME]

    for i in range(len(klista)): # _,_

        klista2 = list(klista)

        if klista[i] == '_': # _,^ 

            klista2[i] = '^'

            kstring2 = ','.join(klista2)

            index2 = compare(tensor.n,kstring2) # numero correspondiente a '^,^' o '^,_' del tensor

            if tensor.indices[index2] == True: # si ya esta calculado no hace nada

                pass

            else:

                bla = ''

                iterstring = ''

                iterstring2 = ''

                greek_desc = ''

                iterg = ''

                cosa2 = 0

                for count in range(tensor.n):

                    greek_desc += '{%s%s}'%(klista2[count],greek[count])

                    iterstring2 += '[p[%d]]'%count

                    if count == i:

                        iterstring += '[j]'

                        iterg += '[p[%d]][j]'%i

                        cosa2 += 1

                    else:

                        iterstring += '[p[%d]]'%cosa2

                        cosa2 += 1

                description =  '%s Tensor $%s%s$'%(tensor.name,NAME,greek_desc)

                #---

                for p in tqdm_notebook(iterprod(range(dim),repeat=tensor.n),total=dim**tensor.n,desc= description):

                    temporal = 0

                    for j in range(dim):

                        bla2 = 'g[3]%s*tensor.tensor[index]%s'%(iterg,iterstring)

                        temporal += eval(bla2)

                    if config.ord_status == True:

                        bla = 'tensor.tensor[index2]%s = tensor_series(temporal)'%iterstring2 

                    else:

                        bla = 'tensor.tensor[index2]%s = temporal'%iterstring2      # Esto asigna a los indices que queremos llegar

                    #print('En subir indice\t', iterg, iterstring, iterstring2)

                    exec(bla,globals(),locals())

                    tensor.indices[index2] = True

            subirindice(tensor,kstring2)

def createfirstindex(tensor,kstring):

    '''
    tensor: object of tensor class for which we want get the full covariant form

    kstring: original string of the current indices of the tensor e.g. '^,_,_'

    TODO: This function should be implemented as a method of the tensor class
    '''

    N = tensor.n # Number of indices

    objetivo = tensor.sequence[0].split(',') # ['_','_','_']

    lista = kstring.split(',')  # ['^','_','_']

    for i in range(len(lista)):

        if lista[i] != '_':

            lista[i] = '_'

            kstring_new = ','.join(lista)

            bajarindice(tensor,i,kstring,kstring_new)

            kstring = kstring_new

class Tensor:

    """ Tensor Class

    The 'Tensor' class contains all the relevant information for a Tensor object. 

    Attributes
    ----------
    name : str
        name of the Tensor.
    n : int
        rank of the Tensor.
    dim :   int
        dimension of the Tensor.
    sequence : list
        a list containing all the possible combination of indices for the Tensor.
    indices : array_like
        an array containing Boolean values to indicate which combination of the indices were calculated.
    tensor : array_like
        an array containing each component of the tensor. Initialized with NaN values.
    tensor_sp : array_like
        an array containing only the spatial components of the tensor. Initialized with NaN values.
    
    Methods
    -------
    assign(elements,index=None, All = False, printing = True, spatial = None)
        It assigns the elements to the tensor on the corresponding indices combination. 
    complete(index)
        It calculates the missing indices combintation of the tensor raising and lowering the indices from the given indices combination.
    display(index=None, aslist = None, simplify = False, spatial=None)
        Displays the Tensor. By default it displays the tensor with all covariant indices unless index is given.
    series(index = None)
        Performs a series expanson on each component of the Tensor. If index is given, only acts on the given indices combination.
    simplify(index = None)
        Simplifies each component of the tensor. If index is given, only acts on the given indices combination.
    expand(index = None)
        Expands each component of the tensor. If index is given, only acts on the given indices combination.
    factor(index = None)
        Factorizes each component of the tensor. If index is given, only acts on the given indices combination.

    Raises
    ------
    ValueError
        If the rank of a tensor is not a positive integer. If the Dimension is undefined
    """
    
    
    

    def __init__(self,name,n):

        if n <= 0 or not isinstance(n,int):
            
            raise ValueError("The rank of a tensor (n) must be a positive integer.")

        dim = config.dim

        if dim == 0:

            raise ValueError('Dimension undefined')

        if name == 'g':

            if config.g == True:

                while True:

                    answer = input('Warning g is already defined as the metric tensor. Are you sure that you want to overwrite it?\nyes/no?')

                    if answer == 'yes' or answer == 'y' or answer == 'Yes':

                        print('g has been overwritten')

                        break

                    if answer == 'no' or answer == 'n' or answer == 'No':

                        raise gError

                    else:

                        print('Please try again.\n')

        self.name = name

        self.n = n

        self.sequence = ordenar(n)

        self.indices = np.full((2**n), False)

        if core_calc == 'sp':

            string = 'sympify(np.nan),'*dim

        elif core_calc == 'gp':
            
            string = 'np.nan,'*dim

        string = '['+string[:-1]+'],'

        for k in range(n-1):

            string = '['+(string*dim)[:-1]+'],'  

        string = 'self.tensor = [' + (string*(2**n))[:-1]+']'

        exec(string)

        if core_calc == 'sp':

            string = 'sympify(np.nan),'*(dim-1)

        elif core_calc == 'gp':
            
            string = 'np.nan,'*(dim-1)

        string = '['+string[:-1]+'],'

        for k in range(n-1):

            string = '['+(string*(dim-1))[:-1]+'],'  

        string = 'self.tensor_sp = [' + (string*(2**n))[:-1]+']'

        exec(string)

    def __repr__(self):

        return '%s tensor defined'%self.name

    def __str__(self):

        if self.n <=2:

            self.display()

            string = ''

        else:

            string = 'Too many tensor indices. Please use the display method.'
        
        return string

    def __scalar_call(self,updn,numbers,Nindex,ten_call):
    
        tdat_str = ''
        
        new_string_right = ''
        
        for i in numbers:
                
            new_string_right += '[%s]'%i
        
        return eval('self.%s[%s]%s'%(ten_call,Nindex,new_string_right))

    def __Tdata_call(self,updn,coord,numbers,Nindex,dim,ten_call):
    
        tdat_str = ''
        
        new_string_right = ''
        
        k = 0
        j = 0
        
        for i in range(len(updn)):
            
            if coord[i] not in numbers:
            
                tdat_str += updn[i] + coord[i] + ','
                
                new_string_right += '[p[%d]]'%k
                
                k += 1
                
            else: 
                
                new_string_right += '[%s]'%numbers[j]
                
                j += 1

        tdat_str = tdat_str[:-1]
                
                    
        new_rank = len(coord)-len(numbers)
        
        elements = construct(0,dim,new_rank)
        
        new_string_left = ''
        
        for k in range(new_rank):

            new_string_left += '[p[%d]]'%k
        
        
        for p in iterprod(range(dim), repeat = new_rank):

            exec_str = 'elements%s = self.%s[%s]%s'%(new_string_left,ten_call,Nindex,new_string_right)
        
            exec(exec_str,locals(),globals())

        data_result = Tdata(tdat_str,elements)

        TEMP = Tensor('TEMP',new_rank)

        TEMP.assign(data_result,tdat_str,printing=False)

        return TEMP(tdat_str)

    def __call__(self,str_index):

        '''Call Method for Tensor Class.

        Returns a Tdata object with the indices given as argument of the call.
        
        '''
        # Solo acepta a lo mas la contraccion de 1 solo indice. Hay que incluir esto en el examine de este call

        syntax(str_index,self.n)

        if config.space_time == 1:

            dim = config.dim

            ten_call = 'tensor'

        else:

            dim = config.dim - 1

            ten_call = 'tensor_sp'

        lista = str_index.split(',')

        updn = [symbol[0] for symbol in lista]

        coord = [symbol[1:] for symbol in lista]
        
        Nindex = compare(len(updn),(',').join(updn))

        repeated_coord = set([x for x in lista if coord.count(x[1:]) > 1])

        non_repeated_coord = set([x for x in lista if coord.count(x[1:]) == 1])

        numbers = []

        #if  in coords hay numeros, etonces error si any es > dim
        
        ErrorIndexAlphaNum = False
        ErrorIndexInt = False

        for i in coord:
            
            if (not i.isalnum()) or ("." in i):
                
                ErrorIndexAlphaNum= True
                
            try:
                
                if (int(i) >= dim) or (int(i) < 0):
                    
                    ErrorIndexInt = True
                    
            except:
                
                pass

            if ErrorIndexAlphaNum:
                
                raise SyntaxError("Wrong indices. Every index must be a name or a integer without any special characters.")
            
            elif ErrorIndexInt:
                
                raise SyntaxError("Wrong indices. Every index must be a name or a integer greater than 0 and less than the dimension.")
                


        for i in coord:

            if i in np.asarray([range(dim)],dtype=str):
                
                numbers.append(i)

        # if numbers esta bien, luego tiene que ir un elif len(numbers) != 0. En ese caso hay problemas
        # finalmente tiene que ir otro elif, que es si no tiene numeros. Este caso se dividira en si tiene o no indices repetidos.
                
        if len(numbers) == len(coord): # All numbered indices
            
            return self.__scalar_call(updn,numbers,Nindex,ten_call)

            
        if len(numbers) != 0: # Some numbered indices and letters


            ## Si hay numeros no suma indices repetidos
            ## En este caso se podría tener que retorne escalar, lo que puede terminar en error.
            
            return self.__Tdata_call(updn,coord,numbers,Nindex,dim,ten_call)

        for i in lista:

            if lista.count(i) > 1: 

                raise SyntaxError('Problem with the indices. Error in the Einstein summation.')


        if len(repeated_coord) == 0:

            elements = eval('self.%s[Nindex]'%ten_call,locals(),globals())

            return Tdata(str_index,elements)

        else: # Repeated Index

            new_string = ''

            old_string = ''

            return_string = ''

            new_rank = len(lista) - 2

            if new_rank != 0:

                temp = construct(0,dim,new_rank)

            k = 0
            rep_count = 0
            variable = ''

            for var in lista:

                if coord.count(var[1:]) == 2 and rep_count != 2:

                    if variable == var[1:] or variable == '':

                        old_string += '[q]'

                        rep_count += 1

                        variable = var[1:]

                    else:# coord.count(var[1:]) == 1 :

                        old_string += '[p[%d]]'%k

                        return_string += '%s,'%var

                        k += 1


                else:# coord.count(var[1:]) == 1 :

                    old_string += '[p[%d]]'%k

                    return_string += '%s,'%var

                    k += 1

            return_string = return_string[:-1]

            for k in range(new_rank):

                new_string += '[p[%d]]'%k


            if new_rank != 0:

                for p in iterprod(range(dim), repeat = new_rank):

                    var_temp = 0

                    for q in range(dim):

                        var_temp += eval('self.%s[Nindex]%s'%(ten_call,old_string),locals(),globals())

                        exec('temp%s = var_temp'%new_string,locals(),globals())

                data_result = Tdata(return_string,temp)

                TEMP = Tensor('TEMP',new_rank)

                TEMP.assign(data_result,return_string,printing=False)

                return TEMP(return_string)

            else:
                
                var = 0

                for q in range(dim):

                    var += eval('self.%s[Nindex]%s'%(ten_call,old_string),locals(),globals())

                return var 

    def space(self):
        
        '''
        Saves the spatial components of the Tensor on the attribute tensor_sp.


        Examples
        --------
        Assuming you have defined a tensor A it is possible to store its spatial by doing

        >>> A.space()
        
        '''
        
        for k in range(2**self.n):
            
            index = k
        
            iterstring = ''
            iterstring2 = ''

            for i in range(self.n):

                iterstring += '[p[%d]]'%i
                iterstring2 += '[p[%d]+1]'%i

            for p in iterprod(range(config.dim-1),repeat=self.n):

                exec_str = 'self.tensor_sp[%d]%s = self.tensor[%d]%s'%(index,iterstring,index,iterstring2)

                exec(exec_str,locals(),globals())

    def series(self,index = None):

        '''Expand each element of the tensor at the corresponding index.

        This method explicitly applies the series expansion up to the order defined.

        Parameters
        ----------
            index : str, optional
                string indicating the indices combination used to start the complete method
                If not given it applies the method to the tensor with all its covariant indices, i.e, '_i,_j,_...'

        Raises
        ------
            ValueError
                If the 'index' specified does not correspond to any possible indices combination.

        See Also
        ------
            misc.setorder()
        
        '''

        if index is None:

            index = self.sequence[0]

        if (index not in self.sequence) or index == '':

            raise ValueError('Bad index definition')

        dim = config.dim

        k = 0
        for i in self.sequence:
            if i == index:
                break 
            k += 1

        iterstring = ""

        for i in range(self.n):

            iterstring += '[p[%d]]'%i

        for p in iterprod(range(dim),repeat=self.n):

            execstr = "self.tensor[k]%s = tensor_series(self.tensor[k]%s)"%(iterstring,iterstring)

            exec(execstr,locals(),globals())
   
    def complete(self, index):

        '''Calculates the missing indices combintation of the tensor

        Calculates the missing indices combintation of the tensor using the metric to raise and lower the indices, starting from the given indices combination

        Parameters
        ----------
        index : str
            string indicating the indices combination used to start the complete method

        Raises
        ------
        ValueError
            If the 'index' specified does not correspond to any possible indices combination.

        Examples
        --------
        Assuming you have defined a tensor A with indices '_i,^j', i.e. $A_{i}^{j}$, we can calculate the other indices combinations by writting 

        >>> A.complete('_i,^j)
        
        All other indices of A Tensor $A$  already calculated.
        >>> A.assign(elements, '_i,_j')
        
        '''

        if (index not in self.sequence and index is not None) or index == '':

            raise ValueError('Bad index definition')

        createfirstindex(self,index) 

        lista = []

        for i in range(self.n):

            lista.append('_,')

        string = ''.join(lista)

        string = string[:-1] 

        subirindice(self,string)

        NAME = self.name 

        if NAME in config.default_tensors:

            NAME = config.default_tensors[NAME]

        display_string = 'All other indices of %s Tensor $%s$  already calculated.'%(self.name,NAME)

        self.space()

        display_IP(Latex_IP(display_string))

    def __assign_space(self,elements,index,printing = True):

        # Revisar el nombre de printing. Puede ser Verbose

        dim = config.dim - 1

        if isinstance(elements,Tdata):

            new_lista = index.split(',')

            old_lista = elements.full_index.split(',')

            rank = len(old_lista)

            New_data = construct(0,dim,rank)

            new_index = ''
            old_index = ''

            for i in range(rank):

                new_index += '[p[%d]]'%i

            for j in range(rank):

                i = 0

                while old_lista[j][1:] != new_lista[i][1:]:

                    i += 1

                old_index += '[p[%d]]'%i

            for p in iterprod(range(dim),repeat=rank):

                string = 'New_data%s = elements.elements%s'%(new_index,old_index)

                exec(string,locals(),globals())

            new_updn = (',').join(x[0] for x in new_lista)

            self.__assign_space(New_data,new_updn,printing=False)

        elif index == None:

            raise ValueError("'index' must be a string. e.g.: '^,^,_,^'. ")

        else:

            dim = config.dim - 1

            k = compare(self.n,index) # numero correspondiente a '^,^' o '_,^', etc


            for p in iterprod(range(dim),repeat=self.n):
                            
                string = 'self.tensor_sp[%s]'%k 
                string2 = ''

                for l in p:
                        
                    string2 += '[%s]'%l

                string = '%s%s = elements%s'%(string,string2,string2)

                try: 

                    exec(string,locals(),globals())

                except AttributeError:

                    pass
            
            self.indices[k] = True

            if printing == True:
        
                print('Elements assigned correctly to the components %s'%index)

    def assign(self, elements, index=None, All = False, printing = True, spatial = None):

        """It assigns the elements to the tensor on the corresponding indices combination.

        Simplifies each component of the tensor. If index is given, only acts on the given indices combination.

        Parameters
        ----------
        elements : array_like or Tdata
            elements to be assigned to the Tensor indices combination. These elemenents must be given in an array-like form such as a numpy array or a nested list.
            Otherwise, elements can be a 'Tdata' object obtained through the call method of a 'Tensor' object.
        index : str, optional
            string indicating the Tensor indices where to assign the elements.
        All : boolean, optional
            boolean indicating if the rest of indices combinations should be calculated after assigning the 'elements' to the Tensor 
            (the default value is False, it implies that no other indices combination will be calculated).
        printing : boolean, optional
            boolean indicating if the method should print the success after assigning the 'elements' to the Tensor
            (the default value is True, it implies that the method will indicate on which indices combination the 'elements' have been assigned).
        spatial : boolean, optional
            boolean indicating if the assignation of the 'elements' corresponds only to the spatial components of the Tensor.
            (the default value is None, it checks if the user is working only with space coordinates and if that's the case, only assigns the spatial components, else, it assigns the 'elements' to the full Tensor).
            
        Raises
        ------
        ValueError
            #####If the 'index' specified does not correspond to any possible indices combination.
        
        Examples
        --------
        Assigning a nested list to a 'Tensor'

        >>> elements = [[-1/a**2, 0, 0, 0], [0, 1, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2*sin(theta)**2]] # the 'sin' function is from sympy
        >>> A = pt.ten('A', 2)
        >>> A.assign(elements, '_i,_j')
        
        Elements assigned correctly to the _i,_j components


        Assigning a 'tdata' to a 'Tensor

        >>> elements = g('_i,_j')/a**2 # using the metric already defined
        >>> A = pt.ten('A',2)
        >>> A.assign(elements,'_i,_j')

        Elements assigned correctly to the _i,_j components

        """

        if config.space_time == False and spatial is None:

            spatial = True

        if spatial == True:

            return self.__assign_space(elements,index,printing)

        dim = config.dim

        if isinstance(elements,Tdata):

            new_lista = index.split(',')

            old_lista = elements.full_index.split(',')

            rank = len(old_lista)

            New_data = construct(0,dim,rank)

            new_index = ''
            old_index = ''

            for i in range(rank):

                new_index += '[p[%d]]'%i

            for j in range(rank):

                i = 0

                while old_lista[j][1:] != new_lista[i][1:]:

                    i += 1

                old_index += '[p[%d]]'%i

            for p in iterprod(range(dim),repeat=rank):

                string = 'New_data%s = elements.elements%s'%(new_index,old_index)

                exec(string,locals(),globals())

            #new_updn = (',').join(x[0] for x in new_lista)

            self.assign(New_data, index, All, printing)

        elif index == None:

            raise ValueError("'index' must be a string. e.g.: '^i,^j,_k,^l'. ")

        else:

            dim = config.dim

            updn = (',').join(x[0] for x in index.split(','))

            k = compare(self.n,updn) # numero correspondiente a '^,^' o '_,^', etc


            for p in iterprod(range(dim),repeat=self.n):
                            
                string = 'self.tensor[%s]'%k 
                string2 = ''

                for l in p:
                        
                    string2 += '[%s]'%l

                string = '%s%s = elements%s'%(string,string2,string2)

                try: 

                    exec(string,locals(),globals())

                except AttributeError:

                    pass
            
            self.indices[k] = True

            if printing == True:
        
                print('Elements assigned correctly to the %s components'%index)

            if All == True:

                self.complete(updn)

        self.space()

    def simplify(self,index=None):

        """Simplifies each component of the tensor.

        Simplifies each component of the tensor. If index is given, only acts on the given indices combination.

        Parameters
        ----------
        index : str, optional
            string indicating the indices combination to apply the simplification (the default is None, it implies that it will simplify all the inices combinations of the Tensor).

        Raises
        ------
        ValueError
            If the 'index' specified does not correspond to any possible indices combination.
        """

        dim = config.dim

        if (index not in self.sequence and index is not None) or index == '':

            raise ValueError('Bad index definition')

        if config.space_time == 1:

            dim = config.dim

            ten_call = 'tensor'

        else:

            dim = config.dim - 1

            ten_call = 'tensor_sp'
        

        if index is None:

            listax = list(range(2**self.n))

            if self.n == 0:


                self.tensor = eval("self.%s.simplify()"%ten_call,locals(),globals())

        else:

            listax = [compare(self.n,index)]
        
        for k in listax: 
            
            if self.indices[k] == True:

                if self.name == 'Riemann' and k == 0: 

                    Riemann_list = construct('False',dim,4)

                    for p in iterprod(range(dim),repeat=self.n):

                        counta = p[0]
                        countb = p[1]
                        countc = p[2]
                        countd = p[3]

                        if Riemann_list[counta][countb][countc][countd] == False:
                            
                            string = 'self.%s[%s]'%(ten_call,k) 

                            for l in p:
                                    
                                string += '[%s]'%l

                            string = string + '=' + string + '.simplify()'

                            exec(string,locals(),globals())

                            print('Fully Simplified:  ',counta,countb,countc,countd)

                            # Skew Symmetry

                            if Riemann_list[counta][countb][countd][countc] == False:

                                self.tensor[0][counta][countb][countd][countc] = -self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][counta][countb][countd][countc] = -self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[counta][countb][countd][countc] = True

                            if Riemann_list[countb][counta][countc][countd] == False:

                                self.tensor[0][countb][counta][countc][countd] = -self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][countb][counta][countc][countd] = -self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[countb][counta][countc][countd] = True

                            # Interchange Symmetry

                            if Riemann_list[countc][countd][counta][countb] == False:

                                self.tensor[0][countc][countd][counta][countb] = self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][countc][countd][counta][countb] = self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[countc][countd][counta][countb] = True

                            # Bianchi Identity (First)

                            if Riemann_list[counta][countc][countd][countb] == False and Riemann_list[counta][countd][countb][countc] == True:

                                self.tensor[0][counta][countc][countd][countb] = -self.tensor[0][counta][countb][countc][countd] - self.tensor[0][counta][countd][countb][countc]
                                self.tensor_sp[0][counta][countc][countd][countb] = -self.tensor_sp[0][counta][countb][countc][countd] - self.tensor_sp[0][counta][countd][countb][countc]

                                Riemann_list[counta][countc][countd][countb] = True

                            if Riemann_list[counta][countd][countb][countc] == False and Riemann_list[counta][countc][countd][countb] == True:

                                self.tensor[0][counta][countd][countb][countc] = -self.tensor[0][counta][countb][countc][countd] - self.tensor[0][counta][countc][countd][countb]
                                self.tensor_sp[0][counta][countd][countb][countc] = -self.tensor_sp[0][counta][countb][countc][countd] - self.tensor_sp[0][counta][countc][countd][countb]

                                Riemann_list[counta][countd][countb][countc] = True


                            Riemann_list[counta][countb][countc][countd] = True
                    
                else:
                
                    for p in iterprod(range(dim),repeat=self.n):
                                
                        string = 'self.%s[%s]'%(ten_call,k) 

                        for l in p:
                                
                            string += '[%s]'%l

                        if config.ord_status == False:

                            string = string + '= simplify(' + string + ')'

                        else:

                            string = string + '= simplify(tensor_series(' + string + '))'

                        #print(string)

                        exec(string,locals(),globals())

        if config.space_time == 1:
        
            self.space()

    def expand(self,index=None):

        """Expands each component of the tensor.

        Expands each component of the tensor. If index is given, only acts on the given indices combination.

        Parameters
        ----------
        index : str, optional
            string indicating the indices combination to apply the expansion (the default is None, it implies that it will expand all the inices combinations of the Tensor).

        Raises
        ------
        ValueError
            If the 'index' specified does not correspond to any possible indices combination.
        """

        dim = config.dim

        if (index not in self.sequence and index is not None) or index == '':

            raise ValueError('Bad index definition')

        
        if config.space_time == 1:

            dim = config.dim

            ten_call = 'tensor'

        else:

            dim = config.dim - 1

            ten_call = 'tensor_sp'
        

        if index is None:

            listax = list(range(2**self.n))

            if self.n == 0:


                self.tensor = eval("self.%s.expand()"%ten_call,locals(),globals())

        else:

            listax = [compare(self.n,index)]
        
        for k in listax: 
            
            if self.indices[k] == True:

                if self.name == 'Riemann' and k == 0: 

                    Riemann_list = construct('False',dim,4)

                    for p in iterprod(range(dim),repeat=self.n):

                        counta = p[0]
                        countb = p[1]
                        countc = p[2]
                        countd = p[3]

                        if Riemann_list[counta][countb][countc][countd] == False:
                            
                            string = 'self.%s[%s]'%(ten_call,k) 

                            for l in p:
                                    
                                string += '[%s]'%l

                            string = string + '=' + string + '.expand()'

                            exec(string,locals(),globals())

                            print('Fully Simplified:  ',counta,countb,countc,countd)

                            # Skew Symmetry

                            if Riemann_list[counta][countb][countd][countc] == False:

                                self.tensor[0][counta][countb][countd][countc] = -self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][counta][countb][countd][countc] = -self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[counta][countb][countd][countc] = True

                            if Riemann_list[countb][counta][countc][countd] == False:

                                self.tensor[0][countb][counta][countc][countd] = -self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][countb][counta][countc][countd] = -self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[countb][counta][countc][countd] = True

                            # Interchange Symmetry

                            if Riemann_list[countc][countd][counta][countb] == False:

                                self.tensor[0][countc][countd][counta][countb] = self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][countc][countd][counta][countb] = self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[countc][countd][counta][countb] = True

                            # Bianchi Identity (First)

                            if Riemann_list[counta][countc][countd][countb] == False and Riemann_list[counta][countd][countb][countc] == True:

                                self.tensor[0][counta][countc][countd][countb] = -self.tensor[0][counta][countb][countc][countd] - self.tensor[0][counta][countd][countb][countc]
                                self.tensor_sp[0][counta][countc][countd][countb] = -self.tensor_sp[0][counta][countb][countc][countd] - self.tensor_sp[0][counta][countd][countb][countc]

                                Riemann_list[counta][countc][countd][countb] = True

                            if Riemann_list[counta][countd][countb][countc] == False and Riemann_list[counta][countc][countd][countb] == True:

                                self.tensor[0][counta][countd][countb][countc] = -self.tensor[0][counta][countb][countc][countd] - self.tensor[0][counta][countc][countd][countb]
                                self.tensor_sp[0][counta][countd][countb][countc] = -self.tensor_sp[0][counta][countb][countc][countd] - self.tensor_sp[0][counta][countc][countd][countb]

                                Riemann_list[counta][countd][countb][countc] = True


                            Riemann_list[counta][countb][countc][countd] = True
                    
                else:
                
                    for p in iterprod(range(dim),repeat=self.n):
                                
                        string = 'self.%s[%s]'%(ten_call,k) 

                        for l in p:
                                
                            string += '[%s]'%l

                        if config.ord_status == False:

                            string = string + '= expand(' + string + ')'

                        else:

                            string = string + '= expand(tensor_series(' + string + '))'

                        #print(string)

                        exec(string,locals(),globals())

        if config.space_time == 1:

            self.space()

    def factor(self,index=None):


        """Factorizes each component of the tensor.

        Factorizes each component of the tensor. If index is given, only acts on the given indices combination.

        Parameters
        ----------
        index : str, optional
            string indicating the indices combination to apply the factorization (the default is None, it implies that it will factor all the inices combinations of the Tensor).

        Raises
        ------
        ValueError
            If the 'index' specified does not correspond to any possible indices combination.
        """

        dim = config.dim

        if (index not in self.sequence and index is not None) or index == '':

            raise ValueError('Bad index definition')

        
        if config.space_time == 1:

            dim = config.dim

            ten_call = 'tensor'

        else:

            dim = config.dim - 1

            ten_call = 'tensor_sp'
        

        if index is None:

            listax = list(range(2**self.n))

            if self.n == 0:


                self.tensor = eval("self.%s.factor()"%ten_call,locals(),globals())

        else:

            listax = [compare(self.n,index)]
        
        for k in listax: 
            
            if self.indices[k] == True:

                if self.name == 'Riemann' and k == 0: 

                    Riemann_list = construct('False',dim,4)

                    for p in iterprod(range(dim),repeat=self.n):

                        counta = p[0]
                        countb = p[1]
                        countc = p[2]
                        countd = p[3]

                        if Riemann_list[counta][countb][countc][countd] == False:
                            
                            string = 'self.%s[%s]'%(ten_call,k) 

                            for l in p:
                                    
                                string += '[%s]'%l

                            string = string + '=' + string + '.factor()'

                            exec(string,locals(),globals())

                            print('Fully Simplified:  ',counta,countb,countc,countd)

                            # Skew Symmetry

                            if Riemann_list[counta][countb][countd][countc] == False:

                                self.tensor[0][counta][countb][countd][countc] = -self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][counta][countb][countd][countc] = -self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[counta][countb][countd][countc] = True

                            if Riemann_list[countb][counta][countc][countd] == False:

                                self.tensor[0][countb][counta][countc][countd] = -self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][countb][counta][countc][countd] = -self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[countb][counta][countc][countd] = True

                            # Interchange Symmetry

                            if Riemann_list[countc][countd][counta][countb] == False:

                                self.tensor[0][countc][countd][counta][countb] = self.tensor[0][counta][countb][countc][countd]
                                self.tensor_sp[0][countc][countd][counta][countb] = self.tensor_sp[0][counta][countb][countc][countd]

                                Riemann_list[countc][countd][counta][countb] = True

                            # Bianchi Identity (First)

                            if Riemann_list[counta][countc][countd][countb] == False and Riemann_list[counta][countd][countb][countc] == True:

                                self.tensor[0][counta][countc][countd][countb] = -self.tensor[0][counta][countb][countc][countd] - self.tensor[0][counta][countd][countb][countc]
                                self.tensor_sp[0][counta][countc][countd][countb] = -self.tensor_sp[0][counta][countb][countc][countd] - self.tensor_sp[0][counta][countd][countb][countc]

                                Riemann_list[counta][countc][countd][countb] = True

                            if Riemann_list[counta][countd][countb][countc] == False and Riemann_list[counta][countc][countd][countb] == True:

                                self.tensor[0][counta][countd][countb][countc] = -self.tensor[0][counta][countb][countc][countd] - self.tensor[0][counta][countc][countd][countb]
                                self.tensor_sp[0][counta][countd][countb][countc] = -self.tensor_sp[0][counta][countb][countc][countd] - self.tensor_sp[0][counta][countc][countd][countb]

                                Riemann_list[counta][countd][countb][countc] = True


                            Riemann_list[counta][countb][countc][countd] = True
                    
                else:
                
                    for p in iterprod(range(dim),repeat=self.n):
                                
                        string = 'self.%s[%s]'%(ten_call,k) 

                        for l in p:
                                
                            string += '[%s]'%l

                        if config.ord_status == False:

                            string = string + '= factor(' + string + ')'

                        else:

                            string = string + '= factor(tensor_series(' + string + '))'

                        #print(string)

                        exec(string,locals(),globals())

        if config.space_time == 1:

            self.space()

    def display(self, index=None, aslist = None, simplify = False, spatial=None):

        """Displays the Tensor. 

        Displays the Tensor. By default it displays the tensor with all covariant indices unless 'index' is given.

        Parameters
        ----------
        index : str, optional
            string indicating the indices combination to display the Tensor (the default is None, it implies that the full covariant indices combination will be displayed).
        aslist : boolean, optional
            boolean indicating if the Tensor should be displayed in matrix form (False) or component by component as a list (True)
            (the default is None, it checks the rank of the Tensor, where if it is less than 2 it displays the tensor in matrix form, else it displays the Tensor as a list).
        simplify : boolean, optional
            if True, a simplification routin is applied to the displayed components. If False, the Tensor is displayed in its original form (the default is False).
        spatial : boolean, optional
            boolean indicating if only the spatial components of the Tensor should be displayed (True) 
            (the default value is None, it checks if the user is working only with space coordinates and if that's the case, only shows the spatial components, else, it shows the full Tensor).

        Raises
        ------
        ValueError
            If the 'index' specified does not correspond to any possible indices combination.

        Notes
        -----
        Note that if 'simplify' is True, the simplification is only performed in the display method and is not saved in the Tensor.

        """

       

        if config.space_time == False and spatial is None:

            spatial = True

        if spatial == True:

            return self.display_spatial(index, aslist, simplify)

        if core_calc == 'sp' and simplify == True:

            warn("The simplify argument is intended to be used only with giacpy.\n The result is not affected when using Sympy.")
        
        if index is None:

            index = self.sequence[0]

        if aslist == None:

            if self.n <= 2:

                aslist = False
            
            else:

                aslist = True

        dim = config.dim
        
        k = 0
        for i in self.sequence:
            if i == index:
                break 
            k += 1

        if core_calc == 'sp':

            init_printing()

        if k == len(self.sequence):

            raise ValueError('Bad index definition')

        if index == '' and self.n == 0: # Scalar

            display(self.tensor)
        
        
        elif aslist == False:

            # if k == len(self.sequence):

            #     raise ValueError('Bad index definition')

            if self.n == 1 and index == '^':
                
                if core_calc == 'sp':

                    display_IP(Array(self.tensor[k]).reshape(dim,1))

                elif core_calc == 'gp':

                    f = io.StringIO()

                    with redirect_stdout(f):

                        print(latex(giac(self.tensor[k]).transpose()))
                    out = f.getvalue()

                    out = out.replace(r"\\",r"\\\\").replace("\\text{","").replace("\"}\"","").replace('\"','').replace('\\}','}').replace('\\{','{')#.replace('\\\\','\\')

                    display_IP(Math_IP(gp_pretty_latex(out)))

            else:

                if core_calc == 'sp':
            
                    display_IP(Array(self.tensor[k]))

                elif core_calc == 'gp':

                    if simplify == False:

                        f = io.StringIO()

                        if self.n != 1:
                            with redirect_stdout(f):
                                print(latex(matrix(self.tensor[k])))
                        else:
                             with redirect_stdout(f):
                                print(latex(giac(self.tensor[k])))
                        out = f.getvalue()

                        out = out.replace(r"\\",r"\\\\").replace("\\text{","").replace("\"}\"","").replace('\"','').replace('\\}','}').replace('\\{','{')#.replace('\\\\','\\')

                        display_IP(Math_IP(gp_pretty_latex(out)))

                    else:

                        f = io.StringIO()
                        with redirect_stdout(f):
                            print((self.tensor[k]))
                        out = f.getvalue()

                        string = sp_latex(sp_simplify(sp_Array(sp_sympify(out))))

                        display_IP(Math_IP(string))

            
        else:

            count = 0
                
            for p in iterprod(range(dim),repeat=self.n):
                    
                string = 'valor = self.tensor[%s]'%k
                    
                for l in p:
                        
                    string += '[%s]'%l

                exec(string,locals(),globals())
                
                if self.name in config.default_tensors:
                    
                    str_name = config.default_tensors[self.name]

                else:

                    str_name = self.name
                
                string = "{%s}"%str_name
                    
                i = 0
                    
                for l in index.split(','):
                        
                    if core_calc == 'gp':

                        f = io.StringIO()
                        with redirect_stdout(f):
                            print(p[i])
                        out = f.getvalue()
                            
                        string = '%s{}%s{%s}'%(string,l,out)
                    
                    elif core_calc == 'sp':

                        string = '%s{}%s{%s}\,'%(string,l,str(p[i]))

                    i += 1
                    
                if valor != 0:
                        
                    #string += " = %s"% (latex(valor))
                    
                    #display_IP(Math(string))

                    if core_calc == 'gp':

                        if simplify == False:

                            display(valor,string)

                        else:

                            f = io.StringIO()
                            with redirect_stdout(f):
                                print(valor)
                            out = f.getvalue()

                            string2 = sp_latex(sp_simplify(sp_sympify(out)))

                            string = "%s = %s"%(string,string2)

                            display_IP(Math_IP(string))

                    elif core_calc == 'sp':

                        display(valor,string)

                    count += 1

            if count == 0:

                print('All components are zero')

    def display_spatial(self, index=None, aslist = None, simplify = False):

        if core_calc == 'sp' and simplify == True:

            warn("The simplify argument is intended to be used only with giacpy.\n The result is not affected when using Sympy.")
        
        if index is None:

            index = self.sequence[0]

        rank = self.n

        if aslist == None:

            if rank <= 2:

                aslist = False
            
            else:

                aslist = True

        dim = config.dim - 1 # Se elimina la dimension temporal
        
        k = 0
        for i in self.sequence:
            if i == index:
                break 
            k += 1

        if core_calc == 'sp':

            init_printing()

        if k == len(self.sequence):

            raise ValueError('Bad index definition')

        if index == '' and rank == 0: # Scalar

            display(self.tensor_sp)
        
        
        elif aslist == False:

            # if k == len(self.sequence):

            #     raise ValueError('Bad index definition')

            if rank == 1 and index == '^':
                
                if core_calc == 'sp':

                    display_IP(Array(self.tensor_sp[k]).reshape(dim,1))

                elif core_calc == 'gp':

                    f = io.StringIO()

                    with redirect_stdout(f):

                        print(latex(giac(self.tensor_sp[k]).transpose()))
                    out = f.getvalue()

                    out = out.replace(r"\\",r"\\\\").replace("\\text{","").replace("\"}\"","").replace('\"','').replace('\\}','}').replace('\\{','{')#.replace('\\\\','\\')

                    display_IP(Math_IP(gp_pretty_latex(out)))

            else:

                if core_calc == 'sp':
            
                    display_IP(Array(self.tensor_sp[k]))

                elif core_calc == 'gp':

                    if simplify == False:

                        f = io.StringIO()

                        if rank != 1:
                            with redirect_stdout(f):
                                print(latex(matrix(self.tensor_sp[k])))
                        else:
                             with redirect_stdout(f):
                                print(latex(giac(self.tensor_sp[k])))
                        out = f.getvalue()

                        out = out.replace(r"\\",r"\\\\").replace("\\text{","").replace("\"}\"","").replace('\"','').replace('\\}','}').replace('\\{','{')#.replace('\\\\','\\')

                        display_IP(Math_IP(gp_pretty_latex(out)))

                    else:

                        f = io.StringIO()
                        with redirect_stdout(f):
                            print((self.tensor_sp[k]))
                        out = f.getvalue()

                        string = sp_latex(sp_simplify(sp_Array(sp_sympify(out))))

                        display_IP(Math_IP(string))

            
        else:

            count = 0
                
            for p in iterprod(range(dim),repeat=rank):
                    
                string = 'valor = self.tensor_sp[%s]'%k

                for l in p:
                        
                    string += '[%s]'%l

                exec(string,locals(),globals())
                
                if self.name in config.default_tensors:
                    
                    str_name = config.default_tensors[self.name]

                else:

                    str_name = self.name
                
                string = "{%s}"%str_name
                    
                i = 0
                    
                for l in index.split(','):
                        
                    if core_calc == 'gp':

                        f = io.StringIO()
                        with redirect_stdout(f):
                            print(p[i])
                        out = f.getvalue()
                            
                        string = '%s{}%s{%s}'%(string,l,out)
                    
                    elif core_calc == 'sp':

                        string = '%s{}%s{%s}'%(string,l,str(p[i]))

                    i += 1
                    
                if valor != 0:
                        
                    #string += " = %s"% (latex(valor))
                    
                    #display_IP(Math(string))

                    if core_calc == 'gp':

                        if simplify == False:

                            display(valor,string)

                        else:

                            f = io.StringIO()
                            with redirect_stdout(f):
                                print(valor)
                            out = f.getvalue()

                            string2 = sp_latex(sp_simplify(sp_sympify(out)))

                            string = "%s = %s"%(string,string2)

                            display_IP(Math_IP(string))

                    elif core_calc == 'sp':

                        display(valor,string)

                    count += 1

            if count == 0:

                print('All components are zero')



def D(a,b):

    """Derivative

    Computes the derivative for the Tensor 'a' with respect to the index 'b'.

    Parameters
    ----------
    a : Tdata
        Tdata instance corresponding to the Tensor for which the derivative will be applied.
    b : str
        string corresponding to the index for the covariant derivative.

    Raises
    ------
    TensorSyntaxError
        If the arguments passed have syntax errors.
    
    Examples
    --------
    Assigning a nested list to a 'Tensor'

    >>> A = D(G("^a, ^b"), "_c")

    We suggest to save this into a Tensor object as

    >>> B = ten("B", 3)

    >>> B.assign(A, "^a, ^b, _c")

    >>> Elements assigned correctly to the ^a,^b,_j components

    """

    der_examine(b)

    if config.space_time == True:

        dim = config.dim

        coords = config.coords

    else:

        dim = config.dim - 1

        coords = config.coords_sp
    
    if isinstance(a,Tdata): #si es un Tdata
        
        old_rank = len(a.updn)
        
        if b[0] == '_':  # si es _

            #print('entro al _')

            if b[1:] in a.index_names:  #si se deriva con respecto a un indice repetido
                
                new_rank = old_rank - 1
            
                string_return = ''

                for i in range(len(a.index_names)):

                    if a.index_names[i] != b[1:]:

                        string_return += a.updn[i] + a.index_names[i] + ','

                string_return = string_return[:-1]

                temp = construct(0,dim,new_rank)

                new_index = ''
                
                k = 0

                while k < new_rank:

                    new_index +='[p[%d]]'%k

                    k += 1

                old_index = ''

                k = 0

                j = 0

                while k < old_rank:

                    if a.index_names[k] == b[1:]:

                        der_index ='q'

                        old_index +='[q]'

                    else:

                        old_index +='[p[%d]]'%j

                        j += 1
                    
                    k += 1
                
                k = 0

                exec(reload_all('config'),locals(),globals())

                for p in iterprod(range(dim),repeat = new_rank): 

                    var_temp = 0
                    
                    for q in range(dim):
    
                        string = 'diff(a.elements%s,coords[%s])'%(old_index,der_index)

                        var_temp += eval(string,locals(),globals())

                    if new_rank == 0:
                        
                        return var_temp
                    
                    string = 'temp%s = var_temp'%new_index

                    exec(string,locals(),globals())
             
                return Tdata(string_return, temp)
                
            else:                   #si se deriva con respecto a un indice no repetido 

                new_rank = old_rank + 1
            
                string_return = a.full_index +','+ b
                
                temp = construct(0,dim,new_rank)
                
                k = 0

                old_index = ''

                while k < old_rank:

                    old_index +='[p[%d]]'%k

                    k += 1
                
                k = 0
                
                new_index = ''
                
                while k < new_rank:

                    new_index +='[p[%d]]'%k

                    k += 1

                exec(reload_all('config'),locals(),globals())

                for p in iterprod(range(dim),repeat = new_rank): 
    
                    string = 'temp%s = diff(a.elements%s,%s)'%(new_index,old_index,coords[p[-1]])

                    exec(string,locals(),globals())
                
                return Tdata(string_return, temp)
            
        else:           # si es ^

            new_symbol = 'dummy'
            i = 0

            while new_symbol in a.index_names or new_symbol == b[1:]:

                new_symbol = 'dummy%d'%i
                i += 1

            b_new = '_' + new_symbol

            g_indices = b + ',^%s'%new_symbol # b is the original index, i.e. '^c'

            return D(a, b_new) * config.g(g_indices)

    else: # si var es un int o sympy o symengine

        temp = construct(0,dim,1)

        string_return = b

        exec(reload_all('config'),locals(),globals())

        for p in range(dim):

            string = 'temp[%d] = diff(a,%s)'%(p,coords[p])

            exec(string,locals(),globals())
        
        return Tdata(string_return, temp)

def C(a,b):

    """Covariant derivative

    Computes the covariant derivative for the Tensor 'a' with respect to the index 'b'.

    Parameters
    ----------
    a : Tdata
        Tdata instance corresponding to the Tensor for wich the covariant derivative will be applied.
    b : str
        string corresponding to the index for the covariant derivative.

    Raises
    ------
    TensorSyntaxError
        If the arguments passed have syntax errors.
    
    Examples
    --------
    Assigning a nested list to a 'Tensor'

    >>> A = C(G("^a, ^b"), "_c")
    We suggest to save this into a Tensor object as

    >>> B = ten("B", 3)

    >>> B.assign(A, "^a, ^b, _c")

    Elements assigned correctly to the ^a,^b,_j components

    """

    der_examine(b)

    if config.space_time == True:

        dim = config.dim

    else:

        dim = config.dim - 1

    if isinstance(a,Tdata): #si es un Tdata

        if config.christ is None:

            print("Christofel Symbols not calculated.")

            raise(NotImplementedError)

        was_up = False
        was_rep = False

        if b[0] == '^':  # si es _

            new_symbol = 'dummy'
            i = 0

            while new_symbol in a.index_names or new_symbol == b[1:]:

                new_symbol = 'dummy%d'%i
                i += 1

            b_new = '_' + new_symbol

            g_indices = b + ',^%s'%new_symbol # b is the original index, i.e. '^c'

            return C(a, b_new) * config.g(g_indices)

        if b[1:] in a.index_names:  #si se deriva con respecto a un indice repetido

            rep_symbol = b[1:][:]

            new_symbol = 'dummy'
            i = 0

            was_symbol = b[1:][:]

            was_rep = True

            while new_symbol in a.index_names or new_symbol == b[1:]:

                new_symbol = 'dummy%d'%i
                i += 1

            b = b[0] + new_symbol[:]

        old_rank = len(a.updn)

        new_rank = old_rank + 1
    
        string_return = a.full_index +','+ b  # _i,_j + _k

        temp_full_index = '%s'%a.full_index
        
        return_tensor = construct(0,dim,new_rank)

        a_list_index = a.full_index.split(',')

        k = 0

        old_index = ''

        while k < old_rank:

            old_index +='[p[%d]]'%k

            k += 1
        
        k = 0
        
        new_index = ''
        
        while k < new_rank:

            new_index +='[p[%d]]'%k

            k += 1

        dummy = 'dummy'

        i = 0

        while dummy in a.index_names or dummy == b[1:]:

            dummy = 'dummy%d'%i
            i += 1

        exec(reload_all('config'),locals(),globals())
            
        var = D(a,b)

        for num, ind in enumerate(a_list_index):  # ['^x','_y']

            tdata_str = ''

            if ind[0] == '^':
        
                chrstr = '^%s,_%s,_%s'%(ind[1:],dummy,b[1:])

                for l in range(len(a_list_index)):

                    if l == num:

                        tdata_str += '^%s,'%dummy
                    else:
                        tdata_str += '%s,'%a_list_index[l]

                tdata_str = tdata_str[:-1]

                TEMP_tdata = Tdata(tdata_str,a.elements)

                var = var + config.christ(chrstr)*TEMP_tdata

                #print("Ind^: christ = %s\ttdat = %s\n"%(chrstr,tdata_str))

            elif ind[0] == '_':
        
                chrstr = '^%s,_%s,_%s'%(dummy,ind[1:],b[1:])

                for l in range(len(a_list_index)):

                    if l == num:

                        tdata_str += '_%s,'%dummy
                    else:
                        tdata_str += '%s,'%a_list_index[l]

                tdata_str = tdata_str[:-1]

                TEMP_tdata = Tdata(tdata_str,a.elements)

                var = var - config.christ(chrstr)*TEMP_tdata

        if was_rep == True:

            str_temp = var.full_index.replace(new_symbol, rep_symbol)

            var = Tdata(str_temp,var.elements)

        return var.auto_sum()
        
    # If var is an int or a sympy object

    else: 
    
        return D(a,b)

def create(name,TD):

    '''
    Ponerla como function de un TDATA entonces hacemos algo como A = TD.save('name')
    '''
    
    rank = len(TD.full_list)
    
    T = new_ten(name,rank)
    
    T.assign(TD,TD.full_index)
    
    T.factor((',').join(TD.updn))
    
    return T

def determinant(T):

    """Determinant

    Utility to compute the determinant of a rank 2 'Tensor' T

    Parameters
    ----------
    T : Tensor
        Rank 2 'Tensor' instance.

    Raises
    ------
    ValueError
        If it receives anything else than a 'Tensor' object.
        If it is not a rank 2 tensor.
    
    Examples
    --------
    Assigning a nested list to a 'Tensor'

    >>>  = C(G("^a, ^b"), "_c")
    We suggest to save this into a Tensor object as

    >>> B = ten("B", 3)

    >>> B.assign(A, "^a, ^b, _c")

    Elements assigned correctly to the ^a,^b,_j components

    """

    if not isinstance(T,Tdata):

        raise(ValueError("T must ve a Tdata instance."))
    
    if len(T.updn) != 2: 
        
        raise(ValueError("Must be a rank 2 tensor"))
        
    if core_calc == 'sp':
        
        return det(Matrix(T.elements))
        
    elif core_calc == 'gp':
        
        raise(NotImplementedError("Method not implemented for giacpy"))
        
        

def create_tensor(T_name,n):
    
    create_temp(name,obj)

    T_object = Tensor(T_name,n)

    return config.create_ten(T_name,T_object)

def tensor_series(element):

    '''
    Compute the series of an element.
    '''

    if core_calc == 'gp':

        result = series(element,config.ord_var,0,config.ord_n)

    elif core_calc == 'sp':

        result = series(expand(element), config.ord_var,0, config.ord_n+1)

    return result
