#ifdef HAS_UV
in vec2 vUV;
#else
vec2 vUV = vec2(1, 1);
#endif

uniform sampler2D COLOR_TEXTURE;

out vec4 fColor;
void main() {
  vec4 tex = texture(COLOR_TEXTURE, vUV);
  fColor = tex;
}
