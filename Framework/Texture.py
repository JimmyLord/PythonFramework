import OpenGL.GL as gl
import pygame

class Texture:
    def __init__(self, filename):
        # Ask pygame to load the image.
        textureSurface = pygame.image.load( filename )
        textureData = pygame.image.tostring( textureSurface, "RGBA", 1 )

        width = textureSurface.get_width()
        height = textureSurface.get_height()

        # Create an OpenGL texture with the image pygame loaded.
        self.textureHandle = gl.glGenTextures( 1 )
        gl.glBindTexture( gl.GL_TEXTURE_2D, self.textureHandle )
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST )
        gl.glTexParameteri( gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST )
        gl.glTexImage2D( gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, textureData )
