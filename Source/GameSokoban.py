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
from Tilemap import Tilemap
from PlayerTilemapLocked import PlayerTilemapLocked
from PlayerTilemapFree import PlayerTilemapFree

class GameSokoban(GameBase):
    def __init__(self):
        # Call the GameBase constructor.
        super().__init__()

        # Load our textures.
        # The Sokoban tilesheet is 13x8 tiles, each is 64x64 pixels.
        tilew = 64
        tileh = 64
        self.TextureTiles = Texture( filename="Data/Textures/sokoban_tilesheet.png" )
        self.playerAnimations = [
            # Up (3 frames)
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 3*tilew, 2*tileh), tileSize=(tilew,tileh) ),
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 4*tilew, 2*tileh), tileSize=(tilew,tileh) ),
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 5*tilew, 2*tileh), tileSize=(tilew,tileh) ),
            # Down (3 frames)
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 0*tilew, 2*tileh), tileSize=(tilew,tileh) ),
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 1*tilew, 2*tileh), tileSize=(tilew,tileh) ),
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 2*tilew, 2*tileh), tileSize=(tilew,tileh) ),
            # Left (3 frames)
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 3*tilew, 0*tileh), tileSize=(tilew,tileh) ),
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 4*tilew, 0*tileh), tileSize=(tilew,tileh) ),
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 5*tilew, 0*tileh), tileSize=(tilew,tileh) ),
            # Right (3 frames)
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 0*tilew, 0*tileh), tileSize=(tilew,tileh) ),
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 1*tilew, 0*tileh), tileSize=(tilew,tileh) ),
            Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 2*tilew, 0*tileh), tileSize=(tilew,tileh) ),
        ]
        self.textureBox =           Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 1*tilew, 7*tileh), tileSize=(tilew,tileh) )
        self.textureTileFloor =     Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=(11*tilew, 1*tileh), tileSize=(tilew,tileh) )
        self.textureTileGoal =      Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=(11*tilew, 0*tileh), tileSize=(tilew,tileh) )
        self.textureTileWall =      Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 6*tilew, 0*tileh), tileSize=(tilew,tileh) )
        self.textureTileBox =       Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 6*tilew, 7*tileh), tileSize=(tilew,tileh) )
        self.textureTileBoxOnGoal = Texture( textureToCopy=self.TextureTiles, bottomLeftPixel=( 6*tilew, 6*tileh), tileSize=(tilew,tileh) )

        # Our game/screen is setup as follows:
        # Screen resolution: 800 x 600
        # World area in camera view: 0,0 to 20,15
        tileSize = vec2( 1, 1 )
        tilemapSize = vec2( 9, 7 )
        tilemapPosition = vec2( 10 - tilemapSize.x/tileSize.x/2, 7.5 - tilemapSize.y/tileSize.y/2 )

        # Add some game objects to our gameObject list.
        self.tilemap = Tilemap( self, tilemapPosition, tilemapSize, tileSize )
        self.gameObjects.append( self.tilemap )
        # self.gameObjects.append( PlayerTilemapFree( vec2( 1, 1 ), self.sprite, self.playerAnimations, self.tilemap ) )
        self.gameObjects.append( PlayerTilemapLocked( vec2( 1, 1 ), self.sprite, self.playerAnimations, self.tilemap ) )

    def onEvent(self, event):
        # Base game class will pass events to all gameobjects in list.
        super().onEvent( event )

    def update(self, deltaTime):
        # Base game class will update all gameobjects in list.
        super().update( deltaTime )

        # Debug info displayed using imgui.
        imgui.begin( "Sokoban", True )
        imgui.text( "Solved: " + str(self.tilemap.solved) )
        imgui.end()

    def draw(self):
        # Base game class will draw all game objects.
        super().draw()
