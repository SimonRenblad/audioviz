#version 330 core

in vec2 fragCoord;
out vec4 fragColor;

uniform float bars[512];

void rgb_to_norm(in float r, in float g, in float b, out vec3 color) {
    color = vec3(r / 256.0, g / 256.0, b / 256.0);
}

void main() {
    vec3 cool_color = vec3(0.0, 0.0, 0.0);
    rgb_to_norm(32.0, 194.0, 14.0, cool_color);
    vec4 bgcolor = vec4(0.0, 0.0, 0.0, 1.0);
    vec4 fgcolor = vec4(cool_color, 1.0);
    // divide into sections of 1.0 / 512.0
    int bar = int(fragCoord.x * 128);
    float y_val = bars[bar];
    if (y_val == 0.0) {
        fragColor = bgcolor;
    } else {
        if (fragCoord.y < y_val) {
            // we interp the alpha
            float diff = smoothstep(0.0, y_val, fragCoord.y);
            fragColor = vec4(cool_color, diff);
        } else {
            fragColor = bgcolor;
        }
    }
}
