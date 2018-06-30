attribute vec2 a_Position;
attribute vec2 a_UV;

uniform vec2 u_ObjectPosition;
uniform vec2 u_ObjectScale;

uniform vec2 u_UVScale;
uniform vec2 u_UVOffset;

uniform float u_Time;

varying vec2 v_UV;

void main()
{
    vec2 u_CameraPosition = vec2( 0, 0 );
    vec2 u_ProjectionOffset = vec2( 10, 7.5 );
    vec2 u_ProjectionScale = vec2( 10, 7.5 );

    vec2 worldSpacePosition = a_Position * u_ObjectScale + u_ObjectPosition;

    worldSpacePosition.y += sin( u_Time + worldSpacePosition.x ) * 0.2;

    vec2 viewSpacePosition = worldSpacePosition - u_CameraPosition;
    vec2 clipSpacePosition = (viewSpacePosition - u_ProjectionOffset) / u_ProjectionScale;

    gl_Position = vec4( clipSpacePosition, 0, 1 );

    v_UV = a_UV * u_UVScale + u_UVOffset;

    v_UV.x += u_Time * 0.02 + sin( u_Time ) * 0.004;
    v_UV.y += sin( u_Time ) * 0.02;
}