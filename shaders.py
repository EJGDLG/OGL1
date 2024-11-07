vertex_shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;
void main()
{ 
  outPosition = modelMatrix * vec4(position, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * outPosition;
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""

Wobble_Shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    float wobble = sin(time * 5.0 + position.y * 10.0) / 10.0;
    outPosition = modelMatrix * vec4(position + wobble * normals, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}
"""

Twist_Shader = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    float angle = position.y * 0.5 + time * 0.5;
    mat4 twistMatrix = mat4(
        cos(angle), 0.0, -sin(angle), 0.0,
        0.0, 1.0, 0.0, 0.0,
        sin(angle), 0.0, cos(angle), 0.0,
        0.0, 0.0, 0.0, 1.0
    );
    outPosition = modelMatrix * twistMatrix * vec4(position, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}

"""

fragmet_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
in vec4 outPosition;

out vec4 fragColor;
uniform sampler2D tex;
uniform vec3 pointLight;
void main()
{
  float intensity = dot(outNormals, normalize(pointLight - outPosition.xyz));
  fragColor = texture(tex, outTextCoords) * intensity;
}
"""

Ripple_Shader  = """
#version 450 core
layout(location=0) in vec3 position;
layout(location=1) in vec2 textCoords;
layout(location=2) in vec3 normals;
out vec2 outTextCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform mat4 modelMatrix;
uniform float time;
uniform mat4 viewMatrix;
uniform mat4 proyectionMatrix;

void main()
{
    float distance = length(position.xz);
    float offset = sin(distance * 10.0 - time * 5.0) / 20.0;
    outPosition = modelMatrix * vec4(position + offset * normals, 1.0);
    gl_Position = proyectionMatrix * viewMatrix * outPosition;
    outTextCoords = textCoords;
    outNormals = normals;
}

"""
Glow_Shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;
in vec4 outPosition;

out vec4 fragColor;
uniform sampler2D tex;
uniform vec3 pointLight;

void main()
{
    float intensity = dot(outNormals, normalize(pointLight - outPosition.xyz));
    intensity = pow(intensity, 2.0); // Ajuste para darle más suavidad
    fragColor = texture(tex, outTextCoords) * vec4(1.0, 1.0, 1.0, 1.0) * intensity * 1.5;
}
"""

Sepia_Shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;

out vec4 fragColor;
uniform sampler2D tex;

void main()
{
    vec4 color = texture(tex, outTextCoords);
    float gray = dot(color.rgb, vec3(0.3, 0.59, 0.11)); // Escala de grises
    fragColor = vec4(gray * vec3(1.2, 1.0, 0.8), color.a); // Aplicar tono sepia
}

"""