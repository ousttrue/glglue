#version 330
in vec3 a_pos;
in vec3 a_normal;
in vec3 a_color;
out vec3 v_color;
uniform mediump mat4 u_view;
uniform mediump mat4 u_projection;
uniform mediump mat4 u_model;

void main() {
  // gl_Position = vec4(aPos, 1) * uView * uProjection;
  gl_Position = u_projection * u_view * u_model * vec4(a_pos, 1);
  
  // lambert
  vec3 L = normalize(vec3(-1, - 2, - 3));
  vec3 N = normalize(a_normal);
  float v = max(dot(N, L), 0.2);
  v_color = a_color * v;
}
