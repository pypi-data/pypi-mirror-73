
from .dataflow import CellDataFlow, Cell
from .dataflow import CellException, CellNotFoundException, CellSelfReferenceException


VERSION="v0.0.4"


def print_error(c,v,ex):
    print( "error", c, v, ex )
    
def clear_error(c,v,ex):
    c.val = None
    c.error = None
