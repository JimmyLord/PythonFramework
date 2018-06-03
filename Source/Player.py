import pygame
import imgui

import GameObject

class Player(GameObject.GameObject):
    def __init__(self, position, sprite, texture):
        super().__init__( position, sprite, texture )

    def onEvent(self, event):
        super().onEvent( event )

        # Inputs will set the direction the player is moving.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction.y += 1
            if event.key == pygame.K_s:
                self.direction.y += -1
            if event.key == pygame.K_a:
                self.direction.x += -1
            if event.key == pygame.K_d:
                self.direction.x += 1
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.direction.y -= 1
            if event.key == pygame.K_s:
                self.direction.y -= -1
            if event.key == pygame.K_a:
                self.direction.x -= -1
            if event.key == pygame.K_d:
                self.direction.x -= 1        

    def update(self, deltaTime):
        # GameObject update will do the actual player movement.
        super().update( deltaTime )

        # Debug info displayed using imgui.
        imgui.begin( "Player", True )
        changed, newvalue = imgui.slider_float2( "Position", self.position.x, self.position.y, 0, 20 )
        self.position.x = newvalue[0]
        self.position.y = newvalue[1]
        imgui.end()        

    def draw(self):
        super().draw()
