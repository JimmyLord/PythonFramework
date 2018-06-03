class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Addition: +
    def __add__(self, o):
        if type(o) is vec2:
            return vec2( self.x + o.x, self.y + o.y )
        else:
            return vec2( self.x + o, self.y + o )

    # Subtraction: -
    def __sub__(self, o):
        if type(o) is vec2:
            return vec2( self.x - o.x, self.y - o.y )
        else:
            return vec2( self.x - o, self.y - o )

    # Multiplication: *
    def __mul__(self, o):
        if type(o) is vec2:
            return vec2( self.x * o.x, self.y * o.y )
        else:
            return vec2( self.x * o, self.y * o )

    # Division: /
    def __truediv__(self, o):
        if type(o) is vec2:
            return vec2( self.x / o.x, self.y / o.y )
        else:
            return vec2( self.x / o, self.y / o )

    # Negate or Unary minus: -vec2(2,2)
    def __neg__(self):
        return vec2( -self.x, -self.y )

    # Equal to: ==
    def __eq__(self, o):
        if self.x == o.x and self.y == o.y:
            return True
        return False

    # Not equal to: !=
    def __ne__(self, o):
        if self.x != o.x or self.y != o.y:
            return True
        return False

    # The string representation: str
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

def vec2Test():
    addA = vec2(1,1)
    addB = vec2(2.0,2)
    addR = addA + addB
    print( str(addR) )

    subA = vec2(1,1)
    subB = vec2(2.0,2)
    subR = subA - subB
    print( str(subR) )

    mulA = vec2(2.3,1)
    mulR = mulA * 5
    print( str(mulR) )

    divA = vec2(9.7,1)
    divR = divA / 5
    print( str(divR) )

    negR = -vec2(1,2)
    print( str(negR) )

