#version 330
in vec2 v_uv;
in vec3 v_color;
out vec4 FragColor;
uniform sampler2D u_texture;

void main()
{
    vec4 texel = texture(u_texture, v_uv);
    // FragColor = vec4(v_color * texel.xyz, 1);
    FragColor = texel;
    FragColor.xyz += 0.0001 * v_color;
    // FragColor = vec4(v_uv, 1, 1);
}