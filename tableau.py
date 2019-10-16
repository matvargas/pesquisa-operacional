import logging
import numpy as np
from tools import Tools
from fractions import Fraction

class Tableau:

    def __init__(self, restrictions, vars, costs, matrixA, vectorB):
        self.restrictions = restrictions
        self.vars = vars
        self.costs = costs
        self.matrixA = matrixA
        self.vectorB = vectorB

        def convert_to_standard_form(restrictions, vars, costs, a, b):
            logging.debug('\n =================================== \n =   CONVERTING TO STANDARD FORM   = \n ===================================')

            objective = 0
            certificate = [0] * restrictions
            operations = Tools.identity(restrictions)
            gap_vars = Tools.identity(restrictions)

            costs = costs + [0] * restrictions

            costs = [x * -1 for x in costs]

            array_tableu = np.concatenate((certificate, costs), axis=0)
            array_tableu = np.append(array_tableu, objective)

            for x in range(0, restrictions):
                array_tableu = np.concatenate((array_tableu, np.array(operations[x])), axis=0)
                array_tableu = np.concatenate((array_tableu, np.array(a[x])), axis=0)
                array_tableu = np.concatenate((array_tableu, np.array(gap_vars[x])), axis=0)
                array_tableu = np.append(array_tableu, b[x])

            matrix_tableu = array_tableu.reshape(restrictions + 1, len(certificate) + len(costs) + 1).astype('object')

            return matrix_tableu

        self.matrix_tableau = convert_to_standard_form(self.restrictions, self.vars, self.costs, self.matrixA, self.vectorB)

    def print_tableau(tableau):

        if logging.getLogger().level != 10:
            return

        # print(tableau)

        VERTICAL_BORDER = '|'

        for x in range(len(tableau[:, 0])):
            print(VERTICAL_BORDER, end="  ")
            for y in range(len(tableau[0, :])):
                print(tableau[x, y], end=" ")
            print(VERTICAL_BORDER, end="")
            print("")


        # print(" ")
        # fmt = "g"
        # col_maxes = [max([len(("{:" + fmt + "}").format(x)) for x in col]) for col in tableau.T]
        # for x in tableau:
        #     print(VERTICAL_BORDER, end="  ")
        #     for i, y in enumerate(x):
        #         print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end="  ")
        #     print(VERTICAL_BORDER, end="")
        #     print("")








