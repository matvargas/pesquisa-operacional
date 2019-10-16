import logging
from tableau import Tableau
from fractions import Fraction
from tools import Tools
import copy
import numpy as np
import sys

class Simplex:

    def get_tableau_costs_vector(tableau):
        return tableau[0][int((len(tableau.T) - 1) / 3): len(tableau.T) - 1]

    def get_tableau_costs_vector_starting_index(tableau):
        return int((len(tableau.T) - 1) / 3)

    def get_tableau_b_vector(tableau):
        return tableau.T[len(tableau.T) - 1][1:]

    def get_tableau_b_vector_whithout_optm(tableau):
        return tableau.T[len(tableau.T) - 1][:]

    def get_tableau_a_matrix(tableau):
        return tableau[1:, int((len(tableau.T) - 1) / 3): len(tableau.T) - 1]

    def get_tableau_optimal(tableau):
        return tableau[0, len(tableau[0, :]) - 1]

    def get_certificate(tableau):
        return tableau[0][0: int((len(tableau.T) - 1) / 3)]

    def get_optimal(matrix_tableau):
        return matrix_tableau[0][len(matrix_tableau[0, :]) - 1]

    def define_bases(bases, row, column):

        logging.debug("Defining bases on value ({},{})".format(row, column))

        for i, base in enumerate(bases):
            if base[0] == row and base[1] != column:
                logging.debug("Removing base: {} from bases list: {}".format(base, bases))
                bases.remove(base)
                new_base = (row, column)
                bases.append(new_base)
                logging.debug("Inserting base: {} on bases list".format(new_base))
                logging.debug("New bases list {} ".format(bases))
                return
            else:
                new_base = (row, column)
                if new_base not in bases:
                    bases.append(new_base)
                    logging.debug("Inserting base: {} on bases list".format(new_base))
                    logging.debug("New bases list {} ".format(bases))
                    return
                else:
                    logging.debug("Base: {} already on bases list".format(new_base))

        if len(bases) == 0:
            new_base = (row, column)
            bases.append(new_base)
            logging.debug("Inserting base: {} on bases list".format(new_base))
            logging.debug("New bases list {} ".format(bases))
            return

    def prepare_auxiliar_matrix(tableau, bases):
        logging.debug("Preparing auxiliar matrix for operations")

        # Make a copy of matrix to operate over without changing the original values
        matrix_aux = copy.copy(tableau.matrix_tableau)

        # On the auxiliar matrix, the costs of initial columns are zero
        matrix_aux[0, :] *= 0

        # Creating the aditional columuns
        aditional_cols = Tools.identity(tableau.restrictions)

        # Additional values on costs vector
        aditional_costs = [1] * tableau.restrictions

        extension_matrix = []

        extension_matrix = np.insert(aditional_cols, 0, aditional_costs, 0)

        for col_index in range(len(extension_matrix[0, :])):
            matrix_aux = np.insert(matrix_aux,
                                   len(tableau.matrix_tableau[0, :]) - 1 + col_index,
                                   extension_matrix[:, col_index],
                                   1)
        tmp_row = 1
        for index in range(len(matrix_aux[0, :]) - len(extension_matrix[0, :]) - 1,
                               len(matrix_aux[0, :]) - 1):
            Simplex.define_bases(bases, tmp_row, index)
            tmp_row += 1

        logging.debug("The auxiliar matrix will be: ")
        Tableau.print_tableau(matrix_aux)

        return matrix_aux, bases

    def run_auxiliar_matrix_operations(matrix_aux, bases, restrictions):
        logging.debug("Running auxiliar matrix operations")

        max_iterations = len(bases) - 1

        for i, base in enumerate(bases):
            Simplex.pivotate(base[0], base[1], matrix_aux, bases)
            if i >= max_iterations:
                break

        logging.debug("All operations over auxiliar are done!")
        Tableau.print_tableau(matrix_aux)

        if Simplex.get_optimal(matrix_aux) < 0:
            logging.debug("Matrix Auxiliar optimal -> {} is lower than 0 so Original matrix is unfeasible".format(Simplex.get_optimal(matrix_aux)))
            print("inviavel")
            for value in range(0, restrictions):
                print(matrix_aux[0, value], end=" ")
            print("")
            sys.exit()


    def show_results(tableau, bases, result):
        logging.debug("End iteration over tableau, showing the results")

        if result == 'optimal':
            print("otima")

            if logging.getLogger().level == 10:
                print(Simplex.get_tableau_optimal(tableau.matrix_tableau))
            else:
                print(float(Simplex.get_tableau_optimal(tableau.matrix_tableau)))

            bases = Tools.Sort_Tuple(bases)

            logging.debug("The final bases list was: {}".format(bases))

            for value in bases:
                if value[1] in range(Simplex.get_tableau_costs_vector_starting_index(tableau.matrix_tableau),
                        Simplex.get_tableau_costs_vector_starting_index(tableau.matrix_tableau)
                                          + len(tableau.costs)):
                    if logging.getLogger().level == 10:
                        print(Simplex.get_tableau_b_vector(tableau.matrix_tableau)[value[0] - 1], end=" ")
                    else:
                        print(float(Simplex.get_tableau_b_vector(tableau.matrix_tableau)[value[0] - 1]), end=" ")
                else:
                    print("0.0", end="")
            print("")

            for value in Simplex.get_certificate(tableau.matrix_tableau):
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

        if any (n < 0 for n in tableau.matrix_tableau.T[len(tableau.matrix_tableau.T) - 1]):
            is_b_positive = False

        bases = []

        if is_b_positive:
            logging.debug("B vector has only positive values")
            count = 1
            for x in range(int((len(tableau.matrix_tableau.T) - 1)/3) + int((len(tableau.matrix_tableau.T) - 1)/3), len(tableau.matrix_tableau.T) - 1):
                t = (count, x)
                bases.append(t)
                count += 1
            logging.debug("Initial bases: {}".format(bases))
        else:
            logging.debug("B vector has at least one negative value")
            logging.debug("Corverting b entry to positive by multiplying row by -1")

            while any(n < 0 for n in Simplex.get_tableau_b_vector_whithout_optm(tableau.matrix_tableau)):
                for entry_index, b_entry in enumerate(Simplex.get_tableau_b_vector_whithout_optm(tableau.matrix_tableau)):
                    if b_entry < 0:
                        tableau.matrix_tableau[entry_index, :] *= -1

            Tableau.print_tableau(tableau.matrix_tableau)

            matrix_aux, bases = Simplex.prepare_auxiliar_matrix(tableau, bases)
            Simplex.run_auxiliar_matrix_operations(matrix_aux, bases, tableau.restrictions)

        return bases

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

        bases = Simplex.define_initial_bases(tableau)

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

        Simplex.show_results(tableau, bases, result)
