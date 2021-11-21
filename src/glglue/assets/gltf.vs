in vec3 aPosition;

#ifdef HAS_UV
in vec2 aUV;
out vec2 vUV;
#endif

uniform mediump mat4 m;
uniform mediump mat4 vp;

void main() {
  gl_Position = vec4(aPosition, 1) * m * vp;
#ifdef HAS_UV
  vUV = aUV;
#endif
}
