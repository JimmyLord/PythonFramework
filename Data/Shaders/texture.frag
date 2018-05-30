
varying vec2 v_UV;

uniform sampler2D u_TextureDiffuse;

void main()
{
    gl_FragColor = texture2D( u_TextureDiffuse, v_UV );
}
