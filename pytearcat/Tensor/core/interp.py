import re
import numpy as np
from collections import Counter
from copy import deepcopy
from .errors import TensorSyntaxError
from .greeks import greek_dict
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

    '''
    This function verifies if the syntax for the requested tensor is correct.
    '''
    
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

