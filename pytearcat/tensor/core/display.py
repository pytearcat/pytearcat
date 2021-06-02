from re import findall,search
from pytearcat.tensor.core import config
from .core import get_name, latex, display_IP, Math_IP, core_calc

if core_calc == "gp":

    from .core import tolatex, expand
    from .gpwrap import gpcore, gp_pretty_latex

    # def gp_pretty_order(element):
        
    #     ord_n = config.ord_n
    #     ord_var = get_name(config.ord_var)
        
    #     if ord_var in config.greek_dict:

    #         ord_var = r"\%s"%ord_var

    #     structure = r"\%s\^\{(\d+)\} \\operatorname\{\\mathrm\{order\\_size\} \}\\left\(\%s\\right\)"%(ord_var,ord_var)

    #     exponent = findall(structure,element)

    #     if len(exponent) > 0:

    #         structure = r"%s^{%s} \operatorname{\mathrm{order\_size} }\left(%s\right)"%(ord_var,exponent[0],ord_var)

    #         final = element.replace(r"%s"%structure,r"\mathrm{O}\left(%s^{%s}\right)"%(ord_var,exponent[0]))
            
    #     elif len(exponent) == 0:

    #         structure = r"%s \operatorname{\mathrm{order\_size} }\left(%s\right)"%(ord_var,ord_var)

    #         final = element.replace(r"%s"%structure,r"\mathrm{O}\left(%s\right)"%ord_var)

    #     return final

    # def gp_pretty_latex(element):
        
    #     '''
    #     It takes a giacpy latex expression and returns a latex string that is similar to the sympy notation.
        
    #         - It rewrites the derivatives
    #         - It rewrites the expansion order
        
    #     '''
        
    #     names = {}
    #     variables = []

    #     result = element[:]
        
    #     greek_dict =config.greek_dict

    #     for i in config.fun:

    #         x = r'%s'%str(latex(i))[1:].split("\left")[0].replace('\\','').replace('{','\\{').replace('}','\\}').replace('mathrm','\\\\mathrm')

    #         names[x] = str(i).split('(')[1][:-1]

    #     for i in names:

    #         j = findall(r'(?<=\W)%s\^\{\\left\((.*?)\\right\)\}'%i,element)
            
    #         for k in j:

    #             ind = k.split(',')

    #             ini,fin = search(r'%s\^\{\\left\(%s\\right\)\}'%(i,k),element).span()
                
    #             while element[ini] != ' ' and element[ini] != ',' and element[ini] != '\\' and element[ini] != '-' and element[ini] != '+':

    #                 ini -= 1

    #             string = ''

    #             l_dict = {}

    #             for l in ind: 

    #                 l_dict[l] = ind.count(l)  
                    
    #             for l in l_dict:  # L = '1'

    #                 y = names[i].split(',')[int(l)-1]
                        
    #                 if y in greek_dict.keys():
                            
    #                     y = r'\\%s'%y
                    
    #                 if l_dict[l] == 1:
                        
    #                     string += r'\frac{\partial }{\partial %s}'%y

    #                 else:

    #                     string += r'\frac{\partial^%d }{\partial %s^%d}'%(l_dict[l],y,l_dict[l])

    #             string+= i

    #             result = result.replace(element[ini:fin],string)    

    #     for func in names:

    #         if func in greek_dict.keys():

    #             result = result.replace(func,greek_dict[func])
                
    #     if config.ord_status == True:

    #         result = gp_pretty_order(result)

    #     return result.replace('\\\\','\\').replace("\"","").replace("\\{","{").replace("\\}","}")


    #     def tolatex(element):

    #         f = io.StringIO()
    #         with redirect_stdout(f):
    #             print(latex(element))
    #         element = f.getvalue()

    #         string =  element[1:-2]

    #         return gp_pretty_latex(string)

    def display(a , b=None):    
        '''
        a is an element from giacpy
        b is a string e.g. "T^{a}_{b}^{c}"

        '''

        if not isinstance(a,gpcore):

            raise TypeError("The argument must be a single element, not a list or array.")

        if config.ord_status == True:

            a = expand(a)

        string = tolatex(a)

        string = gp_pretty_latex(string)

        if b is not None:

            string = "%s = %s"%(b,string)

        display_IP(Math_IP(string))

if core_calc == 'sp':

    import core
    
    def display(a,b = None):

        '''
        a is an element from sympy
        b is an string e.g. "T^{a}_{b}^{c}"
        
        '''

        if not isinstance(a,core.Expr):

            raise TypeError("The argument must be a single element, not a list or array.")

    
        string = str(latex(a))

        if b is not None:

            string = "%s = %s"%(b,string)
    
        display_IP(Math_IP(string))
