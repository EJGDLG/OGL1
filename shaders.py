skybox_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 inPosition;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 texCoords;

void main()
{
    texCoords = inPosition;
    gl_Position = projectionMatrix * viewMatrix * vec4(inPosition, 1.0);
}

'''

skybox_fragment_shader = '''
#version 450 core

uniform samplerCube skybox;

in vec3 texCoords;

out vec4 fragColor;

void main()
{
    fragColor = texture(skybox, texCoords);
}

'''
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

distortion_shader = """
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
  outPosition = modelMatrix * vec4(position + normals * sin(time) /10, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * outPosition;
  outTextCoords =  textCoords;
  outNormals = normals;
}
"""



water_shader = """
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
  outPosition = modelMatrix * vec4(position + vec3(0,1,0) * sin(time * position.x *10) /10, 1.0);
  gl_Position = proyectionMatrix * viewMatrix * outPosition;
  outTextCoords =  textCoords;
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

negative_shader = """
#version 450 core
in vec2 outTextCoords;
in vec3 outNormals;


out vec4 fragColor;
uniform sampler2D tex;
void main()
{
  fragColor = 1 - texture(tex, outTextCoords);
}
"""