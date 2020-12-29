import re
import numpy as np
from collections import Counter
from copy import deepcopy
from .errors import TensorSyntaxError
from .config import greek_dict
from .distribute import distribute


def index_counter(element):
    
    #'Tg[_i,^j]*TC2[^i,_k,_l]+TC2[^i,_k,_l]-TC2[^i,_k,_l]*Tg[^l,_p]'
    
    # WE SPLIT THE STRING AND ASSIGN EVERY TERM TO A LIST
       
    list_strings = re.split('[- +]',element)
    
    if list_strings[0] == '':
        
        list_strings = list_strings[1:]
    
    # NOW WE SEARCH FOR EVERY STRING IN list_strings THE UPPER AND LOWER INDEX AND VERIFY IF THIS HAS SENSE

    error_indice_up_dn = False
    
    n_up = 0
    n_dn = 0
    
    contador_up = []
    contador_dn = []
    
    repeated_index = []
    
    n_termino = 0
    
    list_tensor_term_index = []
    
    indexacion_ok = True
    
    for string in list_strings:
        
        list_index = []
        
        n_up = 0
        n_dn = 0
    
        #'Tg[_i,^j]*TC2[^i,_k,_l]'

        # D(H[^l,_j],_k)
        for i in range(len(string)):
            
            if string[i] == '_' or string[i] == '^':
                
                j = i

                while string[j] != ',' and string[j] != ']' and string[j] != ')':

                    j += 1

                #list_index.append(string[i:i+2])
                list_index.append(string[i:j])

        
        list_tensor_term_index.append(list_index)
        
        #['_i', '^j', '^i', '_k', '_l']
        
        # WE MUST VERIFY IF EVERY ELEMENT OF THIS ARRAY HAS ONLY TWO CHARS BY STRING. THEN
            
        up_dn_index_list = [] 

        symbol_index_list = []

        for letras in list_index:
        
            up_dn_index_list.append(letras[0])
            #['_', '^', '^', '_', '_']
            
            symbol_index_list.append(letras[1:])
            #['i', 'j', 'i', 'k', 'l']

        for i in range(len(symbol_index_list)):
            
            contador = 1
            
            for j in  [x for x in range(len(symbol_index_list)) if x != i]:
                
                if symbol_index_list[i] == symbol_index_list[j]:
                    
                    contador += 1
                    
                    if contador == 2:
            
                        if not ((up_dn_index_list[i] == '_' and up_dn_index_list[j] == '^') or (up_dn_index_list[i] == '^' and up_dn_index_list[j] == '_')):
                            
                            #print('not up or dn')
                            
                            indexacion_ok = False
                    
                    elif contador > 2:
                        
                        #print('repetido mas de 2 veces')
                        
                        #print(string,up_dn_index_list,symbol_index_list)
                        
                        indexacion_ok = False
          
        counter=Counter(symbol_index_list)
        
        arreglo_momentaneo = [counter[x] for x in counter.keys()]
        
        #AHORA HAY QUE CONTAR CUANTOS INDICES HAY SIN REPETIR
        
        arreglo_dict = np.asarray([(k,v) for k,v in counter.items()]) 
        #THIS LINE CONVERTS THE DICTIONARY TO A LIST, AND THIS TO AN ARRAY!!!!!!!
        
        for i in range(len(counter.items())):
        
            if arreglo_dict[i,1] == '1':  
                # SI EL ELEMENTO i-ESIMO NO SE REPITE (SE CUENTA UNA SOLA VEZ)
               
                pos = np.where(np.asarray(symbol_index_list) == arreglo_dict[i,0] )[0][0]
                         
                el_simbolo = up_dn_index_list[pos]    
                #EVALUA EL ARREGLO DE ^_ EN LA POSICION
                # DONDE EL ELEMENTO QUE SOLO APARECE UNA SOLA VEZ TIENE 
                #EL MISMO SIMBOLO EN EL DICCIONARIO QUE EN EL symbol_index_list
                
                if el_simbolo == '^':
                    
                    n_up += 1
                             
                elif el_simbolo == '_':
                    
                    n_dn += 1
                               
                else:
                    
                    error_indice_up_dn = True
            
            else:
                
                # SI EL INDICE ESTA REPETIDO EL CONTADOR DEL DICCIONARIO SERA 2, SI SE REPITE MAS VECES SE RETORNARA
                # EL ERROR EN INDICES REPETIDOS ANTES COMO: indexacion_ok
                # GUARDAMOS LOS INDICES QUE ESTAN REPETIDOS, SOLO EL SIMBOLO, NO EL INDICADOR _ O ^ Y LO GUARDAMOS PARA
                # CADA TERMINO DE LA ECUACION (CADA TERMINO: PARA CADA ELEMENTO SEPARADO POR * )
                
                repeated_index.append([n_termino,arreglo_dict[i,0]])  #GUARDAMOS LOS INDICES REPETIDOS
        
        if all(value == 1 for value in  counter.values()) == True:
            
               
            repeated_index.append([n_termino,'none'])  #GUARDAMOS LOS INDICES REPETIDOS
      
        contador_up.append(n_up)
        contador_dn.append(n_dn)
        
        
        n_termino +=1    
    
        #DE ESTOS INDICES, CUANTOS SON UP Y CUANTOS DOWN, Y Q ESTO SEA CONSISTENTE PARA TODOS LOS TERMINOS
        #RETORNAR SI ES CIERTO O NO
    
    # AHORA RETORNA EL element INICIAL (FORMULA COMPLETA) CORTADA EN STRINGS DONDE 
    # CADA UNO SE SUMA SOBRE SUS PROPIOS INDICES REPETIDOS
    
    indice_up_dn_OK = not error_indice_up_dn

    
    return (indexacion_ok,indice_up_dn_OK,contador_up,contador_dn,repeated_index,list_tensor_term_index)
        

