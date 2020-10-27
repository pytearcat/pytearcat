import numpy as np

from .core import display, Math, Latex
from .errors import TensorSyntaxError

def delete_blanks(element):
    
    return element.replace(" ","")

def correct_multiplication(element):
    
    s = 0

    while s < len(element)-1: 
 
        if (element[s] == ']' or element[s] == ')')  and (element[s+1].isalpha() == True or element[s+1] == '('):
        
            element = element[:s+1] + '*' + element[s+1:]  

        s = s+1
        
    return element

def parentesis_distribute(element):
    
    arr_paren = np.empty(len(element))   # arreglo de parentesis con sus indicadores
    arr_paren[:] = np.nan                # se inicializa como si no hubiese ningun parentesis
    
    arr_pareado = np.empty(len(element))   # arreglo de parentesis con sus indicadores
    arr_pareado[:] = np.nan                # se inicializa como si no hubiese ningun parentesis
    
    j = 0                                # contador de parentesis abiertos
    
    
    cant_par = 0

    
    for i in range(len(element)):
        
        if element[i] == '(':
                
            arr_paren[i] = j
            arr_pareado[i] = 1         # hay que parearlo con algun ')'
            
            cant_par = j+1             # le sumamos 1 porque el j empieza desde el 0. Aqui se cuentan la cantidad total de pares de parentesis
            
            j += 1

        elif element[i] == ')':
                
            l = i-1
                
            while np.isnan(arr_pareado[l]):    #  cuando se acaba el while, encuentra un '(' para ser pareado
                
                l = l-1
                
        
            arr_pareado[l] = np.nan
        
            arr_paren[i] = arr_paren[l]

    
    # entrega parentesis pareados indicados en el arr_paren

    return arr_paren,cant_par

def check_parentesis(arr_paren,element):
    
    for i in range(len(arr_paren)):
        
        if i > 0:
 
            if element[i] == '(' and (element[i-1] == 'D' or element[i-1] == 'C'):

                for j in range(i+1,len(arr_paren)):

                    if arr_paren[j] == arr_paren[i]:
                        
                        break
                        
                change = True
                
                for k in range(i,j-1):
                    
                    if element[k] == '+' or element[k] == '-':
                        
                        change = False
                        
                        break
                    
                if change == True:
                        
                    arr_paren[j] = arr_paren[i]
                        
                    arr_paren[i] = arr_paren[i]
                    
                    #sirve para DERIVADAS Y PARA COVARIANT DERIVATIVES

    # hasta aca el arrelo arr_paren solo tiene numeros en los parentesis que hay que expandir, es decir
    # se han eliminado todos los parentesis donde las derivadas aplican son productos, y sobre solamenete un tensor o de tipo
    # D(D(D(etc... ) ) )
    
    
    return arr_paren,element

def factores(i,j,element):
    
    list_factores = []
    
    factor = ''
    
    k = i+1

    while k <= j:
        
        if factor == '':
            
            factor +=  str(element[k])
                
        elif element[k] != '-' and element[k] != '+' and element[k] !=')':
            
            factor +=  str(element[k])
            
        elif element[k] == '-' or element[k] == '+':
            
            list_factores.append(factor)
            
            factor = str(element[k])

        elif element[k] == ')':
            
            list_factores.append(factor)
        
        k += 1
        
    return list_factores

#REVISAR ESTA FUNCION Y VER DONDE SE MULTIPLICAN Y REEMPLAZAN LOS FACTORES PARA QUE QUEDEN EN ELEMENT CUANDO 
#SE RETORNEN

def factores_der(i,j,element):
    

    element = element
    
    list_factores = []
    
    factor = ''
    
    k = i+1

    while k <= j:
   
        if factor == '':
            
            factor +=  str(element[k])
                
        elif element[k] != '-' and element[k] != '+':
            
            factor +=  str(element[k])
            
        elif element[k] == '-' or element[k] == '+':
            
            list_factores.append(factor)
            
            factor = str(element[k])

        if k == j:
            
            while factor[-1] == ',':
                
                factor = factor[:-1]
            
            list_factores.append(factor)
        
        k += 1
        
    return list_factores

