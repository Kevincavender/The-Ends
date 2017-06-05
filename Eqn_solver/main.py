"""
Module Docstring

THEENDS (The Ends)
THermodynamic Engineering Equations NeeD Solving

"""

__author__ = "Kevin Cavender"
__version__ = "0.0.1"
__license__ = "None atm"


import time
from Eqn_solver.readfile import readstring, readfile
from Eqn_solver.EquationsClass import EquationsClass
from Eqn_solver.Solver import Solver
from Eqn_solver.results import solve_and_print_results as results


def main(instring):
    """ Main entry point of the app 
    add: equations = EquationsClass(rf.readfile("1eqn")
    
    
    """
    start_time = time.time()
    user_input = EquationsClass(instring)
    solve = user_input.check()

    if solve == 1:
        exelist, resultslist = Solver(user_input.equations).original_solver()
        resultsout = results(user_input.entered_equations,exelist, resultslist)
        print('**************************************************')
        print('Number of Equations = ', len(user_input.equation_dict()))
        print('Number of Variables = ', len(user_input.variables()))
        print('List of Variables', ', '.join(user_input.variables()))
        print("Time Elapsed: {:.3f}s".format(time.time() - start_time))
        print('**************************************************')
    return resultsout


if __name__ == "__main__":
    """ This is executed when run from the command line """
    resultout = main(readfile("1eqn"))
    print(resultout)