# def info_tensor_index(element,sum_over_diz_index,mlist_tensor_term_index):
    
#     column_index_sub_element = [i[0] for i in sum_over_diz_index]
#     column_symbol = [i[1] for i in sum_over_diz_index]
#     #ARREGLO QUE ESPECIFICA CUANTAS VECES ESTA REPETIDO DETERMINADO SIMBOLO EN EL N-ESIMO TERMINO
    
#     counts = np.bincount(column_index_sub_element)
#     sub_element_index = np.argmax(counts)            # SOLO SE QUEDA CON EL PRIMER INDICE QUE ENCUENTRE MAS FRECUENTE,
#     # SI HAY VARIOS SUBSUMAS SOBRE N INDICES TENSORIALES, ENTONCES SE QUEDA CON EL SUBELEMENTO DE ELEMENTO QUE POSEE MAS CANTIDAD
#     #DE SUBSUMAS SOBRE SUS INDICES, AUNQUE HAYAN OTROS CON LA MISMA CANTIDAD
    
#     mlist_tensor_term_si_sum_index = []
#     # LISTA SOLO DE INDICES i j k etc... DONDE SE SUMA  PARA CADA TERMINO TENSORIAL
#     # SE EDITA MAS ABAJO

#     mlist_tensor_term_no_sum_index = deepcopy(mlist_tensor_term_index)
#     #IMPORTANTE EL [:] PARA Q CREE UNA NUEVA LISTA Y NO LA REFERENCIA SOLAMENTE  
#     # LISTA DE INDICES CON SIMBOLO _i ^j _k etc... DONDE NO SE SUMA PARA CADA TERMINO TENSORIAL
#     # SE EDITA MAS ABAJO


#     finals_index = []
    
#     for i in range(len(column_symbol)):
        
#         if column_index_sub_element[i] == sub_element_index:
            
#             finals_index.append(column_symbol[i])
#             # SE GUARDAN EN finals_index  LOS SIMBOLOS Q SERAN FINALMENTE LOS GENERALIZADOS
    
#      #'Tg[_i,^j]*TC2[^i,_k,_l]+TC2[^i,_k,_l]-TC2[^i,_k,_l]*Tg[^l,_p]'
    
#     # WE SPLIT THE STRING AND ASSIGN EVERY TERM TO A LIST

#     pattern = '([\+ \-]+)'
#     list_strings = [i.strip() for i in re.split(pattern, element) if i.strip()]
#     #GUARDA LOS SIGNOS Y LOS TENSORES, TODO EN UN SOLO ARREGLO

#     #['-','Tg[_i,^j]*TC2[^i,_k,_l]','+','TC2[^i,_k,_l]','-','TC2[^i,_k,_l]*Tg[^l,_p]']
  
#     n_termino = 0

#     for string in list_strings:

#         if string !="+" and string !="-":  #SOLO SE METE AL IF SI ES UN TENSOR

#         #'Tg[_i,^j]*TC2[^i,_k,_l]'
        
#             k = 0

#             for j in range(len(column_index_sub_element)):

#                 # if column_index_sub_element[j] == n_termino and column_symbol[j] != 'none':
                
