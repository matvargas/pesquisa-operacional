#!/usr/bin/python
showOutputs = True

def identity(n):
    m=[[0 for x in range(n)] for y in range(n)]
    for i in range(0,n):
        m[i][i] = 1
    return m

def simplex_tableau(r, v, c, a, b):
    certificate = [0] * r
    operations = identity(3)
    gap_vars = identity(3)
    print(operations)

r = 3
v = 3
c = [2,4,8]
a = [[1,0,0],[0,1,0],[0,0,1]]
b = [[1],[1],[1]]
simplex_tableau(r,v,c,a,b)