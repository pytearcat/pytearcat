import numpy as np 
from itertools import product as iterprod
from numpy.lib.arraysetops import isin
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

    ''' x

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

    # i: primera posicion que tiene un indice arriba ej: en un string de indices '_,^,^' -> i = 1 (contando desde 0)

    # kstring: string original de los indices tensor ej: '_,^,^'

    # kstring2: string objetivo (con el indice i abajo) de los indices del tencor ej: '_,_,^'

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

    # hasta aqui todo okidoki uwu

    # ESTA FUNCION SE TENDRA QUE LLAMAR CUANTAS VECES SEA NECESARIA HASTA LLEGAR A TENER TODO ABAJO _ _ _

    # REVISAR EL RESULTADO DE LA PRIMERA BAJADA DE INDICES COMPARAR CON GRTENSOR



def subirindice(tensor,kstring):

    # Recibe:

    # 1) Nombre de la variable de clase Tensor al cual queremos subir los indices

    # 2) string de la forma '_,^,_'

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

    # kstring: string original de los indices ej: '^,_,_' ...
    # tensor: tensor de la clase Tensor

    N = tensor.n # Number of index

    objetivo = tensor.sequence[0].split(',') # ['_','_','_']

    lista = kstring.split(',')  # ['^','_','_']

    for i in range(len(lista)):

        if lista[i] != '_':

            lista[i] = '_'

            kstring_new = ','.join(lista)

            bajarindice(tensor,i,kstring,kstring_new)

            kstring = kstring_new

# class Tdata:

#     def __init__(self,name,str_index,elements):

#         self.name = name

#         self.index = # 


class Tensor:

    # CREATE A TENSOR WITH A name, n: NUMBER OF indices AND tensor: values of the tensor with coordinates given by the index

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

        # NAME

        self.name = name

        #NUMBER OF INDEX

        self.n = n

        #ORDEN DE LOS INDICES up Y down

        self.sequence = ordenar(n)

        self.indices = np.full((2**n), False)

        if core_calc == 'sp':

            string = 'sympify(np.nan),'*dim

        elif core_calc == 'gp':
            
            string = 'np.nan,'*dim

        string = '['+string[:-1]+'],'

        for k in range(n-1):

            string = '['+(string*dim)[:-1]+'],'  

        # if n == 1:

        #     string = string[:-1] 

        string = 'self.tensor = [' + (string*(2**n))[:-1]+']'

        exec(string)# primer casillero corresponde al indice de la combinacion de indices (^,_,_,^,_), son 2**n combinaciones, los demas son primer indice, segundo indice, tercer indice, .... del tensor cada uno de ellos va desde 0 a dim, donde hay n dimnesiones

        #----

        if core_calc == 'sp':

            string = 'sympify(np.nan),'*(dim-1)

        elif core_calc == 'gp':
            
            string = 'np.nan,'*(dim-1)

        string = '['+string[:-1]+'],'

        for k in range(n-1):

            string = '['+(string*(dim-1))[:-1]+'],'  

        # if n == 1:

        #     string = string[:-1] 

        string = 'self.tensor_sp = [' + (string*(2**n))[:-1]+']'

        exec(string)# primer casillero corresponde al indice de la combinacion de indices (^,_,_,^,_), son 2**n combinaciones, los demas son primer indice, segundo indice, tercer indice, .... del tensor cada uno de ellos va desde 0 a dim, donde hay n dimnesiones


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

        '''
        Solo acepta a lo mas la contraccion de 1 solo indice. Hay que incluir esto
        en el examine de este call

        Funcionando para space only
        '''

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
        Saves the spatial components of the Tensor on the attribut tensor_sp.

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

        '''
        Expands each element of the tensor at the given indices.
        
        '''

        if index is None:

            index = self.sequence[0]

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
   
    def complete(self, kstring):

        '''
        It calculates the missing indices combintation of the tensor raising and lowering the indices 
        from the given indices combination

        Receives:

        - string indicating the starting indices combination i.e., '_,^,_' for a 3-rank tensor.
        
        '''

        createfirstindex(self,kstring) 

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

    def assign_space(self,elements,index,printing = True):


        '''
        # Revisar el nombre de printing. Puede ser Verbose

        It assigns the elements to the tensor on the corresponding index. 
        If All = True, then it computes the thensor with the rest of the indices combinations.

        index = '^,^,_'
        elements = [[[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]]

        NOTE: the argument "elements" has to be shaped like the example so the indexation goes like elements[i][j][k]

        '''
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

            self.assign_space(New_data,new_updn,printing=False)

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


    def assign(self, elements, index=None, All = False,printing = True, spatial = None):

        '''
        # Revisar el nombre de printing. Puede ser Verbose

        It assigns the elements to the tensor on the corresponding index. 
        If All = True, then it computes the thensor with the rest of the indices combinations.

        index = '^,^,_'
        elements = [[[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]]

        NOTE: the argument "elements" has to be shaped like the example so the indexation goes like elements[i][j][k]

        '''

        if config.space_time == False and spatial is None:

            spatial = True

        if spatial == True:

            return self.assign_space(elements,index,printing)

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

            new_updn = (',').join(x[0] for x in new_lista)

            self.assign(New_data,new_updn,printing=False)

        elif index == None:

            raise ValueError("'index' must be a string. e.g.: '^,^,_,^'. ")

        else:

            dim = config.dim

            k = compare(self.n,index) # numero correspondiente a '^,^' o '_,^', etc


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
        
                print('Elements assigned correctly to the components %s'%index)

            if All == True:

                self.complete(index)

        self.space()

    def simplify(self,index=None):

        '''
        Simplify the Tensor. If index is given, it will simplify only the given index combination ('^,_,_')
        '''

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

        '''
        Expand the Tensor. If index is given, it will expand only the given index combination ('^,_,_')
        '''

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

        '''
        Expand the Tensor. If index is given, it will expand only the given index combination ('^,_,_')
        '''

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

        '''
        Display method of Tensor. By default it displays the tensor with all covariant indices unless index is given.

        '''

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

    '''
    Derivative of a tensor "a" with respect to the index "b".

    a is an object of class Tdata
    b is a string that indicates the index, written as "_index"

    It returns an object of class Tdata. 

    -------------
    Example:

    A = D(G("^a, ^b"), "_c")

    We suggest to save this into a Tensor object as

    B = ten("B", 3)

    B.assign(A, "^a, ^b, _c")

    '''

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

            #print('entro al ^')

            new_rank = old_rank + 1
        
            new_var = 'dummy'

            while new_var in a.index_names:

                new_var += '0'

            new_var = '_' + new_var

            string_return = a.full_index +','+ new_var
            
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

            new_var2 = '^' + new_var[1:]

            string_return = a.full_index +','+ new_var

            if b[1:] not in a.index_names:

                g_string = b + ',' + new_var2

                #print(g_string, string_return)

                return config.g(g_string)*Tdata(string_return, temp)

            else:

                new_var = 'dummy'

                while new_var in a.index_names or new_var == new_var2[1:]:

                    new_var += '0'

                new_var = '^' + new_var

                g_string = new_var + ',' + new_var2

                #print(g_string, string_return)

                temp_return = config.g(g_string)*Tdata(string_return, temp)

                temp_return.full_list[0] = '^' + temp_return.full_list[-1][1:]

                string = ','.join(temp_return.full_list)     

                temp_return = Tdata(string,temp_return.elements)

                return temp_return.auto_sum()

    else: # si var es un int o sympy o symengine

        temp = construct(0,dim,1)

        string_return = b

        exec(reload_all('config'),locals(),globals())

        for p in range(dim):

            string = 'temp[%d] = diff(a,%s)'%(p,coords[p])

            exec(string,locals(),globals())
        
        return Tdata(string_return, temp)

def C(a,b):

    '''
    Covariant derivative of a tensor "a" with respect to the index "b".

    a is an object of class Tdata
    b is a string that indicates the index, written as "_index"

    It returns an object of class Tdata. 

    -------------
    Example:

    A = C(G("^a, ^b"), "_c")

    We suggest to save this into a Tensor object as

    B = ten("B", 3)

    B.assign(A, "^a, ^b, _c")

    '''

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

            was_up = True

            b = '_' + b[1:]

        if b[1:] in a.index_names:  #si se deriva con respecto a un indice repetido

            rep_symbol = b[1:][:]

            new_symbol = 'dummy'
            i = 0

            was_symbol = b[1:][:]

            was_rep = True

            while new_symbol in a.index_names or new_symbol == b[1:]:

                new_symbol += '%d'%i
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

            dummy += '%d'%i
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

        # si el indice c/r al que se deriva estaba arriba entonces multiplicamos por la metrica inversa

        # hay que revisar si esta dando bien porque hay q constatar el orden de los indices

        # esta hecho CON LA IDEA DE QUE, HAY Q REVISARLO...., LA IDEA ES: QUE SIEMPRE EL INDICE QUE SE HEREDA QUEDA AL FINAL
        # POR ORDEN, ASI QUE SIEMPRE HAY QUE REEMPLAZAR SOLO EL ULTIMO INDICE

        if was_up == True:  # solo sube el indice NO SE FIJA SI HAY REPETICION

            dummy = 'dummy'

            i = 0

            while dummy in var.index_names:

                dummy += '%d'%i
                i += 1

            moved_symbol = var.index_names[-1][:]
            
            str_temp = var.full_index[:]

            var = var*config.g('^%s,^%s'%(dummy,moved_symbol))

            var = Tdata(str_temp,var.elements)

        if was_rep == True:

            moved_symbol = var.index_names[-1][:]

            str_temp = ''

            for i,name in enumerate(var.index_names):

                if i == len(var.index_names) - 1:

                    str_temp += '^' + var.updn[i][1:] + rep_symbol +','

                else: 
                    
                    str_temp += var.updn[i] + var.index_names[i]  +','

            str_temp = str_temp[:-1]

            var = Tdata(str_temp,var.elements)     
######################### SON MUCHOS CASOS ARRIBA REPETIDOS ABAJO REPETIDOS, ABAJO SIN REPETIR ARRIBA SIN REPETIR

        #print(var.full_index)

        #print('antes d entrar al autosum')

        return var.auto_sum()
        
    else: # si var es un int o sympy o symengine
    
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