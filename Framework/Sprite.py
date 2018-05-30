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

    def draw(self, position, scale, texture):
        # Enable our shader.
        gl.glUseProgram( self.shader.shaderProgram )

        # Setup attributes.
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, self.VBO )
        
        gl.glVertexAttribPointer( self.shader.attributeLocation_Position, 2, gl.GL_FLOAT, False, 16, ctypes.c_void_p( 0 ) )
        gl.glEnableVertexAttribArray( self.shader.attributeLocation_Position )
        
        if self.shader.attributeLocation_UV != -1:
            gl.glVertexAttribPointer( self.shader.attributeLocation_UV, 2, gl.GL_FLOAT, False, 16, ctypes.c_void_p( 8 ) )
            gl.glEnableVertexAttribArray( self.shader.attributeLocation_UV )

        # Setup uniforms.
        gl.glUniform2f( self.shader.uniformLocation_ObjectScale, scale[0], scale[1] )
        gl.glUniform2f( self.shader.uniformLocation_ObjectPosition, position[0], position[1] )

        # Setup texture unit.
        gl.glActiveTexture( gl.GL_TEXTURE0 )
        gl.glBindTexture( gl.GL_TEXTURE_2D, texture.textureHandle )
        gl.glUniform1i( self.shader.uniformLocation_TextureDiffuse, 0 )

        # Draw the sprite.
        gl.glDrawArrays( gl.GL_TRIANGLE_STRIP, 0, 4 )

        # Unset everything, mainly to allow imgui to draw.
        gl.glBindTexture( gl.GL_TEXTURE_2D, 0 )
        gl.glDisableVertexAttribArray( self.shader.attributeLocation_Position )
        if self.shader.attributeLocation_UV != -1:
            gl.glDisableVertexAttribArray( self.shader.attributeLocation_UV )
        gl.glBindBuffer( gl.GL_ARRAY_BUFFER, 0 )
        gl.glUseProgram( 0 )
