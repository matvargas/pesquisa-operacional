#!/usr/bin/python
SHOW_OUTPUTS = True

def ShowTableau(c, a, b, certificate, optimal):
    print("\n")
    print("c[]: {}".format(c))
    print("A[] : {}".format(a))
    print("b[] : {}".format(b))
    print("certificate[] : {}".format(certificate))
    print("Optimal : {}".format(optimal))
    print("\n")

def Identity(n):
    m=[[0 for x in range(n)] for y in range(n)]
    for i in range(0,n):
        m[i][i] = 1
    return m

def Pivot(which_row, which_column, c, a, b, certificate, operations, optimal):
    
    pivot = a[which_row][which_column]
    if(SHOW_OUTPUTS): print("Pivot: {}".format(pivot))
    
    if(SHOW_OUTPUTS): print("Iterate A[{},{}] over the pivot: {}".format(which_row, which_column ,pivot))
    for i in range(len(a[which_row])):
        if(a[which_row][i] != 0):
            a[which_row][i] = a[which_row][i]/pivot
    if(SHOW_OUTPUTS): print(a)
    
    if(SHOW_OUTPUTS): print("Iterate b[{}] over the pivot: {}".format(which_row, pivot))
    if(b[which_row] != 0):
        b[which_row][0] = b[which_row][0]/pivot
     
    if(SHOW_OUTPUTS): print(b)
    
    if(SHOW_OUTPUTS): print("Iterate operations[{},{}] over the pivot: {}".format(which_row, which_column ,pivot))
    for i in range(len(operations[which_row])):
        if(operations[which_row][i] != 0):
            operations[which_row][i] = operations[which_row][i]/pivot
            
    if(SHOW_OUTPUTS): print(operations)
        
    value = (c[which_column]/a[which_row][which_column]) * -1
    if(SHOW_OUTPUTS): print("The value: {} will be use to set 0 on c[{}] -> {}".format(value, which_column, c[which_column]))
    for i in range(len(a[which_row])):
        if(a[which_row][i] != 0):
            c[i] += a[which_row][i] * value
    
    optimal += b[which_row][0] * value
    
    for i in range(len(certificate)):
        certificate[i] += operations[which_row][i] * value
        
    for i in range(len(a)):
        if(i != which_row):
            if(a[i][which_column] != 0):
                value = (a[i][which_column]/a[which_row][which_column]) * -1
                
                for j in range(len(a[0])):
                    a[i][j] += (a[which_row][j] * value)
            
                b[i][0] += (b[which_row][0] * value)
                    
                    
    
        
    return(c, a, b, certificate, operations, optimal)
    

def SimplexTableau(r, v, c, a, b):
    certificate = [0] * r
    operations = Identity(3)
    gap_vars = Identity(3)
    
    for i in range(len(a)):
        a[i] = a[i] + gap_vars[i] 

    c = c + [0] * r
    optimal = 0
    
    for i in range(len(c)):
        c[i] = c[i] * -1
    
    c_index = 0
    while (c_index < len(c)):    
        if(SHOW_OUTPUTS): ShowTableau(c, a, b, certificate, optimal)
        
        if(c[c_index] < 0 ):
            if(SHOW_OUTPUTS): print("Running tableau for c[{}]".format(c_index))
            lower = 10000
            for i in range(len(b)):
                if(b[i][0] != 0):
                    if(SHOW_OUTPUTS): print("Minimizing: {}/{}".format(b[i][0],a[i][c_index]))
                    if(a[i][c_index] != 0 and b[i][0]/a[i][c_index] < lower):
                        lower = b[i][0]/a[i][c_index]
                        which_row = i
                        which_column = c_index
            if(SHOW_OUTPUTS): print("Lower value is {} on row #{}".format(lower, which_row))
            c, a, b, certificate, operations, optimal = Pivot(which_row, which_column, c, a, b, certificate, operations, optimal)
            c_index = 0
        c_index += 1

r = 3
v = 3
c = [2,4,8]
a = [[1,0,0],[0,1,0],[0,0,1]]
b = [[1],[1],[1]]
SimplexTableau(r,v,c,a,b)