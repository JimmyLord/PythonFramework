import pygame
import OpenGL.GL as gl

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework.Vector import vec2
from Framework.Shader import Shader
from Framework.Sprite import Sprite
from Framework.Texture import Texture

from GameBase import GameBase
from GameObject import GameObject
from Player import Player

class GameSimple(GameBase):
    def __init__(self):
        # Call the GameBase constructor.
        super().__init__()

        # Load our textures.
        texturePlayer = Texture( "Data/Textures/player.png" )
        textureEnemy = Texture( "Data/Textures/enemy.png" )

        # Add some game objects to our dictionary.
        self.gameObjects.append( Player( vec2( 10, 7.5 ), self.sprite, texturePlayer ) )
        self.gameObjects.append( GameObject( vec2( 10, 2 ), self.sprite, textureEnemy ) )

    def onEvent(self, event):
        # Base game class will pass events to all gameobjects in list.
        super().onEvent( event )

    def update(self, deltaTime):
        # Base game class will update all gameobjects in list.
        super().update( deltaTime )

    def draw(self):
        # Base game class will draw all game objects.
        super().draw()
