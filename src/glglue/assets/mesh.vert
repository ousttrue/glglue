#version 330
in vec3 a_pos;
in vec3 a_normal;
in vec2 a_uv;
out vec2 v_uv;
out vec3 v_color;
uniform mediump mat4 u_view;
uniform mediump mat4 u_projection;
uniform mediump mat4 u_model;

void main()
{
    gl_Position =
        u_projection * u_view * u_model * vec4(a_pos.x, a_pos.y, a_pos.z, 1);
    v_uv = a_uv;

    // lambert
    vec3 L = normalize(vec3(-1, -2, 3));
    vec3 N = normalize(a_normal);
    float v = max(dot(N, L), 0.2);
    v_color = vec3(v, v, v);
}