from IPython.display import display as display_IP, Math as Math_IP, Latex as Latex_IP
from platform import system

OS = system()

if OS == "Darwin": # macOS
    
    core_calc = "sp"
    
elif OS == "Windows" or OS == "Linux":
    
    core_calc = "gp"
    
else: # Not determined

    core_calc = "sp"

if core_calc == 'gp':

    from giacpy import *
    import io
    from contextlib import redirect_stdout

    def get_name(element):
        
        f = io.StringIO()
        with redirect_stdout(f):
            print(element)
        element = f.getvalue()

        return element[:-1]


    def tolatex(element):

        f = io.StringIO()
        with redirect_stdout(f):
            print(latex(element))
        element = f.getvalue()

        string =  element[1:-2]

        return string

elif core_calc == 'sp':

    from sympy import *
    
    def get_name(f):

        return f.name

elif core_calc == 'se':

    from symengine import *

    def get_name(f):

        return f.get_name()







