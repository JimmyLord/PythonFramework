import pygame
import imgui

from Framework.Vector import vec2
from GameObject import GameObject
from Tilemap import TileTypes

class PlayerTilemapLocked(GameObject):
    def __init__(self, tilePosition, sprite, animationFrames, tilemap):
        super().__init__( vec2( 0, 0 ), sprite, animationFrames[0] )
        self.animationFrames = animationFrames
        self.tilemap = tilemap
        self.currentAnimation = 1 # Moving down.
        self.currentFrame = 0
        self.animationTimer = 0.2
        self.tilePosition = tilePosition

    def onEvent(self, event):
        super().onEvent( event )

        # Inputs will move the player.
        # Set the correct animation based on the direction we're going.
        # Animations are in this order: Up, Down, Left, Right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.currentAnimation = 0 # Moving up.
                if self.tilemap.getTilePropertiesForTilePosition( self.tilePosition.x, self.tilePosition.y+1 ).walkable:
                    self.tilePosition.y += 1
                else:
                    if self.tilemap.push( vec2(self.tilePosition.x, self.tilePosition.y+1), vec2(0,1) ):
                        self.tilePosition.y += 1

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.currentAnimation = 1 # Moving down.
                if self.tilemap.getTilePropertiesForTilePosition( self.tilePosition.x, self.tilePosition.y-1 ).walkable:
                    self.tilePosition.y -= 1
                else:
                    if self.tilemap.push( vec2(self.tilePosition.x, self.tilePosition.y-1), vec2(0,-1) ):
                        self.tilePosition.y -= 1

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.currentAnimation = 2 # Moving left.
                if self.tilemap.getTilePropertiesForTilePosition( self.tilePosition.x-1, self.tilePosition.y ).walkable:
                    self.tilePosition.x -= 1
                else:
                    if self.tilemap.push( vec2(self.tilePosition.x-1, self.tilePosition.y), vec2(-1,0) ):
                        self.tilePosition.x -= 1

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.currentAnimation = 3 # Moving right.
                if self.tilemap.getTilePropertiesForTilePosition( self.tilePosition.x+1, self.tilePosition.y ).walkable:
                    self.tilePosition.x += 1
                else:
                    if self.tilemap.push( vec2(self.tilePosition.x+1, self.tilePosition.y), vec2(1,0) ):
                        self.tilePosition.x += 1

    def update(self, deltaTime):
        # GameObject update will do the actual player movement.
        # super().update( deltaTime )

        # Move the sprite to match the player's tile position.
        self.position = self.tilemap.getWorldPositionForTilePosition( self.tilePosition )

        # If the player isn't moving, just force the first frame of the animation.
        self.currentFrame = 0

        # Set the player's current texture.
        self.texture = self.animationFrames[self.currentAnimation * 3 + self.currentFrame]

        # Debug info displayed using imgui.
        imgui.begin( "Player", True )
        changed, newvalue = imgui.slider_float2( "Position", self.position.x, self.position.y, 0, 20 )
        self.position.x = newvalue[0]
        self.position.y = newvalue[1]
        tiletype = self.tilemap.getTileTypeForWorldPosition( self.position )
        imgui.text( "Tile Type: " + str(tiletype) )
        imgui.end()

    def draw(self):
        super().draw()
