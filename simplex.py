import logging

class Simplex:

    def define_viable_bases(tableau):

        logging.debug('\n =================================== \n =   DEFINING VIABLE BASES   = \n ===================================')

        # If B vector has all values greater than zero, because the entri format is always <=, 
        # the base will be the matrix formed by gap_vars.

        is_b_positive = True

        if any (n < 0 for n in tableau.T[len(tableau.T) - 1 ]):
            is_b_positive = False

        if is_b_positive:
            logging.debug("B vector has only positive values")
            viable_bases = []
            viable_bases.extend(range(int((len(tableau.T) - 1)/3) + int((len(tableau.T) - 1)/3), len(tableau.T) - 1 ))
            print(viable_bases)
        else:
            logging.debug("B vector has at least one negative value")