#REVISAR ESTA FUNCION Y VER DONDE SE MULTIPLICAN Y REEMPLAZAN LOS FACTORES PARA QUE QUEDEN EN ELEMENT CUANDO 
#SE RETORNEN

def lado_der(i,j,element,arr_paren):
    
    factor = ''
    
    k = j+1
    
    while k < len(element):
        
        if element[k] == '(':    

            for l in range(k+1,len(arr_paren)):

                if arr_paren[l] == arr_paren[k]:
                        
                    break
                        
            factor += element[k:l+1]
            
            k = l
        
        
        
        elif (element[k-1:k+1] == '),' or element[k-1:k+1] == '],'):
            
            factor_der = factor
            
            break
            
        elif element[k] != '-' and element[k] != '+'  and  element[k] != ')' :
            
            factor +=  str(element[k])
            
        elif element[k] == '+' or element[k] == '-'  or element[k] == ')' :
            
            
            factor_der = factor    

            break
            
        if k == len(element)-1:
            
            factor_der = factor
        
        k += 1
        
    return k-1,factor_der

def lado_izq(i,j,element, arr_paren):
    
    factor = ''
    
    k = i-1 
    
    while k >= 0:
        
        if element[k] == '(':    

            for l in range(0,k+1):

                if arr_paren[l] == arr_paren[k]:
                        
                    break

            k = l

        if element[k] == '+' or element[k] == '-'  or  element[k] == '(' or k == 0:

            break
        
        k -= 1
    
    factor_izq = element[k:i]
    
    if factor_izq[0] == '(':
        
        factor_izq = factor_izq[1:]
    
    return k,factor_izq

def existe_algo(num,element):  #evalua si existe esa posicion de element
    
    if num < 0 or num >= len(element):
        
        bol = False
    
    else:
        
        bol = True
    
    return bol    

def evaluar(num,element):
    
    try:
        
        val = element[num] == '*'
    
    except:
        
        val = False
    
    return val

def evaluar_signo(num,element):
    
    try:
        
        if element[num] == '-' or element[num] == '+':

            val = True

        else:

            val = False
            
    except:
        
        val = False
    
    return val

def isDorCD(num,element):
    
    #retorne True or False
    #si es vdd q son D retorne 0 si es CD retorne 1
    
    try:
        
        if element[num] == 'D':

            bol = True
            val = 0
                
        elif element[num] == 'C':
            
            bol = True
            val = 1

        else:
            bol = False

            val = False
            
    except:
        
        bol = False
        val = False
    
    return bol,val  #bol dice si hay o no una derivada de cualquier tipo #val 0 Der, val 1 DerCov

def evaluar_paren_izq(num,element):
    
    try:
        
        if element[num] == '(':
            
            val = True
        
        else:
            
            val = False
    
    except:
        
        val = False
    
    return val

def evaluar_paren_der(num,element):
    
    try:
        
        if element[num] == ')' or element[num] == ',':
            
            val = True
        
        else:
            
            val = False
    
    except:
        
        val = False
    
    return val

