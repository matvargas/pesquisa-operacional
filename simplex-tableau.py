SHOW_OUTPUTS = False
LOWER_VALUE = 10000
PRECISION = 4

def ShowTableau(c, a, b, certificate, optimal):
    print("\n")
    print("c[]: {}".format(c))

    print("A[] :")
    for i in range(len(a)):
        for j in range(len(a[0])):
            print(a[i][j], end = '    ')
        print("")

    print("b[] : {}".format(b))
    print("certificate[] : {}".format(certificate))
    print("Optimal : {}".format(optimal))
    print("\n")

def Identity(n):
    m=[[0 for x in range(n)] for y in range(n)]
    for i in range(0,n):
        m[i][i] = 1
    return m

def Pivotate(which_row, which_column, c, a, b, certificate, operations, optimal):

    if(SHOW_OUTPUTS): print("Starting pivotation on a[{},{}]".format(which_row, which_column))

    pivot = round(a[which_row][which_column],PRECISION)
    if(SHOW_OUTPUTS): print("Pivot: {}".format(pivot))

    if(SHOW_OUTPUTS): print("Iterate A[{},{}] over the pivot: {}".format(which_row, which_column ,pivot))
    for i in range(len(a[which_row])):
        if(a[which_row][i] != 0):
            a[which_row][i] = round((a[which_row][i]/pivot),PRECISION)

    if(SHOW_OUTPUTS): print(a)

    if(SHOW_OUTPUTS): print("Iterate b[{}] over the pivot: {}".format(which_row, pivot))
    if(b[which_row] != 0):
        b[which_row] = round((b[which_row]/pivot),PRECISION)

    if(SHOW_OUTPUTS): print(b)

    if(SHOW_OUTPUTS): print("Iterate operations[{},{}] over the pivot: {}".format(which_row, which_column ,pivot))
    for i in range(len(operations[which_row])):
        if(operations[which_row][i] != 0):
            operations[which_row][i] = round((operations[which_row][i]/pivot),PRECISION)

    if(SHOW_OUTPUTS): print(operations)

    value = round(((c[which_column]/a[which_row][which_column]) * -1),PRECISION)
    if(SHOW_OUTPUTS): print("The value: {} will be use to set 0 on c[{}] -> {}".format(value, which_column, c[which_column]))
    for i in range(len(a[which_row])):
        if(a[which_row][i] != 0):
            c[i] = round((c[i] + (a[which_row][i] * value)),PRECISION)

    optimal = round((optimal + (b[which_row] * value)),PRECISION)
    if(SHOW_OUTPUTS):  print("Partial optimal: {}".format(optimal))

    for i in range(len(certificate)):
        certificate[i] = round((certificate[i] + (operations[which_row][i] * value)),PRECISION)

    for i in range(len(a)):
        if(i != which_row):
            if(a[i][which_column] != 0):
                value = round(((a[i][which_column]/a[which_row][which_column]) * -1),PRECISION)

                for j in range(len(a[0])):
                    a[i][j] = round((a[i][j] + (a[which_row][j] * value)),PRECISION)

                b[i] = round((b[i] + (b[which_row] * value)),PRECISION)

    return(c, a, b, certificate, operations, optimal)


def ConvertToStandardForm(r, v, c, a, b):
    if(SHOW_OUTPUTS): print("Starting standard form convertion")

    certificate = [0] * r

    operations = Identity(r)
    gap_vars = Identity(r)

    negative_b_rows = []

    c = c + [0] * r

    for i in range(len(c)):
        c[i] = c[i] * -1

    for i in range(len(b)):
            if(b[i] < 0):
                negative_b_rows.append(i)
                b[i] = b[i] * -1

    for i in range(len(a)):
        if(i in negative_b_rows):
            l = a[i] + gap_vars[i]
            l = [x * -1 for x in l]
            a[i] = l
        else:
            a[i] = a[i] + gap_vars[i]

    del negative_b_rows[:]

    if(SHOW_OUTPUTS):
        print("Tableau on standard form: ")
        ShowTableau(c, a, b, certificate, 0)

    return (certificate, operations, a, c)

