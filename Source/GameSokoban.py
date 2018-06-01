import pygame
import OpenGL.GL as gl

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework import Shader
from Framework import Sprite
from Framework import Texture

import GameBase
import GameObject
import Tilemap
import Player

class GameSokoban(GameBase.GameBase):
    def __init__(self):
        # Call the GameBase constructor.
        super().__init__()

        # Load our textures.
        # The Sokoban tilesheet is 13x8 tiles, each is 64x64 pixels.
        tilew = 64
        tileh = 64
        self.texturePlayer = Texture.Texture( filename="Data/Textures/sokoban_tilesheet.png", bottomLeftPixel=(0*tilew,0*tileh), tileSize=(tilew,tileh) )
        self.textureBox = Texture.Texture( textureToCopy=self.texturePlayer, bottomLeftPixel=(1*tilew,7*tileh), tileSize=(tilew,tileh) )
        self.textureWall = Texture.Texture( textureToCopy=self.texturePlayer, bottomLeftPixel=(3*tilew,7*tileh), tileSize=(tilew,tileh) )

        # Our game/screen is setup as follows:
        # Screen resolution: 800 x 600
        # World area in camera view: 0,0 to 20,15
        tileSize = ( 1, 1 )
        tilemapSize = ( 9, 7 )
        tilemapPosition = ( 10 - tilemapSize[0]/tileSize[0]/2, 7.5 - tilemapSize[1]/tileSize[1]/2 )

        # Add some game objects to our dictionary.
        self.gameObjects['Map'] = Tilemap.Tilemap( self, tilemapPosition, tilemapSize, tileSize )
        self.gameObjects['Player'] = Player.Player( [10, 7.5], self.sprite, self.texturePlayer )
        self.gameObjects['Box'] = GameObject.GameObject( [10, 2], self.sprite, self.textureBox )

    def onEvent(self, event):
        # Base game class will pass events to all gameobjects in list.
        super().onEvent( event )

    def update(self, deltaTime):
        # Base game class will update all gameobjects in list.
        super().update( deltaTime )

    def draw(self):
        # Base game class will draw all game objects.
        super().draw()
