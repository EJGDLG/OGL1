import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model


width = 960
height = 540

pygame.init()


# Double buffering 
screen = pygame.display.set_mode((width,height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen=screen)

renderer.SetShaders(vShader=vertex_shader, fShader=fragmet_shader)



skyboxTextures = ['Textures\Skybox_Textures\\right.jpg',
                  'Textures\Skybox_Textures\left.jpg',
                  'Textures\Skybox_Textures\\top.jpg',
                  'Textures\Skybox_Textures\\bottom.jpg',
                  'Textures\Skybox_Textures\\front.jpg',
                  'Textures\Skybox_Textures\\back.jpg']

renderer.CreateSkybox(textureLIst=skyboxTextures,
                      vShader=skybox_vertex_shader,
                      fShader=skybox_fragment_shader)

faceModel = Model('Gun.obj')
faceModel.AddTextures('Textures\Gun.bmp')
renderer.scene.append(faceModel)
faceModel.rotation.y = 0
faceModel.translation.z = -3
isRunning = True

vShader = vertex_shader
fShader = fragmet_shader
renderer.SetShaders(vShader, fShader)

#Para manipular la camara
camDistance = 5
camAngle = 0


while isRunning:
  #esto va a tener mas uso en un frame rate mas aceptable
  deltaTime = clock.tick(60) / 1000
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      isRunning = False
    elif event.type == pygame.KEYDOWN:
      if event.key  == pygame.K_ESCAPE:
        isRunning = False
      elif event.key == pygame.K_F1:
        renderer.FillMode()
      elif event.key == pygame.K_F2:
        renderer.WireFrameMode()
      elif event.key == pygame.K_3:
        vShader = vertex_shader
        renderer.SetShaders(vShader, fShader)
      elif event.key == pygame.K_4:
        vShader = distortion_shader
        renderer.SetShaders(vShader, fShader)
      elif event.key == pygame.K_5:
        vShader = water_shader
        renderer.SetShaders(vShader, fShader)
      elif event.key == pygame.K_6:
        fShader = fragmet_shader
        renderer.SetShaders(vShader, fShader)
      elif event.key == pygame.K_7:
        fShader = negative_shader
        renderer.SetShaders(vShader, fShader)
  

  #move model
  if keys[K_LEFT]:
    faceModel.rotation.y -=10*deltaTime
  if keys[K_RIGHT]:
    faceModel.rotation.y +=10*deltaTime
  
  

  if keys[K_a]:
    camAngle -= 45 * deltaTime
  if keys[K_d]:
    camAngle += 45 * deltaTime
  if keys[K_w]:
    camDistance -= 2 * deltaTime
  if keys[K_s]:
    camDistance += 2 * deltaTime

  mouseButtons = pygame.mouse.get_pressed()
  if mouseButtons[0]:
    camAngle += pygame.mouse.get_rel()[0] * deltaTime*5

  #Move LIghte
  
  if keys[K_j]:
    renderer.pointLight.x -= 1 *deltaTime
  
  if keys[K_l]:
    renderer.pointLight.x += 1 *deltaTime
  
  if keys[K_i]:
    renderer.pointLight.z -= 1 *deltaTime
  
  if keys[K_k]:
    renderer.pointLight.z += 1 *deltaTime

  renderer.time += deltaTime

  renderer.camera.LookAt(faceModel.translation)
  renderer.camera.Orbit(center=faceModel.translation, distance=camDistance, angle=camAngle)
  renderer.Render()
  pygame.display.flip()

pygame.quit()