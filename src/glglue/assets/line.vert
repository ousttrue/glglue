#version 330
in vec3 a_pos;
in vec3 a_color;
out vec3 v_color;
uniform mediump mat4 u_view;
uniform mediump mat4 u_projection;
uniform mediump mat4 u_model;

void main() {
  gl_Position = u_projection * u_view * u_model * vec4(a_pos, 1);
  v_color = a_color;
}
