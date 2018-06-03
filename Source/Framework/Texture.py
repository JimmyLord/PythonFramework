import OpenGL.GL as gl
import pygame

from Framework.Vector import vec2

class Texture:
    def __init__(self, filename = None, bottomLeftPixel = (-1,-1), tileSize = (-1,-1), textureToCopy = None):
        # If a filename was passed in, load the texture from disk.
        # If no filename was passed in, make sure 'textureToCopy' isn't None and use that texture's info.

        if filename != None:
            # Ask pygame to load the image.
            textureSurface = pygame.image.load( filename )
            textureData = pygame.image.tostring( textureSurface, "RGBA", 1 )

            self.width = textureSurface.get_width()
            self.height = textureSurface.get_height()

            # Create an OpenGL texture with the image pygame loaded.
            self.textureHandle = gl.glGenTextures( 1 )
            gl.glBindTexture( gl.GL_TEXTURE_2D, self.textureHandle )
            gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST )
            gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST )
            gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, textureData )
        else:
            # A filename wasn't passed in, so copy an existing textureHandle
            assert textureToCopy != None
            self.textureHandle = textureToCopy.textureHandle

            self.width = textureToCopy.width
            self.height = textureToCopy.height

        # Determine the UV scale and offset of the tile we want.
        if bottomLeftPixel[0] == -1:
            self.UVScale = vec2( 1, 1 )
            self.UVOffset = vec2( 0, 0 )
        else:
            self.UVScale = vec2( tileSize[0]/self.width, tileSize[1]/self.height )
            self.UVOffset = vec2( bottomLeftPixel[0]/self.width, bottomLeftPixel[1]/self.height )