def Primal(c, a, b, certificate, operations, optimal):
    if(SHOW_OUTPUTS): print("Starting primal")

    if(SHOW_OUTPUTS): print("Looking for lower negative value on C[]: {}".format(c))

    viable_bases = []

    lower_c_value_index = -1
    lower_c_value = LOWER_VALUE

    for i in range(len(c)):
        if(c[i] < lower_c_value):
            lower_c_value = c[i]
            lower_c_value_index = i

    while(lower_c_value < 0):

        if(SHOW_OUTPUTS): ShowTableau(c, a, b, certificate, optimal)
        if(SHOW_OUTPUTS): print("Lower value is {} on c[{}]".format(lower_c_value, lower_c_value_index))
        if(SHOW_OUTPUTS): print("Running tableau for c[{}]".format(lower_c_value_index))

        lower = LOWER_VALUE

        for i in range(len(b)):
            if(b[i] != 0):

                if(SHOW_OUTPUTS): print("Minimizing: {}/{}".format(b[i],a[i][lower_c_value_index]))

                a_entry = round(a[i][lower_c_value_index],PRECISION)

                if(a_entry != 0):

                    b_over_a = round(b[i]/a_entry,PRECISION)

                    if(b_over_a > 0 and b_over_a < lower):
                        lower = b_over_a
                        which_row = i
                        which_column = lower_c_value_index

        if(SHOW_OUTPUTS): print("Lower value is {} on row #{}".format(lower, which_row))

        viable_bases.append((which_row,which_column))
        c, a, b, certificate, operations, optimal = Pivotate(which_row, which_column, c, a, b, certificate, operations, optimal)

        lower_c_value_index = -1
        lower_c_value = LOWER_VALUE

        for i in range(len(c)):
            if(c[i] < lower_c_value):
                lower_c_value = c[i]
                lower_c_value_index = i

    return(c, a, b, certificate, operations, optimal, viable_bases)


def Dual(c, a, b, certificate, operations, optimal):
    if(SHOW_OUTPUTS): print("Starting dual")

    b_index = 0
    plus_one = True
    while (b_index < len(b)):
        if(b[b_index][0] < 0):

            b_negative_row = b_index


            if(SHOW_OUTPUTS): ShowTableau(c, a, b, certificate, optimal)
            if(SHOW_OUTPUTS): print("Negative entry found on b[{}] -> {}".format(b_negative_row, b[b_negative_row][0]))

            lower = LOWER_VALUE
            for i in range(len(a[b_negative_row])):
                if(c[i] != 0 and a[b_negative_row][i] != 0):
                    if(a[b_negative_row][i] < 0 and c[i]/(-1 * a[b_negative_row][i]) < lower):
                        if(SHOW_OUTPUTS): print("Minimizing: {}/{}".format(c[i],(-1 * a[b_negative_row][i])))
                        which_row = b_negative_row
                        which_column = i
                        lower = c[i]/(-1 * a[b_negative_row][i])

            if(SHOW_OUTPUTS): print("Lower value is {} on a[{},{}]".format(lower, b_negative_row, which_column))
            c, a, b, certificate, operations, optimal = Pivotate(which_row, which_column, c, a, b, certificate, operations, optimal)
            b_index = 0
            plus_one = False
        if(plus_one):
            b_index += 1
        else:
            plus_one = True
    if(SHOW_OUTPUTS): ShowTableau(c, a, b, certificate, optimal)

