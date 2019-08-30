class Tools:
    def identity(n):
        m = [[0 for x in range(n)] for y in range(n)]
        for i in range(0, n):
            m[i][i] = 1
        return m