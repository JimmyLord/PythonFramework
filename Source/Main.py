import OpenGL.GL as gl
import pygame

from imgui.integrations.pygame import PygameRenderer
import imgui

from Framework.Vector import vec2Test

import GameSimple
import GameSokoban
import GameWaterTest
import GameDissolve

class Core:
    def __init__(self):
        pass

    def processEvents(self):
        # Process all pygame events, pass each of them into the Game class.
        for event in pygame.event.get():
            self.imGuiManager.process_event( event )
            if event.type == pygame.QUIT:
                self.running = False       
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            self.game.onEvent( event )

    def update(self):
        # Start a new imgui frame, so Game and GameObject updates can add to it.
        imgui.new_frame()

        # Add in a menu bar.
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu( "File", True ):
                clicked_quit, selected_quit = imgui.menu_item( "Quit", '', False, True )
                if clicked_quit:
                    self.running = False
                imgui.end_menu()
            imgui.end_main_menu_bar()

        # Add a game selector debug menu.
        imgui.begin( "Game Selector", True )
        if imgui.button( "Simple" ):
            self.game = GameSimple.GameSimple()
        if imgui.button( "Sokoban" ):
            self.game = GameSokoban.GameSokoban()
        if imgui.button( "Water Test" ):
            self.game = GameWaterTest.GameWaterTest()
        if imgui.button( "Effect - Dissolve" ):
            self.game = GameDissolve.GameDissolve()
        imgui.end()

        # Uncomment this to see what imgui can do.
        # imgui.show_test_window()

        # Calculate deltaTime and update all game objects by that much time.
        currentTime = pygame.time.get_ticks()
        deltaTime = (currentTime - self.timeAtStartOfLastFrame) / 1000.0
        self.timeAtStartOfLastFrame = currentTime
        self.game.update( deltaTime )

        # Calculate and display FPS.
        self.frameCount += 1
        if currentTime - self.frameResetTime > 1000:
            self.lastFPS = self.frameCount
            self.frameCount = 0
            self.frameResetTime = currentTime

        imgui.begin( "FPS Counter" )
        imgui.text( "FPS: " + str(self.lastFPS) )
        imgui.end()

    def draw(self):
        # Clear the window to dark blue.
        gl.glClearColor( 0, 0, 0.2, 1 )
        gl.glClear( gl.GL_COLOR_BUFFER_BIT )

        # Draw the game.
        self.game.sprite.drawSetup()
        self.game.draw()
        self.game.sprite.drawCleanup()

        # Draw imgui windows.
        imgui.render()

        # Display what we drew.
        pygame.display.flip()

    def main(self):
        # Initialize pygame.
        pygame.init()

        size = (800, 600)

        # Initialize pygame in OpenGL mode.
        pygame.display.set_mode( size, pygame.DOUBLEBUF | pygame.OPENGL )

        # Get number of milliseconds since pygame.init() was called.
        self.timeAtStartOfLastFrame = pygame.time.get_ticks()

        # Setup some vars for FPS counter.
        self.lastFPS = 0
        self.frameCount = 0
        self.frameResetTime = self.timeAtStartOfLastFrame

        # Setup some imgui stuff.
        self.imGuiManager = PygameRenderer()
        io = imgui.get_io()
        io.fonts.add_font_default()
        io.display_size = size

        # Create an instance of our Game class.
        self.game = GameDissolve.GameDissolve()

        # Main game loop: keep looping until Game says it's time to quit.
        self.running = True
        while self.running:
            self.processEvents()
            self.update()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    # vec2Test()

    core = Core()
    core.main()
