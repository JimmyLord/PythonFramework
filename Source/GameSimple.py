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

class GameSimple(GameBase.GameBase):
    def __init__(self):
        # Call the GameBase constructor.
        super().__init__()

        # Load our textures.
        texturePlayer = Texture.Texture( "Data/Textures/player.png" )
        textureEnemy = Texture.Texture( "Data/Textures/enemy.png" )

        # Add some game objects to our dictionary.
        self.gameObjects['Player'] = Player.Player( [10, 7.5], self.sprite, texturePlayer )
        self.gameObjects['Enemy'] = GameObject.GameObject( [10, 2], self.sprite, textureEnemy )

    def onEvent(self, event):
        # Base game class will pass events to all gameobjects in list.
        super().onEvent( event )

    def update(self, deltaTime):
        # Base game class will update all gameobjects in list.
        super().update( deltaTime )

    def draw(self):
        # Base game class will draw all game objects.
        super().draw()
