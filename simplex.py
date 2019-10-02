import logging
from tableau import Tableau
from fractions import Fraction

class Simplex:

    def get_tableau_costs_vector(tableau):
        return tableau[0][int((len(tableau.T) - 1) / 3): len(tableau.T) - 1]

    def get_tableau_b_vector(tableau):
        return tableau.T[len(tableau.T) - 1][1:]

    def get_tableau_a_matrix(tableau):
        return tableau[1:, int((len(tableau.T) - 1) / 3): len(tableau.T) - 1]

    def pivotate(tableau, pivotal_line, pivotal_colum, pivot):
        logging.debug('\n =================================== \n =   PIVOTATING   = \n ===================================')

        # Divide the pivotal line by pivot
        # tableau = tableau[pivotal_line, :] / pivot


    def define_viable_bases(tableau):

        logging.debug('\n =================================== \n =   DEFINING VIABLE BASES   = \n ===================================')

        # If B vector has all values greater than zero, because the entri format is always <=, 
        # the base will be the matrix formed by gap_vars.

        is_b_positive = True

        if any (n < 0 for n in tableau.T[len(tableau.T) - 1 ]):
            is_b_positive = False

        viable_bases = []

        if is_b_positive:
            logging.debug("B vector has only positive values")
            viable_bases.extend(range(int((len(tableau.T) - 1)/3) + int((len(tableau.T) - 1)/3), len(tableau.T) - 1 ))
            logging.debug("Viable bases: {}".format(viable_bases))
        else:
            logging.debug("B vector has at least one negative value")

        return viable_bases

    def do_simplex(tableau):
        
        viable_bases = Simplex.define_viable_bases(tableau.matrix_tableau)

        logging.debug('\n ======================== \n =   STARTING SIMPLEX   = \n ========================')

        c = Simplex.get_tableau_costs_vector(tableau.matrix_tableau)
        b = Simplex.get_tableau_b_vector(tableau.matrix_tableau)
        a = Simplex.get_tableau_a_matrix(tableau.matrix_tableau)

        count = 0

        lowest_value = 99999999

        pivotal_line = -1
        pivotal_column = -1


        while (any (n < 0 for n in Simplex.get_tableau_costs_vector(tableau.matrix_tableau)) and count < 4):
            for cost_index, cost in enumerate(Simplex.get_tableau_costs_vector(tableau.matrix_tableau)):
                if cost < 0:
                    tableau.matrix_tableau[0][cost_index] = tableau.matrix_tableau[0][cost_index] * -1
                    tableau.print_tableau(tableau.matrix_tableau)
            count += 1





