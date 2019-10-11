import logging
from tableau import Tableau
from fractions import Fraction

class Simplex:

    def get_tableau_costs_vector(tableau):
        return tableau[0][int((len(tableau.T) - 1) / 3): len(tableau.T) - 1]

    def get_tableau_costs_vector_starting_index(tableau):
        return int((len(tableau.T) - 1) / 3)

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

        if any (n < 0 for n in tableau.T[len(tableau.T) - 1]):
            is_b_positive = False

        viable_bases = []

        if is_b_positive:
            logging.debug("B vector has only positive values")
            viable_bases.extend(range(int((len(tableau.T) - 1)/3) + int((len(tableau.T) - 1)/3), len(tableau.T) - 1 ))
            logging.debug("Viable bases: {}".format(viable_bases))
        else:
            logging.debug("B vector has at least one negative value")

        return viable_bases

    def pivotating(value, pivotal_row, column_index, matrix_tableau):

        msg = "Zeroing column {} from A[:][{}]".format(matrix_tableau[:, column_index], column_index)
        logging.debug(msg)
        for n in range(0, len(matrix_tableau[:, 0])):
            if matrix_tableau[n][column_index] != 0:
                v = Fraction(matrix_tableau[n][column_index]/value)
                matrix_tableau[n][column_index] = Fraction(matrix_tableau[n][column_index], v)

        msg = "Pivotating the other columns and rows of A matrix"
        logging.debug(msg)

        for row in range(len(matrix_tableau[:, :])):
            if row != pivotal_row:
                print(row)


    def define_lower_value(a_column, b_vector):

        lowest_value = Fraction(99999999, 1)
        pivot_row = -1

        logging.debug('A column corresponding ' + str(a_column))
        for n in range(0, len(b_vector)):
            logging.debug('b/a[n] = ' + str(b_vector[n]) + '/' + str(a_column[n]))
            if b_vector[n] != 0 and a_column[n] != 0:
                value = Fraction(b_vector[n], a_column[n])
                if value < lowest_value:
                    lowest_value = value
                    pivot_row = n

        msg = "Lowest value is {} on row #{} ".format(lowest_value, pivot_row + 1)
        logging.debug(msg)

        return lowest_value, pivot_row



    def do_simplex(tableau):
        
        # viable_bases = Simplex.define_viable_bases(tableau.matrix_tableau)

        logging.debug('\n ======================== \n =   STARTING SIMPLEX   = \n ========================')

        c_vector = Simplex.get_tableau_costs_vector(tableau.matrix_tableau)
        b_vector = Simplex.get_tableau_b_vector(tableau.matrix_tableau)
        a_matrix = Simplex.get_tableau_a_matrix(tableau.matrix_tableau)
        c_starting_index = Simplex.get_tableau_costs_vector_starting_index(tableau.matrix_tableau)

        logging.warn('!!!!!!! VERIFY THE STARTING INDEX OF COSTS VECTOR !!!!!!!!! --> ' + str(c_starting_index))

        count = 0

        pivotal_column = -1

        # Iterate over costs vector looking for < 0 values
        while any(n < 0 for n in Simplex.get_tableau_costs_vector(tableau.matrix_tableau)) and count < 1:
            for cost_index, cost in enumerate(Simplex.get_tableau_costs_vector(tableau.matrix_tableau)):
                if cost < 0:

                    logging.debug('Index of cost = ' + str(cost_index) + ' cost ' + str(cost))

                    # Find the lower value over b[i]/a[c_index][i]
                    lower_value, pivotal_row = Simplex.define_lower_value(a_matrix[:, cost_index], b_vector)

                    # Pivotating
                    Simplex.pivotating(lower_value, pivotal_row, cost_index + c_starting_index, tableau.matrix_tableau)

            count += 1