def Auxiliar(r, v, c, a, b):
    if(SHOW_OUTPUTS): print("Starting Primal method with auxiliar matrix")

    certificate, operations, a , c = ConvertToStandardForm(r, v, c, a, b)
    optimal = 0
    aux_optimal = 0

    if(SHOW_OUTPUTS): print("Adding auxiliar matrix to the tableau")

    aux_certificate = certificate
    aux_a = a
    aux = Identity(r)
    aux_c = [0] * (len(c) + r)

    i = 1
    while(i <= r):
        aux_c[len(aux_c) - i] = 1
        i += 1

    for i in range(len(aux_a)):
        aux_a[i] = aux_a[i] + aux[i]

    if(SHOW_OUTPUTS): print("New tableau with auxiliar matrix")
    if(SHOW_OUTPUTS): ShowTableau(aux_c, aux_a, b, aux_certificate, aux_optimal)

    inerval = range(len(aux_a[0]) - r - 1,len(aux_a[0]) - 1)
    count = 0

    for i in inerval:
        aux_c, aux_a, b, aux_certificate, operations, aux_optimal = Pivotate(count, len(aux_a[0]) - r + count, aux_c, aux_a, b, aux_certificate, operations, aux_optimal)
        count += 1

    if(SHOW_OUTPUTS): print("New tableau on canonical form")
    if(SHOW_OUTPUTS): ShowTableau(aux_c, aux_a, b, aux_certificate, aux_optimal)

    aux_c, aux_a, b, aux_certificate, operations, aux_optimal, viable_bases = Primal(aux_c, aux_a, b, aux_certificate, operations, aux_optimal)

    if(SHOW_OUTPUTS): print("Result of auxiliar")
    if(SHOW_OUTPUTS): ShowTableau(aux_c, aux_a, b, aux_certificate, aux_optimal)
    if(SHOW_OUTPUTS): print("Bases: {}".format(viable_bases))

    if(SHOW_OUTPUTS): print("Using the result of auxiliar on original")

    certificate = [0] * r
    operations = Identity(r)

    original = [ [ 0 for i in range(len(c)) ] for j in range(r) ]

    for i in range(len(original)):
        for j in range(len(c)):
            original[i][j] = aux_a[i][j]

    if(SHOW_OUTPUTS): ShowTableau(c, original, b, certificate, optimal)

    count = 0

    for i in viable_bases:
        c, original, b, certificate, operations, optimal = Pivotate(i[0], i[1], c, original, b, certificate, operations, aux_optimal)
        count += 1

    if(SHOW_OUTPUTS): print("Original tableau on canonical form")
    if(SHOW_OUTPUTS): ShowTableau(c, original, b, certificate, optimal)

    c, original, b, certificate, operations, optimal, viable_bases = Primal(c, original, b, certificate, operations, optimal)
    result = PrepareResult(v,c,a,b,viable_bases)
    for i in range(len(certificate)):
        certificate[i] = round(certificate[i],1)

    if(optimal > 0):
        print('otima')
        print(round(optimal,1))
        print(result)
        print(certificate)
    return

    if(SHOW_OUTPUTS): ShowTableau(c, original, b, certificate, optimal)

    return

def PrepareResult(v,c,a,b,viable_bases):
    if(SHOW_OUTPUTS): print("Preparing result vector")
    result = [0] * v

    if(SHOW_OUTPUTS): print("Viable bases: {}".format(viable_bases))
    if(SHOW_OUTPUTS): ShowTableau(c, a, b, [], 0)

    for i in range(len(viable_bases)):
        if(SHOW_OUTPUTS): print("Partial result: {}".format(result))
        if(SHOW_OUTPUTS): print("Define if {} will be shown on result".format(viable_bases[i][1]))
        if(viable_bases[i][1] < len(result)):
            result[viable_bases[i][1]] = round(b[viable_bases[i][0]],1)

    return result

def SimplexTableau(r, v, c, a, b):

    c_verifier = [x * -1 for x in c]

    if(any(n < 0 for n in c_verifier)):

        if(SHOW_OUTPUTS): print("c[] -> {} has a negative number, so we cannot use dual method.".format(c))

        if(any(n < 0 for n in b)):
            Auxiliar(r, v, c, a, b)
            return
        else:
            certificate, operations, a , c = ConvertToStandardForm(r, v, c, a, b)
            optimal = 0
            c, a, b, certificate, operations, optimal, viable_bases = Primal(c, a, b, certificate, operations, optimal)
            result = PrepareResult(v,c,a,b,viable_bases)

            for i in range(len(certificate)):
                certificate[i] = round(certificate[i],1)

            if(optimal > 0):
                print('otima')
                print(round(optimal,1))

                for i in result:
                    print(i, end = " ")

                print("")

                for i in certificate:
                    print(i, end = " ")
            return
    else:
        Dual(c, a, b, certificate, operations, optimal)
        return


def main():
    vars_and_restrictions = input()
    vars_and_restrictions = vars_and_restrictions.split()

    r = int(vars_and_restrictions[0])
    v = int(vars_and_restrictions[1])

    if (SHOW_OUTPUTS): print("Number of restrictions: {}".format(r))
    if (SHOW_OUTPUTS): print("Number of variables: {}".format(v))

    c_input = input()
    c_list = list(c_input.split())
    c = []
    for i in range(len(c_list)):
        c.append(int(c_list[i]))

    if (SHOW_OUTPUTS): print("Vector C[]: {}".format(c))

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


    if (SHOW_OUTPUTS): print("Vector A[]: {}".format(a))
    if (SHOW_OUTPUTS): print("Vector B[]: {}".format(b))

    SimplexTableau(r,v,c,a,b)

main()