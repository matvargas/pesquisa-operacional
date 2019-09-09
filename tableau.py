import logging
from tools import Tools

class Tableau:

    def __init__(self, restrictions, variables, costs, matrixA, vectorB):
        self.restrictions = restrictions
        self.variables = variables
        self.costs = costs
        self.matrixA = matrixA
        self.vectorB = vectorB

        def convert_to_standard_form(r, v, c, a, b):
            logging.info('\n =================================== \n =   CONVERTING TO STANDARD FORM   = \n ===================================')

            certificate = [0] * r

            operations = Tools.identity(r)
            gap_vars = Tools.identity(r)

            c = c + [0] * r

            tableau_lines = []

            return (certificate, operations, a, c ,b)

        self.tableau = convert_to_standard_form(self.restrictions, self.variables, self.costs, self.matrixA, self.vectorB)

    def print_tableau_nicely(self, tableau):
        tableau_columns = tableau[0]
        print(tableau_columns)


