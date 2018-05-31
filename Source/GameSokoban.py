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

class GameSokoban(GameBase.GameBase):
    def __init__(self):
        # Call the GameBase constructor.
        super().__init__()

        # Load our textures.
        # The Sokoban tilesheet is 13x8 tiles, each is 64x64 pixels.
        tilew = 64
        tileh = 64
        texturePlayer = Texture.Texture( "Data/Textures/sokoban_tilesheet.png", (0*tilew,0*tileh), (tilew,tileh) )
        textureBox = Texture.Texture( "Data/Textures/sokoban_tilesheet.png", (1*tilew,7*tileh), (tilew,tileh) )

        # Add some game objects to our dictionary.
        self._gameObjects['Player'] = Player.Player( [10, 7.5], self.sprite, texturePlayer )
        self._gameObjects['Enemy'] = GameObject.GameObject( [10, 2], self.sprite, textureBox )

    def onEvent(self, event):
        # Base game class will pass events to all gameobjects in list.
        super().onEvent( event )

    def update(self, deltaTime):
        # Base game class will update all gameobjects in list.
        super().update( deltaTime )

    def draw(self):
        # Base game class will draw all game objects.
        super().draw()
