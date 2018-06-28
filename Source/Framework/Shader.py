import OpenGL.GL as gl

from Framework.Vector import vec2

class Shader:
    def __init__(self, vertexShaderFilename, fragmentShaderFilename):
        # Load the .vert and .frag files from disk.
        vertexShaderFile = open( vertexShaderFilename, "r" )
        fragmentShaderFile = open( fragmentShaderFilename, "r" )

        vertexShaderStrings = vertexShaderFile.read()
        fragmentShaderStrings = fragmentShaderFile.read()

        # Create the 2 shaders and the shader program.
        self.vertexShader = gl.glCreateShader( gl.GL_VERTEX_SHADER )
        self.fragmentShader = gl.glCreateShader( gl.GL_FRAGMENT_SHADER )
        self.shaderProgram = gl.glCreateProgram()

        # Setup the compile the vert and frag shaders.
        gl.glShaderSource( self.vertexShader, vertexShaderStrings )
        gl.glShaderSource( self.fragmentShader, fragmentShaderStrings )

        gl.glCompileShader( self.vertexShader )
        gl.glCompileShader( self.fragmentShader )
        
        # Error checking, should warn us if either shader had syntax errors.
        if gl.glGetShaderiv( self.vertexShader, gl.GL_COMPILE_STATUS ) != gl.GL_TRUE:
            raise RuntimeError( gl.glGetShaderInfoLog( self.vertexShader ).decode() )
        
        if gl.glGetShaderiv( self.fragmentShader, gl.GL_COMPILE_STATUS ) != gl.GL_TRUE:
            raise RuntimeError( gl.glGetShaderInfoLog( self.fragmentShader ).decode() )

        # Attach and link the 2 shaders to build the final shader program.
        gl.glAttachShader( self.shaderProgram, self.vertexShader )
        gl.glAttachShader( self.shaderProgram, self.fragmentShader )
        gl.glLinkProgram( self.shaderProgram )

        # More error checking, should warn us if the link process had issues.
        if gl.glGetProgramiv( self.shaderProgram, gl.GL_LINK_STATUS ) != gl.GL_TRUE:
            raise RuntimeError( gl.glGetProgramInfoLog( self.shaderProgram ).decode() )

        # Get the locations of various attributes and uniforms from the shader program.
        self.attributeLocation_Position = gl.glGetAttribLocation( self.shaderProgram, "a_Position" )
        self.attributeLocation_UV = gl.glGetAttribLocation( self.shaderProgram, "a_UV" )

        self.uniformLocation_ObjectPosition = gl.glGetUniformLocation( self.shaderProgram, "u_ObjectPosition" )
        self.uniformLocation_ObjectScale = gl.glGetUniformLocation( self.shaderProgram, "u_ObjectScale" )
        self.uniformLocation_UVScale = gl.glGetUniformLocation( self.shaderProgram, "u_UVScale" )
        self.uniformLocation_UVOffset = gl.glGetUniformLocation( self.shaderProgram, "u_UVOffset" )
        self.uniformLocation_TextureDiffuse = gl.glGetUniformLocation( self.shaderProgram, "u_TextureDiffuse" )
        self.uniformLocation_TextureOther = gl.glGetUniformLocation( self.shaderProgram, "u_TextureOther" )
        self.uniformLocation_Time = gl.glGetUniformLocation( self.shaderProgram, "u_Time" )
        self.uniformLocation_Percentage = gl.glGetUniformLocation( self.shaderProgram, "u_Percentage" )

        self.currentScale = vec2( 0, 0 )
        self.currentUVScale = vec2( 0, 0 )
        self.currentUVOffset = vec2( 0, 0 )
        self.currentTextureDiffuse = -1
        self.currentTextureOther = -1
        self.currentTime = 0
        self.currentPercentage = 0

    def setUniformPosition(self, position):
        gl.glUniform2f( self.uniformLocation_ObjectPosition, position.x, position.y )

    def setUniformScale(self, scale):
        if self.currentScale != scale:
            self.currentScale = scale
            gl.glUniform2f( self.uniformLocation_ObjectScale, scale.x, scale.y )
       
    def setUniformUVScale(self, scale):
        if self.currentUVScale != scale:
            self.currentUVScale = scale
            gl.glUniform2f( self.uniformLocation_UVScale, scale.x, scale.y )

    def setUniformUVOffset(self, offset):
        if self.currentUVOffset != offset:
            self.currentUVOffset = offset
            gl.glUniform2f( self.uniformLocation_UVOffset, offset.x, offset.y )

    def setUniformTextureDiffuse(self, texture):
        if self.currentTextureDiffuse != texture:
            self.currentTextureDiffuse = texture
            gl.glActiveTexture( gl.GL_TEXTURE12 )
            gl.glBindTexture( gl.GL_TEXTURE_2D, texture )
            gl.glUniform1i( self.uniformLocation_TextureDiffuse, 12 )

    def setUniformTextureOther(self, texture):
        if self.currentTextureOther != texture:
            self.currentTextureOther = texture
            gl.glActiveTexture( gl.GL_TEXTURE13 )
            gl.glBindTexture( gl.GL_TEXTURE_2D, texture )
            gl.glUniform1i( self.uniformLocation_TextureOther, 13 )

    def setUniformTime(self, time):
        if self.currentTime != time:
            self.currentTime = time
            gl.glUniform1f( self.uniformLocation_Time, time )

    def setUniformPercentage(self, percentage):
        if self.currentPercentage != percentage:
            self.currentPercentage = percentage
            gl.glUniform1f( self.uniformLocation_Percentage, percentage )
