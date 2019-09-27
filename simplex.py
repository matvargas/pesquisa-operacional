import logging
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
        
        viable_bases = Simplex.define_viable_bases(tableau)

        logging.debug('\n ======================== \n =   STARTING SIMPLEX   = \n ========================')

        c = Simplex.get_tableau_costs_vector(tableau)
        b = Simplex.get_tableau_b_vector(tableau)
        a = Simplex.get_tableau_a_matrix(tableau)

        count = 0

        lowest_value = 99999999

        pivotal_line = -1
        pivotal_column = -1

        while (count < len(c)):
            if c[count] < 0:
                for line in range(0, len(a)):
                    if b[count] != 0 and a[line][count] != 0:
                        if Fraction(b[count], a[line][count]) < lowest_value:
                            lowest_value = Fraction(b[count], a[line][count])
                            pivotal_line = line
                            pivotal_column = count
                logging.debug("Lower value under b/a is: {} on A[{}][{}]".format(lowest_value, pivotal_line, pivotal_column))
                Simplex.pivotate(tableau, pivotal_line, pivotal_line, lowest_value)
            count += 1



