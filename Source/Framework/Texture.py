import OpenGL.GL as gl
import pygame

class Texture:
    def __init__(self, filename, bottomLeftPixel = (-1,-1), tileSize = (-1,-1)):
        # Ask pygame to load the image.
        textureSurface = pygame.image.load( filename )
        textureData = pygame.image.tostring( textureSurface, "RGBA", 1 )

        width = textureSurface.get_width()
        height = textureSurface.get_height()

        # Determine the UV scale and offset of the tile we want.
        if bottomLeftPixel[0] == -1:
            self.UVScale = (1,1)
            self.UVOffset = (0,0)
        else:
            self.UVScale = ( tileSize[0]/width, tileSize[1]/height )
            self.UVOffset = ( bottomLeftPixel[0]/width, bottomLeftPixel[1]/height )

        # Create an OpenGL texture with the image pygame loaded.
        self.textureHandle = gl.glGenTextures( 1 )
        gl.glBindTexture( gl.GL_TEXTURE_2D, self.textureHandle )
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST )
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST )
        gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, textureData )
