#version 330 core
#define PI 3.1415926538

in vec2 fragCoord;
out vec4 fragColor;

uniform float bars[512];

void rgb_to_norm(in float r, in float g, in float b, out vec3 color) {
    color = vec3(r / 256.0, g / 256.0, b / 256.0);
}

float atan2(in float y, in float x)
{
    bool s = (abs(x) > abs(y));
    return mix(PI/2.0 - atan(x,y), atan(y,x), s);
}

void main() {
    vec3 cool_color = vec3(0.0, 0.0, 0.0);
    rgb_to_norm(255.0, 191.0, 0.0, cool_color);
    vec4 bgcolor = vec4(0.0, 0.0, 0.0, 1.0);
    vec4 fgcolor = vec4(cool_color, 1.0);

    // 0.5, 0.5 is the origin so reorient to
    vec2 newCoords = (fragCoord.xy * 2) - vec2(1.0, 1.0);

    float d = length(newCoords);
    if (d < 0.20) {
        fragColor = fgcolor;
    } else {
        float angle = atan2(newCoords.x, newCoords.y);
        int bar = int(smoothstep(-PI, PI, angle + PI/4) * 128);
        float y_val = bars[bar];
        float depth_norm = smoothstep(0.2, (2*y_val)+0.2, d);
        fragColor = mix(fgcolor, bgcolor, depth_norm);
    }
}
