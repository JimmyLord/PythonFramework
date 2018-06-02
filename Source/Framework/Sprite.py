import OpenGL.GL as gl
import ctypes

class Sprite:
    def __init__(self, shader):
        # Store the shader object as a member.
        self.shader = shader

        # Define the sprite vertices.
        vertices = [ -0.5, -0.5,  0, 0,   # bottom left
                     -0.5,  0.5,  0, 1,   # top left
                      0.5, -0.5,  1, 0,   # bottom right
                      0.5,  0.5,  1, 1, ] # top right

        # Copy the vertex info into a VBO.
        self.VBO = gl.glGenBuffers( 1 )
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.VBO )
        gl.glBufferData( gl.GL_ARRAY_BUFFER, len(vertices)*4, (ctypes.c_float*len(vertices))(*vertices), gl.GL_STATIC_DRAW )
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )

    def drawSetup(self):
        # Enable our shader.
        gl.glUseProgram( self.shader.shaderProgram )

        # Enable blending.
        gl.glEnable( gl.GL_BLEND )
        gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )

        # Setup attributes.
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.VBO )
        
        gl.glVertexAttribPointer( self.shader.attributeLocation_Position, 2, gl.GL_FLOAT, False, 16, ctypes.c_void_p( 0 ) )
        gl.glEnableVertexAttribArray( self.shader.attributeLocation_Position )
        
        if self.shader.attributeLocation_UV != -1:
            gl.glVertexAttribPointer( self.shader.attributeLocation_UV, 2, gl.GL_FLOAT, False, 16, ctypes.c_void_p( 8 ) )
            gl.glEnableVertexAttribArray( self.shader.attributeLocation_UV )

    def drawCleanup(self):
        # Unset everything, mainly to allow imgui to draw.
        gl.glActiveTexture( gl.GL_TEXTURE0 )
        gl.glDisableVertexAttribArray( self.shader.attributeLocation_Position )
        if self.shader.attributeLocation_UV != -1:
            gl.glDisableVertexAttribArray( self.shader.attributeLocation_UV )
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )
        gl.glUseProgram( 0 )

    def draw(self, position, scale, texture):
        # Setup for draw.
        # Moved to Main.py since this stuff doesn't change between sprites.
        # Now only done once per frame, which should work as long as we only have 1 shader and sprite.
        # drawSetup()

        # Setup uniforms.
        self.shader.setUniformPosition( position )
        self.shader.setUniformScale( scale )
        self.shader.setUniformUVScale( texture.UVScale )
        self.shader.setUniformUVOffset( texture.UVOffset )
        self.shader.setUniformTextureDiffuse( texture.textureHandle )

        # Draw the sprite.
        gl.glDrawArrays( gl.GL_TRIANGLE_STRIP, 0, 4 )

        # Cleanup the GL state after drawing.
        # Moved to Main.py since this stuff doesn't change between sprites.
        # Now only done once per frame, which should work as long as we only have 1 shader and sprite.
        # drawCleanup()