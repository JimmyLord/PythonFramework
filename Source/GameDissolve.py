import pygame
import OpenGL.GL as gl

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework.Vector import vec2
from Framework.Shader import Shader
from Framework.Sprite import Sprite
from Framework.WaterMesh import WaterMesh
from Framework.Texture import Texture

from GameBase import GameBase
from GameObject import GameObject
from Tilemap import Tilemap
from PlayerTilemapLocked import PlayerTilemapLocked
from PlayerTilemapFree import PlayerTilemapFree

class GameDissolve(GameBase):
    def __init__(self):
        # Call the GameBase constructor.
        super().__init__()

        self.shader = Shader( "Data/Shaders/dissolve.vert", "Data/Shaders/dissolve.frag" )
        self.mesh = Sprite( self.shader )
        self.textureBase = Texture( filename="Data/Textures/player.png" )
        self.textureDissolve = Texture( filename="Data/Textures/clouds.png" )
        self.totalTimeElapsed = 0
        self.dissolvePercentage = 0

    def onEvent(self, event):
        # Base game class will pass events to all gameobjects in list.
        super().onEvent( event )

    def update(self, deltaTime):
        # Base game class will update all gameobjects in list.
        super().update( deltaTime )
        self.totalTimeElapsed += deltaTime

        # Debug info displayed using imgui.
        imgui.begin( "Dissolve", True )
        changed, self.dissolvePercentage = imgui.slider_float( "Percentage", self.dissolvePercentage, 0, 1 )
        imgui.end()

    def draw(self):
        # Base game class will draw all game objects.
        super().draw()

        self.mesh.drawSetup()
        self.mesh.draw( vec2(10, 7.5), vec2(10,3), self.textureBase, self.totalTimeElapsed, self.dissolvePercentage, self.textureDissolve )
        self.mesh.drawCleanup()
