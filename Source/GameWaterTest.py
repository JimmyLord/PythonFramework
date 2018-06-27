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

class GameWaterTest(GameBase):
    def __init__(self):
        # Call the GameBase constructor.
        super().__init__()

        self.waterShader = Shader( "Data/Shaders/water.vert", "Data/Shaders/water.frag" )
        self.waterMesh = WaterMesh( self.waterShader )
        self.waterTexture = Texture( filename="Data/Textures/player.png" )
        self.totalTimeElapsed = 0

    def onEvent(self, event):
        # Base game class will pass events to all gameobjects in list.
        super().onEvent( event )

    def update(self, deltaTime):
        # Base game class will update all gameobjects in list.
        super().update( deltaTime )
        self.totalTimeElapsed += deltaTime

        # Debug info displayed using imgui.
        # imgui.begin( "Sokoban", True )
        # imgui.text( "Solved: " + str(self.tilemap.solved) )
        # imgui.end()

    def draw(self):
        # Base game class will draw all game objects.
        super().draw()

        self.waterMesh.drawSetup()
        self.waterMesh.draw( vec2(10, 7.5), vec2(10,3), self.waterTexture, self.totalTimeElapsed )
        self.waterMesh.drawCleanup()
