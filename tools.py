class Tools:
    def identity(n):
        m = [[0.0 for x in range(n)] for y in range(n)]
        for i in range(0, n):
            m[i][i] = 1.0
        return m

    def Sort_Tuple(tup):
        # reverse = None (Sorts in Ascending order)
        # key is set to sort using second element of
        # sublist lambda has been used
        tup.sort(key=lambda x: x[1])
        return tup