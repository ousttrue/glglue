#version 330
in vec3 aPos;
in vec3 aColor;
out vec3 vColor;
uniform mediump mat4 uView;
uniform mediump mat4 uProjection;
uniform mediump mat4 uModel;

void main() {
  gl_Position = uProjection * uView * uModel * vec4(aPos, 1);
  vColor = aColor;
}
