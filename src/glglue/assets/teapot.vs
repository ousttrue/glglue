#version 330
in vec3 aPosition;
in vec3 aNormal;
out vec3 vPosition;
out vec3 vNormal;
uniform mediump mat4 m;
uniform mediump mat4 v;
uniform mediump mat4 p;

void main() {
  vNormal = normalize((vec4(aNormal, 0) * m).xyz);
  vPosition = (vec4(aPosition, 1) * m * v).xyz;
  gl_Position = vec4(aPosition, 1) * m * v * p;
}
