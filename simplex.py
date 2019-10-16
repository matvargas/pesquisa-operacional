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

    def get_tableau_optimal(tableau):
        return tableau[0, len(tableau[0, :]) - 1]

    def get_certificate(tableau):
        return tableau[0][0: int((len(tableau.T) - 1) / 3)]

    def show_results(matrix_tableau, bases, result):
        logging.debug("End iteration over tableau, showing the results")

        if result == 'optimal':
            print("otima")

            if logging.getLogger().level == 10:
                print(Simplex.get_tableau_optimal(matrix_tableau))
            else:
                print(float(Simplex.get_tableau_optimal(matrix_tableau)))

            for value in Simplex.get_tableau_b_vector(matrix_tableau):
                if logging.getLogger().level == 10:
                    print(value, end=" ")
                else:
                    print(float(value), end=" ")
            print("")

            for value in Simplex.get_certificate(matrix_tableau):
                if logging.getLogger().level == 10:
                    print(value, end=" ")
                else:
                    print(float(value), end=" ")
            print("")

    def define_initial_bases(tableau):

        logging.debug('\n =================================== \n =   DEFINING INITIAL BASES   = \n ===================================')

        # If B vector has all values greater than zero, because the entry format is always <=,
        # the base will be the matrix formed by gap_vars.

        is_b_positive = True

        if any (n < 0 for n in tableau.T[len(tableau.T) - 1]):
            is_b_positive = False

        bases = []

        if is_b_positive:
            logging.debug("B vector has only positive values")
            count = 1
            for x in range(int((len(tableau.T) - 1)/3) + int((len(tableau.T) - 1)/3), len(tableau.T) - 1):
                t = (count, x)
                bases.append(t)
                count += 1
            logging.debug("Initial bases: {}".format(bases))
        else:
            logging.debug("B vector has at least one negative value")

        return bases

    def define_bases(bases, row, column):
        for i, base in enumerate(bases):
            if base[0] == row and base[1] != column:
                logging.debug("Removing base: {} from bases list: {}".format(base, bases))
                bases.remove(base)
                new_base = (row, column)
                bases.append(new_base)
                logging.debug("Inserting base: {} on bases list".format(new_base))
                logging.debug("New bases list {} ".format(bases))


    def pivotate(pivotal_row, cost_index, matrix_tableau, bases):

        value = Fraction(matrix_tableau[pivotal_row][cost_index])

        logging.debug("Dividing pivotal row from A[{}][:] by {}".format(pivotal_row, value))

        for n in range(len(matrix_tableau[pivotal_row, :])):
            if matrix_tableau[pivotal_row][n] != 0:
                matrix_tableau[pivotal_row][n] = Fraction(matrix_tableau[pivotal_row][n])/Fraction(value)

        Tableau.print_tableau(matrix_tableau)

        logging.debug("Pivotating matrix over value {} on A[{}][{}]".format(value, pivotal_row, cost_index))

        for row in range(len(matrix_tableau[:])):

            if row != pivotal_row:
                v = (Fraction(matrix_tableau[row, cost_index])/Fraction(matrix_tableau[pivotal_row, cost_index])) * -1

                logging.debug("Adding {} on row {} of tableau".format(v, row))

                for column in range(len(matrix_tableau[0, :])):
                    matrix_tableau[row][column] = Fraction(matrix_tableau[row][column]) + Fraction((matrix_tableau[pivotal_row][column]) * v)

        Simplex.define_bases(bases, pivotal_row, cost_index)

        return matrix_tableau, bases

    def define_lower_value(a_column, b_vector):

        logging.debug('\n ======================== \n =   DEFINIG LOWER VALUE   = \n ========================')

        lowest_value = 99999999
        pivot_row = -1

        logging.debug("A column corresponding {}".format(a_column))
        for n in range(0, len(b_vector)):
            logging.debug("b/a[n] = {}/{}".format(b_vector[n], a_column[n]))
            if b_vector[n] != 0 and a_column[n] != 0:
                value = Fraction(b_vector[n])/Fraction(a_column[n])
                if 0 < value < lowest_value:
                    lowest_value = value
                    # Since we are using the A column excluding the costs vector value,
                    # we need to shift the row number at the and plus 1
                    pivot_row = n + 1

        logging.debug("Lowest value is {} on row #{} ".format(lowest_value, pivot_row))

        return pivot_row

    def do_simplex(tableau):

        logging.debug('\n ======================== \n =   STARTING SIMPLEX   = \n ========================')

        bases = Simplex.define_initial_bases(tableau.matrix_tableau)

        b_vector = Simplex.get_tableau_b_vector(tableau.matrix_tableau)
        a_matrix = Simplex.get_tableau_a_matrix(tableau.matrix_tableau)
        c_starting_index = Simplex.get_tableau_costs_vector_starting_index(tableau.matrix_tableau)

        logging.debug('!!!!!!! VERIFY THE STARTING INDEX OF COSTS VECTOR !!!!!!!!! --> {}'.format(c_starting_index))

        count = 0

        pivotal_column = -1

        # Iterate over costs vector looking for < 0 values
        while any(n < 0 for n in Simplex.get_tableau_costs_vector(tableau.matrix_tableau)):
            for cost_index, cost in enumerate(Simplex.get_tableau_costs_vector(tableau.matrix_tableau)):
                if cost < 0:

                    logging.debug('Index of cost on cost vector = {}, value {}'.format(cost_index, cost))

                    # Find the lower value over b[i]/a[c_index][i]
                    pivotal_row = Simplex.define_lower_value(a_matrix[:, cost_index], b_vector)

                    if pivotal_row == -1:
                        logging.debug("Could not find positive relation b over A[][cost_index], so the PL is unlimited")
                        print("inviavel")
                        return

                    # Pivotating
                    tableau.matrix_tableau, bases = Simplex.pivotate(pivotal_row,
                                                              cost_index + c_starting_index,
                                                              tableau.matrix_tableau, bases)

                    Tableau.print_tableau(tableau.matrix_tableau)
        result = 'optimal'

        Simplex.show_results(tableau.matrix_tableau, bases, result)
