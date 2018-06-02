import pygame
import OpenGL.GL as gl

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework import Shader
from Framework import Sprite
from Framework import Texture

import GameObject
import Player

class GameBase:
    def __init__(self):
        # Load a single shader and create a single sprite for all of our objects.
        self.shader = Shader.Shader( "Data/Shaders/texture.vert", "Data/Shaders/texture.frag" )
        self.sprite = Sprite.Sprite( self.shader )

        # Create a dictionary of game objects to allow easy access by name.
        self.gameObjects = []

    def onEvent(self, event):
        # Pass all events on to all game objects.
        for object in self.gameObjects:
            object.onEvent( event )

    def update(self, deltaTime):
        # Update all game objects.
        for object in self.gameObjects:
            object.update( deltaTime )

    def draw(self):
        # Draw all game objects.
        for object in self.gameObjects:
            object.draw()
