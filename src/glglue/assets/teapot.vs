#version 330
in vec3 aPosition;
in vec3 aNormalr;
uniform mediump mat4 m;
uniform mediump mat4 vp;

void main() {
  gl_Position = vec4(aPosition, 1) * m * vp;
}
