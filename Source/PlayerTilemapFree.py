import pygame
import imgui

from Framework.Vector import vec2
from GameObject import GameObject
from Tilemap import TileTypes

class PlayerTilemapFree(GameObject):
    def __init__(self, tilePosition, sprite, animationFrames, tilemap):
        super().__init__( vec2( 0, 0 ), sprite, animationFrames[0] )
        self.animationFrames = animationFrames
        self.tilemap = tilemap
        self.currentAnimation = 1 # Moving down.
        self.currentFrame = 0
        self.animationTimer = 0.2
        self.position = self.tilemap.getWorldPositionForTilePosition( tilePosition )

    def onEvent(self, event):
        super().onEvent( event )

        # Inputs will set the direction the player is moving.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction.y += 1
            if event.key == pygame.K_s:
                self.direction.y += -1
            if event.key == pygame.K_a:
                self.direction.x += -1
            if event.key == pygame.K_d:
                self.direction.x += 1
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.direction.y -= 1
            if event.key == pygame.K_s:
                self.direction.y -= -1
            if event.key == pygame.K_a:
                self.direction.x -= -1
            if event.key == pygame.K_d:
                self.direction.x -= 1        

    def doesPositionFitOnTilemap(self, position, size):
        # Check if the player's new X position is valid on this tilemap.
        tileTypeBL = self.tilemap.getTileTypeForWorldPosition( vec2( position.x,          position.y ) )
        tileTypeBR = self.tilemap.getTileTypeForWorldPosition( vec2( position.x + size.x, position.y ) )
        tileTypeTL = self.tilemap.getTileTypeForWorldPosition( vec2( position.x,          position.y + size.y ) )
        tileTypeTR = self.tilemap.getTileTypeForWorldPosition( vec2( position.x + size.x, position.y + size.y ) )

        # If it fits, set the new X position.
        if tileTypeBL == TileTypes.Empty and tileTypeBR == TileTypes.Empty and tileTypeTL == TileTypes.Empty and tileTypeTR == TileTypes.Empty:
           return True
        
        return False

    def update(self, deltaTime):
        # GameObject update will do the actual player movement.
        # super().update( deltaTime )

        collisionOffset = vec2( 0.15, 0.05 )
        playerSize = vec2( self.tilemap.tileSize.x * 0.7, self.tilemap.tileSize.y * 0.45 )
        newPosition = vec2( self.position.x + self.direction.x * self.speed * deltaTime,
                            self.position.y + self.direction.y * self.speed * deltaTime )

        # Check if the player's new X position is valid on this tilemap.  If it fits, set it.
        newPositionOnXAxis = vec2( newPosition.x + collisionOffset.x, self.position.y + collisionOffset.y )
        if self.doesPositionFitOnTilemap( newPositionOnXAxis, playerSize ):
            self.position.x = newPosition.x

        # Check if the player's new Y position is valid on this tilemap.  If it fits, set it.
        newPositionOnYAxis = vec2( self.position.x + collisionOffset.x, newPosition.y + collisionOffset.y )
        if self.doesPositionFitOnTilemap( newPositionOnYAxis, playerSize ):
            self.position.y = newPosition.y

        # Set the correct animation based on the direction we're going.
        # Animations are in this order: Up, Down, Left, Right
        # Each animation is 3 frames long.
        if self.direction.y > 0:
            self.currentAnimation = 0 # Moving up.
        if self.direction.y < 0:
            self.currentAnimation = 1 # Moving down.
        if self.direction.x < 0:
            self.currentAnimation = 2 # Moving left.
        if self.direction.x > 0:
            self.currentAnimation = 3 # Moving right.

        # Update the timer and switch frames on the animation.
        self.animationTimer -= deltaTime
        if self.animationTimer < 0:
            self.animationTimer = 0.2
            self.currentFrame += 1
            if self.currentFrame > 2:
                self.currentFrame = 0

        # If the player isn't moving, just force the first frame of the animation.
        if self.direction.x == 0 and self.direction.y == 0:
            self.currentFrame = 0

        # Set the player's current texture.
        self.texture = self.animationFrames[self.currentAnimation * 3 + self.currentFrame]

        # Debug info displayed using imgui.
        imgui.begin( "Player", True )
        changed, newvalue = imgui.slider_float2( "Position", self.position.x, self.position.y, 0, 20 )
        self.position.x = newvalue[0]
        self.position.y = newvalue[1]
        tiletype = self.tilemap.getTileTypeForWorldPosition( self.position + collisionOffset )
        imgui.text( "Tile Type: " + str(tiletype) )
        imgui.end()

    def draw(self):
        super().draw()
