import pygame
import OpenGL.GL as gl

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework import Shader
from Framework import Sprite
from Framework import Texture

import GameBase
import GameObject
import Player

class Tilemap():
    def __init__(self, game, tilemapPosition, tilemapSize, tileSize):
        # Our game/screen is setup as follows:
        # Screen resolution: 800 x 600
        # World area in camera view: 0,0 to 20,15
        self.tileSize = tileSize
        self.tilemapSize = tilemapSize
        self.width = self.tilemapSize[0]
        self.height = self.tilemapSize[1]
        self.tilemapPosition = tilemapPosition

        # Create a tilemap.
        self.tilemap = [ 0 ] * self.width * self.height

        # Place walls around the edges for testing.
        for x in range( 0, self.width ):
            self.tilemap[0 * self.width + x] = 1
            y = (self.height-1)
            self.tilemap[y * self.width + x] = 1

        for y in range( 0, self.height ):
            self.tilemap[y * self.width + 0] = 1
            x = self.width - 1
            self.tilemap[y * self.width + x] = 1
        
        print( self.tilemap )

        self.tileWall = GameObject.GameObject( [2, 5], game.sprite, game.textureWall )

    def onEvent(self, event):
        #super().onEvent( event )
        pass

    def update(self, deltaTime):
        #super().update( deltaTime )
        pass

    def draw(self):
        # super().draw() # Not calling the draw method of the base GameObject class

        # Draw all the tiles in the tilemap.
        for y in range( 0, self.height ):
            for x in range( 0, self.width ):
                if self.tilemap[ y * self.width + x ] == 1:
                    self.tileWall.position[0] = self.tilemapPosition[0] + self.tileSize[0] * x
                    self.tileWall.position[1] = self.tilemapPosition[1] + self.tileSize[1] * y
                    self.tileWall.draw()
        pass