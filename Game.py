import pygame
import OpenGL.GL as gl

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework import Shader
from Framework import Sprite
from Framework import Texture

import GameObject
import Player

class Game:
    def __init__(self):
        # Load a single shader and create a single sprite for all of our objects.
        shader = Shader.Shader( "Data/Shaders/texture.vert", "Data/Shaders/texture.frag" )
        sprite = Sprite.Sprite( shader )

        # Load our textures.
        texturePlayer = Texture.Texture( "Data/Textures/player.png" )
        textureEnemy = Texture.Texture( "Data/Textures/enemy.png" )

        # Create a dictionary of game objects to allow easy access by name.
        self._gameObjects = {}
        self._gameObjects['Player'] = Player.Player( [10, 7.5], sprite, texturePlayer )
        self._gameObjects['Enemy'] = GameObject.GameObject( [10, 2], sprite, textureEnemy )

    def onEvent(self, event):
        # Pass all events on to all game objects.
        for key, object in self._gameObjects.items():
            object.onEvent( event )

    def update(self, deltaTime):
        # Update all game objects.
        for key, object in self._gameObjects.items():
            object.update( deltaTime )

    def draw(self):
        # Draw all game objects.
        for key, object in self._gameObjects.items():
            object.draw()
