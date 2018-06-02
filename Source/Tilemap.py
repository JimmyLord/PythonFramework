import pygame
import OpenGL.GL as gl
from collections import namedtuple

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework import Shader
from Framework import Sprite
from Framework import Texture

import GameBase
import GameObject
import Player

from enum import IntEnum
class TileTypes(IntEnum):
    Empty = 0
    Wall = 1

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
        self.game = game

        # Create a tilemap.
        self.tilemap = [ TileTypes.Empty ] * self.width * self.height

        # Place walls around the edges for testing.
        for x in range( 0, self.width ):
            self.tilemap[0 * self.width + x] = TileTypes.Wall
            y = (self.height-1)
            self.tilemap[y * self.width + x] = TileTypes.Wall

        for y in range( 0, self.height ):
            self.tilemap[y * self.width + 0] = TileTypes.Wall
            x = self.width - 1
            self.tilemap[y * self.width + x] = TileTypes.Wall

        tileProperty = namedtuple( 'tileProperty', ['texture', 'walkable'] )
        self.tileProperties = [ tileProperty( self.game.textureTileFloor, True ),
                                tileProperty( self.game.textureTileWall, False ), ]
        
        # print( self.tilemap )

    def onEvent(self, event):
        pass

    def update(self, deltaTime):
        pass

    def draw(self):
        # Draw all the tiles in the tilemap.
        for y in range( 0, self.height ):
            for x in range( 0, self.width ):
                tileType = self.tilemap[y * self.width + x]
                
                # textureChoices = { TileTypes.Empty: self.game.textureTileFloor,
                #                    TileTypes.Wall:  self.game.textureTileWall }
                # textureToUse = textureChoices.get( tileType )

                # if tileType == TileTypes.Empty:
                #     textureToUse = self.game.textureTileFloor
                # if tileType == TileTypes.Wall:
                #     textureToUse = self.game.textureTileWall
                
                textureToUse = self.tileProperties[tileType].texture

                position = [ self.tilemapPosition[0] + self.tileSize[0] * x,
                             self.tilemapPosition[1] + self.tileSize[1] * y ]
                self.game.sprite.draw( position, self.tileSize, textureToUse )
        pass