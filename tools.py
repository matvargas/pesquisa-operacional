class Tools:
    def identity(n):
        m = [[0.0 for x in range(n)] for y in range(n)]
        for i in range(0, n):
            m[i][i] = 1.0
        return m