#                 if column_index_sub_element[j] == n_termino:
#                     # QUIERE DECIR QUE SI EL SIMBOLO NO ES NONE, Y ADEMAS EL NUMERO DEL TERMINO TENSORIAL COINCIDE CON
#                     # EL TERMINO QUE ESTAMOS EXAMINANDO, OBVIAMENTE EL INDICE ESTA REPETIDO, LUEGO SE SUMA SOBRE ESTE INDICE
                    
#                     try:
#                         mlist_tensor_term_no_sum_index[n_termino].remove('^' + column_symbol[j])
#                         mlist_tensor_term_no_sum_index[n_termino].remove('_' + column_symbol[j])
                        
#                     except ValueError:
#                         pass
    
#             n_termino += 1
    
#     order_list_no_sum = []

#     for i in range(n_termino):
        
#         data1 = mlist_tensor_term_index[i]
        
#         data2 = mlist_tensor_term_no_sum_index[i]
        
#         list_1 = list(set(data1) - set(data2))
        
#         list_1 = sorted(list_1, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower()) 
#         # ORDENA LA LISTA DE LOS INDICES QUE SE SUMAN

#         mlist_tensor_term_si_sum_index.append(list_1)
        
#         bla = sorted(mlist_tensor_term_no_sum_index[i], key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())
#         # ORDENA LA LISTA DE LOS INDICES QUE NO SE SUMAN
        
#         order_list_no_sum.append(bla)

    
#     return element , mlist_tensor_term_si_sum_index, order_list_no_sum

# def funcion_tensor(tensor_x):

#     # recibe a*T[^mu,_nu,^xi,^chi]

#     tensor_x = tensor_x.replace('[_','_{')
#     tensor_x = tensor_x.replace('[^','^{')
#     tensor_x = tensor_x.replace(',_','}{}_{')
#     tensor_x = tensor_x.replace(',^','}{}^{')
#     tensor_x = tensor_x.replace(']','}')   

#     return tensor_x

# def string_to_latex(string):   #convierte lo que hay entre dos signos a version latex
#                                #ejemplo:  Tg[_i,^j,_k]*D(TC2[^i,^k,_l]*D(Tw[^u],_h),_u)
#                                 # Tg[_i,^j,_k]*D(TC2[^i,^k,_l]*D(Tw[^u$$_h),_u)
#     new_string_list = []

#     #print('String en string to latex',string)
    
#     i = 0
    
#     while i < len(string):
        
#         if string[i] != 'C' and string[i] != 'D' and string[i].isalpha() == True:
            
#             j = i
            
#             while j < len(string) and string[j] != ']':

#                 j += 1
                
#             new_string_list.append(funcion_tensor(string[i:j+1]))
            
#             i = j+1
            
#         elif string[i] == 'D':
            
#             j = i
            
#             k = 0
            
#             found = False
            
#             while found == False:
                
#                 if string[j] == '(':
                    
#                     k += 1
                    
#                 elif string[j] == ')' and k != 0:
                    
#                     k -= 1
                
#                 if string[j] == ')' and k == 0:
                    
#                     found = True
                    
#                     break

#                 j += 1
                
#             # j contiene la posicion del ')' correspondiente a la derivada que estamos viendo
            
#             l = j-1
            
#             while string[l] != ',':
                
#                 l = l - 1
       
#             index_dif = string[l+2:j]     
#             #',_r,_u,_v'
            
#             index_dif = index_dif.replace("_","")

#             #print('index dif array', index_dif)

#             init_derivada = '\\frac{\\partial}{\\partial x^{' + index_dif + '}'+'}'
         

#             # HAY QUE AGREGAR RECURSIVIDAD
             
#             new_string_list.append(init_derivada)
            
#             string = string[:l+2]+string[j:]
            
#             i += 1
        
#         elif string[i] == 'C':
            
#             j = i
            
#             k = 0
            
#             found = False
            
#             while found == False:
                
#                 if string[j] == '(':
                    
#                     k += 1
                    
#                 elif string[j] == ')' and k != 0:
                    
#                     k -= 1
                
#                 if string[j] == ')' and k == 0:
                    
#                     found = True
                    
#                     break

#                 j += 1
                
#             # j contiene la posicion del ')' correspondiente a la derivada que estamos viendo
            
#             l = j-1
            
#             while string[l] !=',':
                
#                 l = l - 1
       
#             index_dif = string[l+2:j]     
#             #',_r,_u,_v'

#             #print('INDEX DIF: %s'%index_dif)
            
#             index_dif = index_dif.replace("_","")

#             #print('INDEX DIF: %s'%index_dif)
                    
#             new_string_list.append('\\nabla_{%s}'%index_dif)
            
