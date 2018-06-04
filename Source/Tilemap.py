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
class GroundTypes(IntEnum):
    Normal = 0
    Goal = 1

class TileTypes(IntEnum):
    Empty = 0
    Wall = 1
    Box = 2
    BoxOnGoal = 3

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
        self.tilemapGround = [ GroundTypes.Normal ] * self.width * self.height
        self.tilemap = [ TileTypes.Empty ] * self.width * self.height

        # Define the ground properties.
        groundProperty = namedtuple( 'groundProperty', ['texture', 'walkable', 'goal'] )
        self.groundProperties = [ groundProperty( game.textureTileFloor,  True, False ),   # GroundTypes.Normal
                                  groundProperty( game.textureTileGoal,   True,  True ), ] # GroundTypes.Goal

        # Define the tile properties.
        tileProperty = namedtuple( 'tileProperty', ['texture', 'walkable', 'pushable'] )
        self.tileProperties = [ tileProperty( None,                       True, False ),   # TileTypes.Empty
                                tileProperty( game.textureTileWall,      False, False ),   # TileTypes.Wall
                                tileProperty( game.textureTileBox,       False,  True ),   # TileTypes.Box
                                tileProperty( game.textureTileBoxOnGoal, False,  True ), ] # TileTypes.BoxOnGoal

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

        self.tilemapGround[3 * self.width + 4] = GroundTypes.Goal
        self.tilemapGround[5 * self.width + 4] = GroundTypes.Goal
        self.tilemapGround[3 * self.width + 6] = GroundTypes.Goal

        # Run a solved check immediately in case map generated above is broken.
        self.checkIfSolved()
        
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
                if self.tilemapGround[y * self.width + x] == GroundTypes.Goal:
                    self.game.sprite.draw( position, vec2( self.tileSize.x, self.tileSize.y ), self.game.textureTileGoal )
                else:
                    self.game.sprite.draw( position, vec2( self.tileSize.x, self.tileSize.y ), self.game.textureTileFloor )

                # Check the tile type for this grid position and draw the texture if it's not empty.
                textureToUse = self.getTilePropertiesForTilePosition( x, y ).texture
                if textureToUse != None:
                    self.game.sprite.draw( position, vec2( self.tileSize.x, self.tileSize.y ), textureToUse )

    def checkIfSolved(self):
        # Reset the solved flag, we'll set it again if the board checks out.
        self.solved = False

        # If any GroundTypes.Goal tile doesn't have a TileTypes.BoxOnGoal above it, kick out.
        for y in range( 0, self.height ):
            for x in range( 0, self.width ):
                tileIndex = y * self.width + x
                if self.tilemapGround[tileIndex] == GroundTypes.Goal and self.tilemap[tileIndex] != TileTypes.BoxOnGoal:
                    return
        
        # The board checked out, so mark it as solved.
        self.solved = True

    def push(self, tilePosition, direction):
        tx = tilePosition.x
        ty = tilePosition.y
        oldTileIndex = ty * self.width + tx
        oldTileType = self.tilemap[oldTileIndex]

        # Check if the tile is 'pushable'.
        if self.tileProperties[oldTileType].pushable:
            tx += direction.x
            ty += direction.y
            newTileIndex = ty * self.width + tx
            
            # Check if the next tile is empty.
            newTileType = self.tilemap[newTileIndex]
            if newTileType == TileTypes.Empty:
                self.tilemap[newTileIndex] = oldTileType
                self.tilemap[oldTileIndex] = TileTypes.Empty

                # If we pushed a box onto a goal, swap the tile type.
                if self.tilemap[newTileIndex] == TileTypes.Box and self.tilemapGround[newTileIndex] == GroundTypes.Goal:
                    self.tilemap[newTileIndex] = TileTypes.BoxOnGoal
                
                # If we pushed a box off of a goal, swap the tile type.
                if self.tilemap[newTileIndex] == TileTypes.BoxOnGoal and self.tilemapGround[newTileIndex] != GroundTypes.Goal:
                    self.tilemap[newTileIndex] = TileTypes.Box

                # Since we moved a block, check if the board is solved.
                self.checkIfSolved()

                # Push succeeded.
                return True
        
        # Push failed.
        return False

    def getTilePositionForWorldPosition(self, worldPosition):
        return ( worldPosition - self.tilemapPosition ) / self.tileSize

    def getWorldPositionForTilePosition(self, tilePosition):
        return self.tilemapPosition + tilePosition * self.tileSize

    def getTileTypeForWorldPosition(self, worldPosition):
        tilePosition = ( worldPosition - self.tilemapPosition ) / self.tileSize
        if tilePosition.x < 0 or tilePosition.x >= self.tilemapSize.x:
            return None
        if tilePosition.y < 0 or tilePosition.y >= self.tilemapSize.y:
            return None
        return self.tilemap[int(tilePosition.y) * self.width + int(tilePosition.x)]

    def getTileTypeForTilePosition(self, tx, ty):
        return self.tilemap[ty * self.width + tx]

    def getTilePropertiesForTilePosition(self, tx, ty):
        tileType = self.tilemap[ty * self.width + tx]
        return self.tileProperties[tileType]
