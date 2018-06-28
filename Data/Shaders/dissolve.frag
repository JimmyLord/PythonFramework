
varying vec2 v_UV;

uniform sampler2D u_TextureDiffuse;
uniform sampler2D u_TextureOther;
uniform float u_Percentage;

void main()
{
    vec4 color = texture2D( u_TextureDiffuse, v_UV );
    vec4 dissolve = texture2D( u_TextureOther, v_UV );

    float dissolveAmount = (1 - u_Percentage) + dissolve.r * 0.9;
    if( dissolveAmount < 0.95 )
    {
        discard;
    }
    else if( dissolveAmount < 1.0 )
    {
        gl_FragColor.rgb = vec3( 1, 0, 0 );
    }
    else
    {
        gl_FragColor = color;
    }
}