#             string = string[:l+2]+string[j:]
            
#             i += 1
            
#         else:
            
#             new_string_list.append(string[i])
            
#             i += 1



#     string= ''.join(new_string_list)
    
#     i = 0

#     #print('string antes del replace',string)

#     string = string.replace(',_)',')')

#     #print(string)

#     string = string.replace('(','\\left(')
#     string = string.replace(')','\\right)')

#     #print('string final',string)

#     return string

# def checknames(element):

#     pattern = "([\+ \- \* \[]+)"

#     list_strings = re.split(pattern,element)

#     for i in range(len(list_strings)):
    
#         if list_strings[i] == 'christ':
            
#             list_strings[i] = "\Gamma"

#         elif list_strings[i] == 'ricci' or list_strings[i] == 'riemann':
            
#             list_strings[i] = "R"

#         elif list_strings[i] == 'einstein':
            
#             list_strings[i] = "G"

#     final_string = ''.join(list_strings)

#     return final_string



def writelatex(element,sum_over_diz_index,condition):


    element = checknames(element) # Cambia los nombres para mostrarlos correctamentes si son tensores tipicos (Ricci, Christoffel, etc.)
    
    pattern = '([\+ \-]+)'
    list_strings = [i.strip() for i in re.split(pattern, element) if i.strip()]
    #GUARDA LOS SIGNOS Y LOS TENSORES, TODO EN UN SOLO ARREGLO
    

    
    #'Tg[_i,^j,_u] TC2[^i,_k,_l] Tw[^u] +TC2[^j,_k,_l] - TC2[^j,_q , _w ]*Tg[^q,_l,_k] Tw[^w]+ D(Te[^j,_k],_r)*Tg[^r,_l,_u]* Tw[^u]'
     
    n_termino = 0
    
    new_element = []

    for string in list_strings:

        if string !="+" and string !="-":        
            
            string = string_to_latex(string)
      
            #print('string desp de string to latex',string)

            #'LO QUE VUELVE DESPUES DE TRANSFORMARLO A LATEX'
            #AQUI VUELVE EN LATEX EL TERMINO ENTERO 'TC2[^j,_q , _w ]*Tg[^q,_l,_k] Tw[^w]' SIN LOS SIGNOS + O -
        
            if condition == 'Y':

                new_element.append('\sum_{')

                for i in range(len(sum_over_diz_index)):

                    if sum_over_diz_index[i][0] == n_termino:

                        new_element.append(sum_over_diz_index[i][1])
                        new_element.append(',')

                new_element.pop()
                new_element.append('}')
                
            n_termino += 1 

        new_element.append(string)
  
    new_math_element = ''.join(new_element)
  


    new_math_element = new_math_element.replace("\sum_{none}","")  
    #elimina las sumas sobre indices inexistentes
    
    new_math_element = new_math_element.replace("*","\cdot ")
    #reemplaza los * por signos bonitos de multiplicacion

    #print('new math element',new_math_element)    

    return new_math_element   



def non_repeated_i(element):
    
    examine(element)

    element = distribute(element)
    
    r1,r2,r3,r4,r5,r6 = index_counter(element)

    non_repeated_indexes = []

    for term in r6:
    
        for index in term:
            
            if index[1] != r5[0][1]:
            
                non_repeated_indexes.append(index)

    return non_repeated_indexes


# def repeated_position_D(tensor_indexes,der_var):


#     for i in range(len(tensor_indexes)):

#         if tensor_indexes[i] == der_var: 

#             repeated_pos = i
            
#             break

#     return repeated_pos

def add_examine(left,right):

    if set(left) != set(right):

        # Deberia mostrar los indices que estan incorrectos

        raise(TensorSyntaxError('Bad index Definition'))

def mul_examine(rep):

    for i,index in enumerate(rep):

        name = index[1:] # 'i'

        for j in range(i+1,len(rep)):

            #print('rep[j]',rep[j])

            if name == rep[j][1:]:

                if rep[j][0] == index[0]:

                    #print('name,rep[j][1:]',name,rep[j][1:])

                    #print('index[0],rep[j][0]',index[0],rep[j][0])

                    raise(TensorSyntaxError('Bad'))
    
def der_examine(b):

    if len(b)<2:

        raise(TensorSyntaxError('Syntax Error.'))

    elif b[0] != '_' and b[0] != '^':

        raise(TensorSyntaxError('Wrong symbol.'))

    elif b.count(',') !=  0:

        raise(TensorSyntaxError('It must be only one index.'))

    elif b.count('_') + b.count('^') > 1:

        raise(TensorSyntaxError("Syntax Error. Problem with the '_' or '^' symbols."))

