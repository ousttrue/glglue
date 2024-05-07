#version 330
in vec3 aPos;
in vec3 aNormal;
in vec3 aColor;
out vec3 vColor;
uniform mediump mat4 uView;
uniform mediump mat4 uProjection;

void main() {
  // gl_Position = vec4(aPos, 1) * uView * uProjection;
  gl_Position = uProjection * uView * vec4(aPos, 1);

  // lambert
  vec3 L = normalize(vec3(-1, -2, -3));
  vec3 N = normalize(aNormal);
  float v = max(dot(N, L), 0.2);
  vColor = aColor * v;
}