def multiplicar(i,j,element,arr_paren):

    '''
    i posision de (
    j posision de )
    '''
    

    new_string = ''

    #print('Elemento en Multiplicar',element[i:j])

    if element[j-3] == ',' and isDorCD(i-1,element)[0] == False:  # aqui habra problema por el element[j-3] == ','

        #print(element[i-1:j-3])

        raise(TensorSyntaxError("Bad definition of derivative.\n Remember that it must be defined with 'C' or 'D', and check the '_' next to the derivative index."))
    
    
    if evaluar_paren_izq(i-1,element) and evaluar_paren_der(j+1,element):
        
        #HAY Q INCLUIR EL CASO DE Q ESTE PARENTESIS INTERNO RECIBIDO ESTE COMO: (()) O COMO ((),
        
        element = element[:i]  + element[i+1:j] +  element[j+1:]
    
    elif isDorCD(i-1,element)[0]:   #si es una derivada D o CD
        
        if isDorCD(i-1,element)[1] == 0:  #es una D
            
            cosa = 'D'
            
        else:                            #es una CD
            
            cosa = 'C'

        l = j
        
        while element[l] != '_':

            l = l - 1

        

        l = l - 3  #no entiendo esto


        #while element[l] == '_' and element[l-1] == ',':
        #    
        #    print('Bad definition of derivative')
        #    break
        #    #l = l - 3
        #    #D(T[_x],_x,_d,_s)

    # l+3 tiene la posicion donde esta la coma, es decir> entre (l+3)+1 <= cosas <= j-1 estan los elementos a derivar  
        
        cosa2 = element[l+2:j]
 
        list_factores = factores_der(i,l+2,element)
    
        for factor in list_factores:

            if factor[0] == '+':
                
                signo = '+'
                
                factor = factor[1:]
            
            elif factor[0] == '-':
                
                signo = '-'
                
                factor = factor[1:]
            
            else:
                
                signo = '+'
                 
            new_string += signo + cosa + '{' + factor + cosa2 + '}'
            
        try:

            if element[i-2] == '-':
                
                new_string = new_string.replace('+','BLABLASIGNO')
                new_string = new_string.replace('-','+')
                new_string = new_string.replace('BLABLASIGNO','-')
                
                element = element[:i-2] + '+' + '(' +new_string +')' + element[j+1:]
            
            elif element[i-2] == '*':
                
                element = element[:i-1]  + '(' +new_string +')' + element[j+1:]
                
            else:
                
                element = element[:i-1] + '+' + '(' +new_string +')' + element[j+1:]
        
        except:
        
            element = element[:i-1] +'(' +new_string +')' + element[j+1:]
    
    elif evaluar_signo(i-1,element) and evaluar(j+1,element) == False:
        #SI SOLO HAY SIGNO POR IZQUIERDA, ENTONCES MULTIPLICAR EL SIGNO (Y POR DERECHA NO HAY NADA)
        
        list_factores = factores(i,j,element)
        
        if element[i-1] == '-':
            
            new_string = ''
            
            for factor in list_factores:
                
                if factor[0] == '-':
                    
                    factor = '+' + factor[1:]
                
                elif factor[0] == '+':
                    
                    factor = '-' + factor[1:]
                    #CAMBIA LOS SIGNOS DE TODOS LSO FACTORES
                
                else:
                    
                    factor = '-' + factor
                    
                new_string += factor
                
            element = element[:i-1]+new_string+element[j+1:]
        
        else:
            #SI ES UN SIGNO + ENTONCES SOLO ELIMINE LOS PARENTESIS PORQ ES MULTPLICAR POR UN +
            
            element = element[:i-1]+element[i+1:j]+element[j+1:]
        
   #     element = element[1:-1]

    elif existe_algo(i-1,element) == False and evaluar(j+1,element) == False:
        #SI NO EXISTE NADA A LA IZQUERDA Y A LA DERECHA NO HAY MULTIPLICACION
        
        element = element[i+1:j]+element[j+1:]

    elif evaluar(i-1,element):

        pos_inicial, factor_izq = lado_izq(i,j,element, arr_paren)
        
        list_factores = factores(i,j,element)
            
        if factor_izq[0] == '+':
                    
            signo_factor_izq = 1
                
            factor_izq = factor_izq[1:]
                
        elif factor_izq[0] == '-':
                    
            signo_factor_izq = -1
                
            factor_izq = factor_izq[1:]
                    
        else:
                    
            signo_factor_izq = 1
            
        # multiplicamos
        
        for trozo in list_factores:
                
            if trozo[0] == '+':
                    
                signo_trozo = 1
                    
                trozo = trozo[1:]
                
            elif trozo[0] == '-':
                    
                signo_trozo = -1
                    
                trozo = trozo[1:]
                    
            else:
                    
                signo_trozo = 1
                
            var = signo_trozo*signo_factor_izq
                
            if var > 0:
                    
                signo = '+'
                
            else:
                    
                signo = '-'

            new_string += signo + factor_izq + trozo
        
        try:
            if element[j+1] == '*':

                put_in = '+('
                put_out = ')'
                
            else:
            
                put_in = ''
                put_out = ''
        
        except:
            
            put_in = ''
            put_out = ''
        
        if pos_inicial != 0:
        
            if element[:pos_inicial+1][-1] == '+' or element[:pos_inicial+1][-1] == '-':
                
                #print('opcion 1')
                
                element = element[:pos_inicial] + put_in + new_string + put_out + element[j+1:]
                
            else:
                
                #print('opcion 2')
                
                element = element[:pos_inicial+1] + put_in + new_string + put_out + element[j+1:]  

        else:
            
            #print('opcion 3')
            
            if pos_inicial-1 >= 0:
                
                init_string = element[:pos_inicial]
                
            else:
                
                init_string = ''
            
            element = init_string + put_in + new_string + put_out  + element[j+1:]
                
        #AQUI HAY Q CAMBIARLO

    elif evaluar(j+1,element):

        pos_final, factor_der = lado_der(i,j,element, arr_paren)
            
        if factor_der[0] == '+':
                    
            signo_factor_der = 1
                
            factor_der = factor_der[1:]
                
        elif factor_der[0] == '-':
                    
            signo_factor_der = -1
                
            factor_der = factor_der[1:]
                    
        else:
                    
            signo_factor_der = 1

        list_factores = factores(i,j,element)
        
        #print('FACTORES',list_factores)
        # multiplicamos

        primer_termino = True
            
        for trozo in list_factores:
                
            if trozo[0] == '+':
                    
                signo_trozo = 1
                    
                trozo = trozo[1:]
                
            elif trozo[0] == '-':
                    
                signo_trozo = -1
                    
                trozo = trozo[1:]
                    
            else:
                    
                signo_trozo = 1
                
            var = signo_trozo*signo_factor_der
                
            if var > 0:
                    
                signo = '+'
                
            else:
                    
                signo = '-'

                
            new_string += signo + trozo + factor_der
            
        element = element[:i] + '(' + new_string + ')'  + element[pos_final+1:]
        
        #HAY Q CORREGIR EL POS_FINAL, EL POS_FINAL CAMBIA SI ES UN SIGNO A SI ES UN PARENTESIS
    
    #print(element)
    element = element.replace('++','+')
    
    element = element.replace('+-','-')
    
    element = element.replace('-+','-')
    
    element = element.replace('--','+')
    
    return element

