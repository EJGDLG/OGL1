import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from camera import Camera
from Skybox import Skybox
class Renderer(object):
  def __init__(self, screen):
    self.screen = screen
    _,_, self.width, self.height = screen.get_rect()

    glClearColor(0.2,0.2,0.2,1.0)

  
    glEnable(GL_DEPTH_TEST)
    glViewport(0,0, self.width, self.height)

    self.time = 0
    self.value = 0
    self.skybox = None
    self.pointLight = glm.vec3(0,0,0)

    self.camera = Camera(width=self.width, height=self.height)
    self.scene = []
    self.active_shaders = None

  def CreateSkybox(self, textureLIst, vShader, fShader):
    self.skybox = Skybox(textureList=textureLIst, vertexShader=vShader, fragmentShader=fShader)


  def FillMode(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
  
  def WireFrameMode(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


  def SetShaders(self, vShader, fShader):
    if vShader is not None and fShader is not None:
      self.active_shaders = compileProgram(compileShader(vShader, GL_VERTEX_SHADER),
                                           compileShader(fShader, GL_FRAGMENT_SHADER))
    else:
      self.active_shaders = None

  
  def Render(self):

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if self.skybox is not None:
      self.skybox.Render(viewMatrix=self.camera.GetViewMaTrix(),
                         projectionMatrix=self.camera.GetProjectionMatrix())
    if self.active_shaders is not None:
      glUseProgram(self.active_shaders)
      glUniform1f( glGetUniformLocation(self.active_shaders, "time"), self.time)
      glUniform3fv( glGetUniformLocation(self.active_shaders, "pointLight"), 
                   1,
                   glm.value_ptr(self.pointLight) )
      
      glUniformMatrix4fv( glGetUniformLocation(self.active_shaders, 
                                                  "viewMatrix"), 
                                                  1, 
                                                  GL_FALSE, 
                                                  glm.value_ptr(self.camera.GetViewMaTrix()))
      glUniformMatrix4fv( glGetUniformLocation(self.active_shaders, 
                                                  "proyectionMatrix"), 
                                                  1, 
                                                  GL_FALSE, 
                                                  glm.value_ptr(self.camera.GetProjectionMatrix()))

    for obj in self.scene:
      if self.active_shaders is not None:
         glUniformMatrix4fv( glGetUniformLocation(self.active_shaders, 
                                                  "modelMatrix"), 
                                                  1, 
                                                  GL_FALSE, 
                                                  glm.value_ptr(obj.GetModelMatrix()))
         
      obj.Render()
    

    