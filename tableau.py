class Tableau:
    def __init__(self, restrictions, variables, costs, matrixA, vectorB):
        self.restrictions = restrictions
        self.variables = variables
        self.costs = costs
        self.matrixA = matrixA
        self.vectorB = vectorB