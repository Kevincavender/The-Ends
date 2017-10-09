from Eqn_solver.EquationObject import EquationsClass


class Solver(object):
    """
    docstring
    take in list of equations
    
    """
    def __init__(self, input_equations, debug=False):
        self.looplimit = 20
        self.eqn_obj = EquationsClass(input_equations)
        self.vdict = self.eqn_obj.variable_dict()
        self.debug = debug
        self.equations = input_equations

    def original_solver(self):
        '''
        (rename to parser to reflect actual job)
        (is that a promotion or demotion?)
        :param
        self.equations

        :return:
        '''

        eqn_block = [self.equations, []]
        solvable_vars = []
        parsed = False
        count = 0
        block_num = 0

        while not parsed:
            count += 1
            # *****************************************************************
            # Loop Termination Items
            # *****************************************************************
            # Loop is terminated if:
            # A: self.looplimit is reached
            # B: Current block has run out of equations
            # C: (NEED TO ADD) Remaining Block has multiple (self-contingent) unknowns
            if count > self.looplimit:
                print("Loop Limit reached on block solver")
                execute_list = ['print("Error: Loop Limit Reached on Solver")']
                results_list = ''
                return execute_list, results_list

                # break if loop limit is reached
            # DO NOT CHANGE FROM == TO is
            elif eqn_block[block_num] == []:
                # when there are no more equations to sort,
                # terminate the loop
                eqn_block.remove([])
                # DO NOT MODIFY THIS LINE! things will break, frustration will ensue
                if eqn_block[block_num] == []:
                    eqn_block.remove([])
                if self.debug == 1:
                    print("--------------------------------------------"
                          "--------------------"
                          "\nFinal Equation Block: ")
                    for i in range(0, len(eqn_block)):
                        print("     " + str(eqn_block[i]))
                break

            # *****************************************************************
            # Working with Current Block
            # *****************************************************************

            # by default the block is not solvable
            blockissolvable = False

            # simplify the reference to the current block
            current_block = eqn_block[block_num]

            # collect variables in the current_block
            current_block_vars = EquationsClass(current_block).variables()

            # adds solvable variables to the current block variables
            block_vars = solvable_vars+current_block_vars

            # list(set()) operation to sort and remove duplicates
            block_vars = list(set(block_vars))
            block_vars = list(filter(None, block_vars))
            solvable_vars = list(set(solvable_vars))

            if self.debug is True:
                print("\nCurrent Block: " + str(current_block))
                print("Block Number: " + str(block_num + 1))
                # prints activity for debugging

            # Check if the block is already solvable
            # if variables in current block and
            #                 previous blocks
            #                 == solvable variables
            # --> revisit order of logic
            if set(block_vars) == set(solvable_vars):
                blockissolvable = True
                if self.debug == 1: print("block vars and solvable vars are the same")

            elif set(block_vars) != set(solvable_vars):
                tmp_solvable_vars = []
                next_block_equation_list = []

                for current_equation in current_block:
                    # *****************************************************************
                    # Working with Current Equation (sorting single unknowns)
                    # *****************************************************************
                    # 1. Determine if solvable
                    #       By comparing solvable vars to current equation
                    # 2. If not solvable
                    #       Push Equation to next Block
                    # 3. If solvable
                    #       Add variables to Solvable Variables
                    #       Leave Equation in current block

                    solvable = self.issolvable(current_equation, solvable_vars, False)
                    if solvable is False:
                        # move equation to next block
                        next_block_equation_list.append(current_equation)

                        if self.debug == 1: print(str(current_equation) + " is not solvable")
                    if solvable is True:
                        # add variables to solvable variables
                        tmp_eqn_vars = self.vdict[current_equation]
                        for v in tmp_eqn_vars:
                            tmp_solvable_vars.append(v)
                        if self.debug == 1: print(str(current_equation) + " is solvable")
                        # print("variables in equation test" + str(tmp_eqn_vars))

                for current_equation in next_block_equation_list:
                    eqn_block[block_num + 1].append(current_equation)
                    eqn_block[block_num].remove(current_equation)

                for variable in tmp_solvable_vars:
                    solvable_vars.append(variable)
                if self.debug == 1: print("block vars and solvable vars are not the same")
                # iterate through current block equations
                # determine if not solvable

            if self.debug == 1:
                print("Block Variables \n     " + str(block_vars))
                print("Solvable Variables \n     " + str(solvable_vars))
                print("current equation block: ")
                for i in range(0, len(eqn_block)):
                    print("     " + str(eqn_block[i]))
                print("Is block solvable: " + str(blockissolvable))

            if blockissolvable is True:
                # If the block is solvable, advance to next block
                block_num += 1
                eqn_block.append([])
                if self.debug == 1: print("next block\n--------------------------"
                                          "--------------------------------------")
                # if the block is solvable, advance the block
        # check if block is solvable
            # read previous solveable variables (list them)
            # pull out solvable
            # move unsolvable to next level

        # *****************************************************************
        # Export of solvable list of variables
        # *****************************************************************
        all_vars = sorted(set(solvable_vars))
        # executable list to be run by python interpreter
        execute_list = []
        results_list = []
        for current_block in eqn_block:
            for current_equation in current_block:
                execute_list.append(current_equation)
        for current_variable in all_vars:
            results_list.append(current_variable)
        return execute_list, results_list

    def solver_selection(self):
        """
        Will read in execute_list and apply additional solvers as nessesary?
        - python math
        - fsolve
        (solving actually happens in tmp.py)
        :return:
        """
        pass

    def issolvable(self, equation, solvablevars, debug):
        """
        takes in a single equation and variables to compare it against
        determines variables in the equation
        returns a True/False condition
        :param equation: 
            str single equation 'X2=X1+1'
        :param solvablevars:
            list of already solvable variables
        :param debug:
            set True for debug of this function
        :return solvable: 
            True if the equation, given the solvable variables
            is able to be solved
        """

        solvable = False
        svariables = self.vdict[equation]
        common_variables = list(set(svariables).intersection(solvablevars))
        if debug:
            print(svariables)
            print(solvablevars)
            print(common_variables)
        for i in common_variables:
            svariables.remove(str(i))
        if len(svariables) <= 1:
            solvable = True
        return solvable


if __name__ == "__main__":
    # test of is solvable
    import Eqn_solver.readfile as rf
    input_file = "1eqn"
    eqns = rf.readfile(input_file)
    equations_object = EquationsClass(eqns)
    print("Reading input file of name: " + input_file)
    equations = equations_object.equations
    variables = equations_object.variables()
    # print(equations)
    # print(variables)
    # print(Solver(equations).issolvable(equations[0], variables[2], 0))
    exelist, resultslist = Solver(equations, debug=True).original_solver()
    peqns = EquationsClass(eqns).equations
    print("exelist:")
    print(exelist)
    print("results list:")
    print(resultslist)
    print("equations from equations class:")
    print(peqns)
    # solve_and_print_results(peqns, exelist)


