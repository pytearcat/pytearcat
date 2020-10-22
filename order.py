import config
from misc import new_var

def setorder(var,n):

    '''
    Sets the expansion order equal to "n" around variable "var". 

    Note: 
    This sets the expansion order equal to "n", allowing the program to truncate
    all the calculations up to this order. You can also revert to a value lower
    than "n" without having to restart the kernel. However, this does not work
    if the new order is greater than the first defined order since all the 
    higher-order terms were discarded in the first execution of this function.

    '''

    config.ord_status = True

    config.ord_var = new_var(str(var))

    config.ord_n = n

def series(element):

    '''
    Compute the series of an element.
    '''

    string = "factor(series(element, x = config.ord_var, n = config.ord_n+1))"

    result = eval(string,locals(),globals())

    return result