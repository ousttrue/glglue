#version 330
in vec3 vPosition;
in vec3 vNormal;
out vec4 fColor;
uniform vec4 light;

vec3 light_vector(vec3 p)
{
    if (light.w == 0)
    {
        // dir
        return normalize(-light.xyz);
    }
    else
    {
        // positon
        return normalize(vec3(light) - p);
    }
}

float lambert(vec3 n, vec3 p)
{
    vec3 s = light_vector(p);
    return max(dot(s, n), 0);
}

void main()
{
    float d = lambert(normalize(vNormal), vPosition);
    fColor = vec4(d, d, d, 1);
}
