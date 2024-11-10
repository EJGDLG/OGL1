import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model
import glm
width = 960
height = 540

pygame.init()

# Double buffering
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

renderer = Renderer(screen=screen)

renderer.SetShaders(vShader=vertex_shader, fShader=fragmet_shader)

# Usar prefijos de cadena sin formato para evitar advertencias de secuencias de escape
skyboxTextures = [
    r'Textures\Skybox_Textures\right.jpg',
    r'Textures\Skybox_Textures\left.jpg',
    r'Textures\Skybox_Textures\top.jpg',
    r'Textures\Skybox_Textures\bottom.jpg',
    r'Textures\Skybox_Textures\front.jpg',
    r'Textures\Skybox_Textures\back.jpg'
]

renderer.CreateSkybox(textureLIst=skyboxTextures,
                      vShader=skybox_vertex_shader,
                      fShader=skybox_fragment_shader)

faceModel = Model(r'Gun.obj')
faceModel.AddTextures(r'Textures\Gun.bmp')
renderer.scene.append(faceModel)
faceModel.rotation.y = 0
faceModel.translation.z = -3
isRunning = True

vShader = vertex_shader
fShader = fragmet_shader
renderer.SetShaders(vShader, fShader)

# Variables de cámara
camDistance = 1
camAngle = 0
camHeight = 0  # Nueva variable para altura de la cámara

while isRunning:
    deltaTime = clock.tick(60) / 100
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_F1:
                renderer.FillMode()
            elif event.key == pygame.K_F2:
                renderer.WireFrameMode()
            elif event.key == pygame.K_F3:
                vShader = vertex_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F4:
                vShader = distortion_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F5:
                vShader = water_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F6:
                fShader = fragmet_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F7:
                fShader = negative_shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F8:
                vShader = Wobble_Shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F9:
                vShader = Twist_Shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F10:
                vShader = Ripple_Shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F11:
                fShader = Glow_Shader
                renderer.SetShaders(vShader, fShader)
            elif event.key == pygame.K_F12:
                fShader = Sepia_Shader
                renderer.SetShaders(vShader, fShader)
                
    # Movimiento de la cámara con límites para camHeight y camDistance
    if keys[K_LEFT]:
        faceModel.rotation.y -= 10 * deltaTime
    if keys[K_RIGHT]:
        faceModel.rotation.y += 10 * deltaTime

    if keys[K_a]:
        camAngle -= 45 * deltaTime
    if keys[K_d]:
        camAngle += 45 * deltaTime
    if keys[K_w]:
        camDistance = max(1, camDistance - 2 * deltaTime)  # Zoom In con límite
    if keys[K_s]:
        camDistance = min(5, camDistance + 2 * deltaTime)  # Zoom Out con límite
    if keys[K_UP]:
        camHeight = min(2, camHeight + 1 * deltaTime)      # Mover cámara hacia arriba con límite
    if keys[K_DOWN]:
        camHeight = max(-2, camHeight - 1 * deltaTime)     # Mover cámara hacia abajo con límite

    # Llamar a LookAt y Orbit usando glm.vec3
    renderer.camera.LookAt(glm.vec3(faceModel.translation.x, faceModel.translation.y + camHeight, faceModel.translation.z))
    renderer.camera.Orbit(center=faceModel.translation, distance=camDistance, angle=camAngle)

    renderer.time += deltaTime
    renderer.Render()
    pygame.display.flip()

pygame.quit()
