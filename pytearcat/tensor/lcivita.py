import numpy as np
from itertools import permutations, product as iterprod
from .tensor import ordenar, compare, Tensor
from .core import config
from .core.core import *
from .core.display import display
from .core.interp import syntax
from .core.tdata import Tdata, construct

if core_calc == 'gp':

    import io
    from contextlib import redirect_stdout
    from .core.display import gp_pretty_latex
    from .core.core import sp_simplify, sp_sympify, sp_latex, sp_Array

class LeviCivita():

    
    def __init__(self,convention=1):

        dim = config.dim

        self.name = 'LeviCivitaSymbol'

        self.n = dim

        self.sequence = ordenar(self.n)

        self.indices = np.full((2**self.n), False)

        if convention != 1 and convention != -1:

            raise(ValueError("Convention must be 1 or -1."))

        self.convention = convention

        if core_calc == 'sp':

            string = 'sympify(np.nan),'*dim

        elif core_calc == 'gp':
            
            string = 'np.nan,'*dim

        string = '['+string[:-1]+'],'

        for k in range(self.n-1):

            string = '['+(string*dim)[:-1]+'],'  

        string = 'self.tensor = [' + (string*(2**self.n))[:-1]+']'

        exec(string)# primer casillero corresponde al indice de la combinacion de indices (^,_,_,^,_), son 2**n combinaciones, los demas son primer indice, segundo indice, tercer indice, .... del tensor cada uno de ellos va desde 0 a dim, donde hay n dimnesiones

        #----

        if core_calc == 'sp':

            string = 'sympify(np.nan),'*(dim-1)

        elif core_calc == 'gp':
            
            string = 'np.nan,'*(dim-1)

        string = '['+string[:-1]+'],'

        for k in range(self.n-1):

            string = '['+(string*(dim-1))[:-1]+'],'  

        string = 'self.tensor_sp = [' + (string*(2**(self.n-1)))[:-1]+']'

        exec(string)# primer casillero corresponde al indice de la combinacion de indices (^,_,_,^,_), son 2**n combinaciones, los demas son primer indice, segundo indice, tercer indice, .... del tensor cada uno de ellos va desde 0 a dim, donde hay n dimnesiones

        # ----------------------------------------

        rank = config.dim

        vals, order = values(rank,rank)

        for i,j in enumerate(order):

            iterstring = '[0][' + ']['.join(j.astype(str)) + ']' 

            string = 'self.tensor%s = int(vals[%d]*self.convention)'%(iterstring,i)

            exec(string,locals(),globals())


        for k in range(1,2**rank):

            string = 'self.tensor[%d] =self.tensor[0]'%k

            exec(string,locals(),globals())

        rank = rank - 1

        vals, order = values(rank,rank)

        for i,j in enumerate(order):

            iterstring = '[0][' + ']['.join(j.astype(str)) + ']' 

            string = 'self.tensor_sp%s = int(vals[%d]*self.convention)'%(iterstring,i)

            exec(string,locals(),globals())

        for k in range(1,2**rank):

            string = 'self.tensor_sp[%d] = self.tensor_sp[0]'%k

            exec(string,locals(),globals())

    def __repr__(self):

        return '%s Symbol defined'%self.name

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
            
                tdat_str += updn[i] + coord[i]
                
                new_string_right += '[p[%d]]'%k
                
                k += 1
                
            else: 
                
                new_string_right += '[%s]'%numbers[j]
                
                j += 1
                
                    
        new_rank = len(coord)-len(numbers)
        
        elements = construct(0,dim,new_rank)
        
        new_string_left = ''
        
        for k in range(new_rank):

            new_string_left += '[p[%d]]'%k
        
        
        for p in iterprod(range(dim), repeat = new_rank):

            exec_str = 'elements%s = self.%s[%s]%s'%(new_string_left,ten_call,Nindex,new_string_right)
        
            exec(exec_str,locals(),globals())
        
        return Tdata(tdat_str,elements)
    

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
                
        if len(numbers) == len(coord):
            
            return self.__scalar_call(updn,numbers,Nindex,ten_call)

        for i in lista:

            if lista.count(i) > 1:

                raise SyntaxError('Problem with the indices. Error in the Einstein summation.')
            
        if len(numbers) != 0:
            
            return self.__Tdata_call(updn,coord,numbers,Nindex,dim,ten_call)


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
        Retorna solo las componentes espaciales del tensor completo
        
        Generalizar para todos los indices. El [1:,1:,....,1:]
        
        
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



    def display(self, index=None, aslist = None, simplify = False, spatial = None):

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
                
                str_name =  "\\varepsilon"
                
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


    def display_spatial(self, index=None, aslist = None, simplify = False):

        if core_calc == 'sp' and simplify == True:

            warn("The simplify argument is intended to be used only with giacpy.\n The result is not affected when using Sympy.")
        
        sequence_sp = ordenar(self.n - 1)


        if index is None:

            index = sequence_sp[0]

        rank = self.n - 1

        if aslist == None:

            if rank <= 2:

                aslist = False
            
            else:

                aslist = True

        dim = config.dim - 1 # Se elimina la dimension temporal
        
        k = 0
        for i in sequence_sp:
            if i == index:
                break 
            k += 1

        if core_calc == 'sp':

            init_printing()

        if k == len(sequence_sp):

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
                
                str_name =  "\\varepsilon"
                
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







def arePermsEqualParity(perm0, perm1):
    """Check if 2 permutations are of equal parity.

    Assume that both permutation lists are of equal length
    and have the same elements. No need to check for these
    conditions.
    """
    perm1 = list(perm1) ## copy this into a list so we don't mutate the original
    perm1_map = dict((v, i) for i,v in enumerate(perm1))
    transCount = 0
    for loc, p0 in enumerate(perm0):
        p1 = perm1[loc]
        if p0 != p1:
            sloc = perm1_map[p0]                       # Find position in perm1
            perm1[loc], perm1[sloc] = p0, p1           # Swap in perm1
            perm1_map[p0], perm1_map[p1] = loc, sloc   # Swap the map
            transCount += 1
    # Even number of transpositions means equal parity
    value = (transCount % 2) == 0
    
    if value:
        
        return 1
    
    else:
        
        return -1
    

def values(n,dim):
    
    x = np.linspace(0,dim-1,dim)
    
    elements = np.asarray(list(iterprod(x,repeat=n)),dtype=int) 
    
    parity = np.zeros(dim**n,dtype=int)
    
    for pos,i in enumerate(elements):
        
        #print(i)
        
        if any(list(i).count(j) > 1 for j in i): # si hay repetidos
            
            #print(0)
            
            parity[pos] = 0
        
        else: # no estan repetidos
        
            parity[pos] = arePermsEqualParity(x,i)
        
            #print(parity[pos])
        
    return parity,elements

