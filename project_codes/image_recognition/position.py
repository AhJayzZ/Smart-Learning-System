class Position:
    """
    class 2d-point Position:

        1. self.x, self.y can be used, default x,y are 0
        2. return x, y when it call as function

    Example:

        p1 = Position("p1")

        p1.x = 50, p1.y = 50

        x, y = p1()
    """
    POSITION_INITIAL = 0

    def __init__(self, name):
        self.name = name
        self.x = self.POSITION_INITIAL
        self.y = self.POSITION_INITIAL

    def __call__(self):
        return self.x, self.y

    def __str__(self):
        return_str = self.name + ", x: " + str(self.x) + ", y: " + str(self.y)
        return return_str