def syntax(string,rank):
    
    lista = string.split(',')

    for i in lista:
        
        if len(i) < 2:
            
            raise(TensorSyntaxError("Bad index Definition: Missing index or symbol."))
        
        elif i[0] != '_' and i[0] != '^':
            
            raise(TensorSyntaxError("Bad index Definition: Missing a '_' or a '^'."))
            
        elif i.count('_') + i.count('^') > 1:
            
            raise(TensorSyntaxError("Bad index Definition: Missing a ',' or typo error."))

    if rank < len(lista):

        raise(TensorSyntaxError("Too many indices for this tensor."))

    elif rank > len(lista):

        raise(TensorSyntaxError("Too few indices for this tensor."))

# def examine(element, display_tensor=False):

#     if '=' in element:

#         left_elem,right_elem = element.split('=')

#         element = right_elem
        

#         if '*' in left_elem or '+' in left_elem or '-' in left_elem or (left_elem.count('[') != left_elem.count(']')):

#             raise(TensorSyntaxError('Bad definition of tensor.'))


#         elif left_elem.count('[') == 0 and left_elem.count(']') == 0: # Caso escalar

#             left_indexes = []


#         elif left_elem.count('[') == 1 and left_elem.count(']') == 1: # Caso Tensor

#             left_elem = left_elem.split('[')[1].split(']')[0]
#             left_indexes = left_elem.split(',')

#         else: 

#             raise(TensorSyntaxError('Bad definition of tensor.'))
        
#         #left_indexes = left_elem.split(',')


#     element = distribute(element)

#     #print('Salida del Distribute la ptm',element)
    
#     # FOR ONE STRING IN list_strings WE CALL index_counter AND WE PASS ELEMENT LIKE ARGUMENT

#     review1, review2, review4, review5,sum_over_diz_index,list_tensor_term_index = index_counter(element)

#     # sum_over_diz_index ES UN ARREGLO DONDE EL PRIMER COMPONENTE INDICA EL NUMERO DEL TERMINO 0, 1, 2, 3... ETC DE LA ECUACION,
#     # Y EL SEGUNDO COMPONENTE INDICA EL SIMBOLO (LETRA) SOBRE LA CUAL HAY QUE SUMAR

#     todo_ok = True
    
#     if review1 == False:
        
#         todo_ok = False

#         str_err = "Hay variables que se repiten mas de una vez. Suma sobre indices mal definida."

#         raise(TensorSyntaxError(str_err))
        
#     elif review2 == False:
        
#         todo_ok = False

#         str_err = "error en simbolo. Signo ^ o _ mal definido."

#         raise(TensorSyntaxError(str_err))
         
#     elif all(x==review4[0] for x in review4) == False:
        
#         todo_ok = False
        
#         str_err = "error indices contravariantes en la expresion"

#         raise(TensorSyntaxError(str_err))
        
#     elif all(x==review5[0] for x in review5) == False:
        
#         todo_ok = False

#         str_err = "error indices covariantes en la expresion"

#         raise(TensorSyntaxError(str_err))
           
#     elif todo_ok == True:
        
#         element,orderlist_tensor_term_si_sum_index, orderlist_tensor_term_no_sum_index= info_tensor_index(element,sum_over_diz_index, list_tensor_term_index)

#         #print('COMPARE MONCHO',left_indexes, orderlist_tensor_term_no_sum_index[0])

#         if all(x==orderlist_tensor_term_no_sum_index[0] for x in orderlist_tensor_term_no_sum_index) == True:
            
#             if 'left_indexes' in locals(): # Comprueba que los indices del lado izquierdo concuerdan con los indices del lado derecho
                
#                 #if all(x==left_indexes for x in orderlist_tensor_term_no_sum_index) == False: 

#                 if sorted(left_indexes) != sorted(orderlist_tensor_term_no_sum_index[0]):

#                     str_err = "Problema con los indices"

#                     raise(TensorSyntaxError(str_err))
                                       

#             print("Everything is well-defined.")

#             if display_tensor == True:
                        
#                 new_math_element = writelatex(element,sum_over_diz_index,'Y')

#                 for i in greek_dict.keys():

#                     if '{%s}'%i in new_math_element:

#                         new_math_element = new_math_element.replace(i,greek_dict[i])
                        
#                 display(Math(new_math_element))
                            
#             else:
#                 pass
#         else:

#             str_err = "Problema con los indices no repetidos"

#             raise(TensorSyntaxError(str_err))