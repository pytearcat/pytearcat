from IPython.display import display as display_IP, Math as Math_IP, Latex as Latex_IP
#from platform import system
import pkg_resources

__required = {'jupyter','numpy' ,'sympy', 'tqdm','giacpy'}
__installed = {pkg.key for pkg in pkg_resources.working_set}
__missing = __required - __installed
    
if len(__missing) != 0:

    # This condition is to allow pytearcat to work in environments with jupyter-core and other 
    # jupyter instances that are not exacly recognized as jupyter. (Fixes import bug in Google Colab)

    if 'jupyter' in __missing:

        for pkg in __installed:

            if 'jupyter' in pkg:

                __missing -= {'jupyter'}

    if 'giacpy' in __missing and len(__missing) == 1:

        pass

    else:

        raise(EnvironmentError("There are missing modules:",(__missing-{'giacpy'})))


if 'giacpy' in __installed:

    core_calc = 'gp'

else:

    core_calc = 'sp'

if core_calc == 'gp':

    from .gpwrap import *
    import io
    from contextlib import redirect_stdout
    from sympy import simplify as sp_simplify, sympify as sp_sympify, latex as sp_latex, Array as sp_Array

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
