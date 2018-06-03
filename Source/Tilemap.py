import pygame
import OpenGL.GL as gl
from collections import namedtuple

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework.Vector import vec2
from Framework.Shader import Shader
from Framework.Sprite import Sprite
from Framework.Texture import Texture

from GameBase import GameBase
from GameObject import GameObject
from Player import Player

from enum import IntEnum
class TileTypes(IntEnum):
    Empty = 0
    Wall = 1
    Box = 2

class Tilemap():
    def __init__(self, game, tilemapPosition, tilemapSize, tileSize):
        # Our game/screen is setup as follows:
        # Screen resolution: 800 x 600
        # World area in camera view: 0,0 to 20,15
        self.tileSize = tileSize
        self.tilemapSize = tilemapSize
        self.width = self.tilemapSize.x
        self.height = self.tilemapSize.y
        self.tilemapPosition = tilemapPosition
        self.game = game

        # Create a tilemap.
        self.tilemap = [ TileTypes.Empty ] * self.width * self.height

        # Define the tile properties.
        tileProperty = namedtuple( 'tileProperty', ['texture', 'walkable'] )
        self.tileProperties = [ tileProperty( None, True ),
                                tileProperty( game.textureTileWall, False ),
                                tileProperty( game.textureTileBox, False ), ]

        # Place walls around the edges for testing.
        for x in range( 0, self.width ):
            self.tilemap[0 * self.width + x] = TileTypes.Wall
            y = (self.height-1)
            self.tilemap[y * self.width + x] = TileTypes.Wall

        for y in range( 0, self.height ):
            self.tilemap[y * self.width + 0] = TileTypes.Wall
            x = self.width - 1
            self.tilemap[y * self.width + x] = TileTypes.Wall

        self.tilemap[3 * self.width + 3] = TileTypes.Box
        self.tilemap[5 * self.width + 3] = TileTypes.Box
        self.tilemap[3 * self.width + 5] = TileTypes.Box
        
        # print( self.tilemap )

    def onEvent(self, event):
        pass

    def update(self, deltaTime):
        pass

    def draw(self):
        # Draw all the tiles in the tilemap.
        for y in range( 0, self.height ):
            for x in range( 0, self.width ):
                position = vec2( self.tilemapPosition.x + self.tileSize.x * x,
                                 self.tilemapPosition.y + self.tileSize.y * y )

                # Always draw a floor tile before drawing the walls/boxes/etc.
                self.game.sprite.draw( position, vec2( self.tileSize.x, self.tileSize.y ), self.game.textureTileFloor )

                # Check the tile type for this grid position and draw the texture if it's not empty.
                textureToUse = self.getTilePropertiesForTileIndex( x, y ).texture
                if textureToUse != None:
                    self.game.sprite.draw( position, vec2( self.tileSize.x, self.tileSize.y ), textureToUse )

    def getTileTypeForWorldPosition(self, worldPosition):
        tilePosition = ( worldPosition - self.tilemapPosition ) / self.tileSize
        if tilePosition.x < 0 or tilePosition.x >= self.tilemapSize.x:
            return None
        if tilePosition.y < 0 or tilePosition.y >= self.tilemapSize.y:
            return None
        return self.tilemap[int(tilePosition.y) * self.width + int(tilePosition.x)]

    def getTileTypeForTileIndex(self, tx, ty):
        return self.tilemap[ty * self.width + tx]

    def getTilePropertiesForTileIndex(self, tx, ty):
        tileType = self.tilemap[ty * self.width + tx]
        return self.tileProperties[tileType]
