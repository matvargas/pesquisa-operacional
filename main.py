import logging
from tableau import Tableau

logging.basicConfig(level=logging.INFO)


def main():

    logging.info('\n ======================== \n =   Reading Data   = \n ========================')

    vars_and_restrictions = input()
    vars_and_restrictions = vars_and_restrictions.split()

    r = int(vars_and_restrictions[0])
    v = int(vars_and_restrictions[1])

    logging.info("Number of restrictions: {}".format(r))
    logging.info("Number of variables: {}".format(v))

    c_input = input()
    c_list = list(c_input.split())
    c = []
    for i in range(len(c_list)):
        c.append(int(c_list[i]))

    logging.info("Costs vector: {}".format(c))

    a = []
    b = []
    for i in range(r):
        line = input().split()
        a_row = []
        for j in range(len(line)):
            if(j < v):
                a_row.append(int(line[j]))
            else:
                b.append(int(line[j]))
        a.append(a_row)


    logging.info("Matrix A[]: {}".format(a))
    logging.info("Vector B[]: {}".format(b))


    tableau = Tableau(r, v, c, a, b)
    tableau.print_tableau(tableau.matrix_tableau)

    logging.info('\n ======================== \n =   STARTING SIMPLEX   = \n ========================')

main()