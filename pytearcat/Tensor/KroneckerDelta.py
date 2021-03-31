
import numpy as np
from itertools import permutations, product as iterprod
from .tensor_class import ordenar, compare, Tensor
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



class KroneckerDelta():

    
    def __init__(self):

        dim = config.dim

        self.name = 'KroneckerDelta'

        self.n = 2

        self.orden = ordenar(self.n)

        self.indexes = np.full((2**self.n), False)

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

        for k in range(self.n):

            string = '['+(string*(dim-1))[:-1]+'],'  

        string = 'self.tensor_sp = [' + (string*(2**(self.n)))[:-1]+']'

        exec(string)# primer casillero corresponde al indice de la combinacion de indices (^,_,_,^,_), son 2**n combinaciones, los demas son primer indice, segundo indice, tercer indice, .... del tensor cada uno de ellos va desde 0 a dim, donde hay n dimnesiones

        # ----------------------------------------

        if core_calc == 'sp':

            Eye = eye(dim)

            self.__assign(Eye.tolist(),'_,_')
            self.__assign(Eye.tolist(),'^,_')
            self.__assign(Eye.tolist(),'_,^')
            self.__assign(Eye.tolist(),'^,^')
        
        elif core_calc == 'gp':

            Eye = identity(dim)

            self.__assign(list(Eye),'_,_')
            self.__assign(list(Eye),'^,_')
            self.__assign(list(Eye),'_,^')
            self.__assign(list(Eye),'^,^')

    def __repr__(self):

        return '%s Symbol defined'%self.name

    def __str__(self):

        if self.n <=2:

            self.display()

            string = ''

        else:

            string = 'Too many tensor indexes. Please use the display method.'
        
        return string

    def __call__(self,str_index):

        '''
        Solo acepta a lo mas la contraccion de 1 solo indice. Hay que incluir esto
        en el examine de este call

        Funcionando para space only
        '''

        if config.space_time == True:

            dim = config.dim

            ten_call = 'tensor'

            syntax(str_index,self.n)

        else:

            dim = config.dim - 1

            ten_call = 'tensor_sp'

            syntax(str_index,self.n)

        lista = str_index.split(',')

        updn = [symbol[0] for symbol in lista]

        coord = [symbol[1:] for symbol in lista]
        
        Nindex = compare(len(updn),(',').join(updn))

        repeated_coord = set([x for x in lista if coord.count(x[1:]) > 1])

        non_repeated_coord = set([x for x in lista if coord.count(x[1:]) == 1])

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

    def __assign(self, elements, index=None,All = False,printing = False):

        '''
        # Revisar el nombre de printing. Puede ser Verbose

        It assigns the elements to the tensor on the corresponding index. 
        If All = True, then it computes the thensor with the rest of the indexes combinations.

        index = '^,^,_'
        elements = [[[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]]

        NOTE: the argument "elements" has to be shaped like the example so the indexation goes like elements[i][j][k]

        '''
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

            print(ERROR)

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
            
            self.indexes[k] = True

            if printing == True:
        
                print('Elements assigned correctly to the components %s'%index)

            if All == True:

                self.indexcomb(index)

        self.space()

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

            index = self.orden[0]

        if aslist == None:

            if self.n <= 2:

                aslist = False
            
            else:

                aslist = True

        dim = config.dim
        
        k = 0
        for i in self.orden:
            if i == index:
                break 
            k += 1

        if core_calc == 'sp':

            init_printing()

        if k == len(self.orden):

            raise ValueError('Bad index definition')

        if index == '' and self.n == 0: # Scalar

            display(self.tensor)
        
        
        elif aslist == False:

            # if k == len(self.orden):

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
        
        if index is None:

            index = self.orden[0]

        rank = self.n

        if aslist == None:

            if rank <= 2:

                aslist = False
            
            else:

                aslist = True

        dim = config.dim - 1 # Se elimina la dimension temporal
        
        k = 0
        for i in self.orden:
            if i == index:
                break 
            k += 1

        if core_calc == 'sp':

            init_printing()

        if k == len(self.orden):

            raise ValueError('Bad index definition')

        if index == '' and rank == 0: # Scalar

            display(self.tensor_sp)
        
        
        elif aslist == False:

            # if k == len(self.orden):

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