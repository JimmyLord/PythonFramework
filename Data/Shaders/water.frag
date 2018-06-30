
varying vec2 v_UV;

uniform sampler2D u_TextureDiffuse;

void main()
{
    gl_FragColor = texture2D( u_TextureDiffuse, v_UV ) + vec4( 40.0/255.0, 155/255.0f, 230/255.0f, 0 );
}