def find_interno(arr_paren,element):     #ENCUENTRA LOS PARENTESIS INTERNOS: de tipo ( jaskljaslkdjal) que no tienen () dentro
      
    paren_interno = False    
    
    for i in range(len(arr_paren)):
        
        if np.isnan(arr_paren[i]) == False:
            
            for j in range(i+1,len(arr_paren)):
                
                if arr_paren[j] == arr_paren[i]:
                    
                    break
                    
            paren_interno = True
                    
            for k in range(i+1,j-1):
                
                if np.isnan(arr_paren[k]) == False:
                    
                    paren_interno = False
                    
                    break
            
            if paren_interno == True:
                
                break
       
    if paren_interno == True:
        
        #print(i,j)
    
        element_new = multiplicar(i,j,element,arr_paren)

        if element_new != element:
            
            element = element_new
                
            arr_paren = parentesis_distribute(element)[0]
                
            element_new = find_interno(arr_paren,element)
            
            #print('Dentro del IF',element)
    else:
        
        element_new = element
    
    return element_new

def distribute(element):
    
    '''blablabla'''

    
    if '=' in element:

        raise(TensorSyntaxError("The element cannot contain an '=' sign."))

    element = delete_blanks(element)
    
    #print('delete_blanks',element)

    element = correct_multiplication(element)
    
    #print('correct multiplication',element)
    #print('INPUT:')
    #display(Math(element))
    
    arr_paren,cant_par = parentesis_distribute(element)
    
    arr_paren,element = check_parentesis(arr_paren,element)
    
    #print('parentesis', element)
    
    #print(arr_paren)
    
    element = find_interno(arr_paren,element)
    
    #print('find interno',element)
    
    element = element.replace('{','(')
    element = element.replace('}',')')    
    
    #print('FINAL', element)

    #print('OUTPUT:')
    #display(Math(element))
    
    return element


# Ejemplo:
#distribute('D(Tx[^j,_u]+D(Ty[^j],_u)*(C(Ty[^k],_k)+Tz[^b,_b]),_r)')

