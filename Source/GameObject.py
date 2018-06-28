from Framework.Vector import vec2

class GameObject:
    def __init__(self, position, sprite, texture):
        self.sprite = sprite
        self.texture = texture

        self.position = position
        self.direction = vec2( 0, 0 )
        self.speed = 3
        self.scale = vec2( 1, 1 )

    def onEvent(self, event):
        pass

    def update(self, deltaTime):
        self.position.x += self.direction.x * self.speed * deltaTime
        self.position.y += self.direction.y * self.speed * deltaTime

    def draw(self):
        self.sprite.draw( self.position, self.scale, self.texture, 0, 0, 0 )
