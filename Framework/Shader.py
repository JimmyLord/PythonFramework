import OpenGL.GL as gl

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
        self.uniformLocation_TextureDiffuse = gl.glGetUniformLocation( self.shaderProgram, "u_TextureDiffuse" )
