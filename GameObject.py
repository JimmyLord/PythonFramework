
class GameObject:
    def __init__(self, position, sprite, texture):
        self.sprite = sprite
        self.texture = texture

        self.position = position
        self.direction = [ 0, 0 ]
        self.speed = 3
        self.scale = [ 1, 1 ]

    def onEvent(self, event):
        pass

    def update(self, deltaTime):
        self.position[0] += self.direction[0] * self.speed * deltaTime
        self.position[1] += self.direction[1] * self.speed * deltaTime

    def draw(self):
        self.sprite.draw( self.position, self.scale, self.texture )
