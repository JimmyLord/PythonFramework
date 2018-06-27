import OpenGL.GL as gl
import ctypes

class WaterMesh:
    def __init__(self, shader):
        # Store the shader object as a member.
        self.shader = shader

        # Define the water vertices. Set up as a Triangle Fan.
        self.numberOfVertices = 100 + 2
        vertices = []
        
        vertices.extend( [ -0.5, -0.5,  0.0, 0.0 ] ) # bottom left
        for x in range(0,self.numberOfVertices - 2):
            vertices.extend( [ -0.5 + (1.0 * x/(self.numberOfVertices - 3)), 0.5,  x/(self.numberOfVertices - 3), 1.0 ] )
        vertices.extend( [ 0.5, -0.5,  1.0, 0.0 ] ) # bottom right

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

    def draw(self, position, scale, texture, time):
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
        self.shader.setUniformTime( time )

        # Draw the sprite.
        gl.glDrawArrays( gl.GL_TRIANGLE_FAN, 0, self.numberOfVertices )

        # Cleanup the GL state after drawing.
        # Moved to Main.py since this stuff doesn't change between sprites.
        # Now only done once per frame, which should work as long as we only have 1 shader and sprite.
        # drawCleanup()