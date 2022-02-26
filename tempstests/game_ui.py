import sys, os, random
import re
import pathlib
import pygame

# Constant for the size of the screen.
WIDTH = 800
HEIGHT = 500
# Constant for the size of the text.
TXT_CORE_SIZE = 38
TXT_MENU_SIZE = 50

class Slide2048:
    def __init__(self, grid_size, tile_size, margin_size, screen):
        """
        Init the game.

        :param grid_size: The grid size. It is a tuple (n,n) of Int.
        :param tile_size: The size of the tiles. It is an Int.
        :param margin_size: The size of the margin. It is an Int.
        :param screen:      The screen, Surface object.
        """
        # Attributes for the main core of the game.
        self.screen = screen

        self.grid_size, self.tile_size, self.margin_size = grid_size, tile_size, margin_size
        self.tiles_len = grid_size[0] * grid_size[1] - 1
        # Tiles is a list of position [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
        # for grid_size = (3, 3).
        self.tiles = [(x, y) for y in range(grid_size[1]) for x in range(grid_size[0])]
        # The win condition is the same list but we do not want to change to compare it with tiles.
        self.winCdt = [(x, y) for y in range(grid_size[1]) for x in range(grid_size[0])]

        # actual pos on the screen.
        self.tilepos = [
            (x * (tile_size + margin_size) + margin_size, y * (tile_size + margin_size) + margin_size)
            for y in range(grid_size[1])
            for x in range(grid_size[0])
        ]

        # the place they slide to.
        self.tilePOS = {
            (x, y): (x * (tile_size + margin_size) + margin_size, y * (tile_size + margin_size) + margin_size)
            for y in range(grid_size[1])
            for x in range(grid_size[0])
        }
        self.nb_move = 0
        # Speed for the move of tiles.
        self.speed = 3
        # Previous tile.
        self.prev = None
        # Boolean if the player want to return to the main menu.
        self.want_to_quit = False
        # boolean for toogling autoPlay
        self.autoPlay = False
        self.last = 0

        # Attributes for the image of the game.
        # Create a rectangle for the game according to the grid size, the size of tiles and the size of
        # margin.
        self.rect = pygame.Rect(
            0, 0, grid_size[0] * (tile_size + margin_size) + margin_size, grid_size[1] * (tile_size + margin_size) + margin_size
        )
        #self.pic = pygame.transform.smoothscale(
        #    pygame.image.load(
        #        pathlib.Path("assetile_size") / pathlib.Path("image.png")
        #    ),
        #    self.rect.size,
        #)
        # Partition the image according to the number of tiles.
        self.images = []
        font = pygame.font.Font(None, 120)
        #number_image = font.render( "8", True, BLACK, WHITE )  # Number 8
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]
            #image = self.pic.subsurface(x, y, tile_size, tile_size)
            text = font.render(str(i + 1), True , (128, 128, 128))
            w, h = text.get_size()
            screen.blit(text, ((tile_size - w) / 2, (tile_size - h) / 2))
            self.images += [screen]

    def playHumanGame(self, fpsclock):
        """
        Play the game.

        :param fpsclock: Track time, Clock object.
        """
        while not self.want_to_quit:
            dt = fpsclock.tick()
            self.screen.fill((0, 0, 0))
            self.draw()
            self.drawShortcuts(True, True)
            pygame.display.flip()
            self.catchGameEvents(True, None)
            self.update(dt)
            self.checkGameState(False)

    def selectPlayerMenu(self, AI_type):
        """
        Ask to the player if he wants to play or if he wants an AI to play.

        :param AI_type  A string representing which type of AI you are using
        :return:        Return a String that reprensent the choice of the player.
                        It returns "human" or "AI".
        """
        self.screen.fill((0, 0, 0))
        self.drawText(AI_type, TXT_MENU_SIZE, 400, 50, 255, 255, 255, True)
        self.drawText(
            "Press <h> to play", TXT_MENU_SIZE, 400, 150, 255, 255, 255, True
        )
        self.drawText(
            "Press <a> to run the AI",
            TXT_MENU_SIZE,
            400,
            250,
            255,
            255,
            255,
            True,
        )
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                self.catchExitEvent(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.shuffle()
                        return "human"
                    if event.key == pygame.K_a:
                        return "AI"

    def draw(self):
        """
        Draw the game with the number of move.
        """
        #for i in range(self.tiles_len):
        #    x, y = self.tilepos[i]
        #    self.screen.blit(x+y, (x, y))
        self.drawText(
            "Moves : {}".format(self.nb_move),
            TXT_CORE_SIZE,
            500,
            10,
            255,
            255,
            255,
            False,
        )

    
    def catchExitEvent(self, event):
        """
        Check if it is a quit event.

        :param event:   Event object.
        """
        if event.type == pygame.QUIT:
            self.exit()

    def shuffle(self):
        """
        Shuffle tiles and check if the board is solvable.
        """
        print("shuf")
        while not self.isSolvable():
            random.shuffle(self.tiles)

    def isSolvable(self):
        """
        Check if the game is solvable.

        :return: Return a Boolean, True if the board is solvable, otherwise False.
        
        tiles = []
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                if self.tiles[j][1] * 3 + self.tiles[j][0] + 1 == i + 1:
                    tiles.append(j + 1)
        count = 0
        for i in range(len(tiles) - 1):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j] and tiles[i] != 9:
                    count += 1
        return True if (count % 2 == 0 and count != 0) else False
        """
        return True

    def catchGameEvents(self, is_player, movefunc):
        """
        Catchs event during the game and during the board creation.

        :param is_player:       A boolean value to check if it is a game with a player or with an AI.
        :return:                Return True if the player want to quit the game.
                                Otherwise, False.
        """
        for event in pygame.event.get():
            self.catchExitEvent(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.want_to_quit = self.pauseMenu()
                    return
            if is_player:
                self.playEvents(event)
            elif (
                not is_player
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                movefunc()
            elif (
                not is_player
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_a
            ):
                self.autoPlay = not self.autoPlay

        now = pygame.time.get_ticks()
        if self.autoPlay and now - self.last >= 300:
            self.last = pygame.time.get_ticks()
            movefunc()

        self.want_to_quit = False

    def update(self, dt):
        """
        Update the view.

        :param dt: Derived time. It is an Int.
        """
        # If the value between the current and target is less than speed, we can just let it jump right into place.
        # Otherwise, we just need to add/sub in direction.
        s = self.speed * dt
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]  # current pos
            X, Y = self.tilePOS[self.tiles[i]]  # target pos
            dx, dy = X - x, Y - y

            self.tilepos[i] = (
                X if abs(dx) < s else x + s if dx > 0 else x - s
            ), (Y if abs(dy) < s else y + s if dy > 0 else y - s)

    def checkGameState(self, is_AI):
        """
        Check if the game is won. If it is won, we ask to the player if he want
        the play again, quit the game or want to go to the main menu.

        :param fpsclock:    Track time, Clock object.
        :param is_AI:       A boolean value to check if it is a game with a player or with an AI.
        :return:            Return False if the game is won or if the player want
                            to play again. Otherwise, False.
        """
        if self.isWin():
            self.want_to_quit = self.exitMenu(is_AI)
            return True
        return False

    def isWin(self):
        return False

    def playEvents(self, event):
        """
        Catch events from the mouse and the keyboard.
        Binded keys:
            - z moves the tile upwards
            - s moves the tile downwards
            - q moves the tile to the left
            - d moves the tile to the right
            - space choose a random mouvement

        :param event:   The current event, Event object.
        """
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        # If we use the left click
        if mouse[0]:
            # We convert the position of the mouse according to the grid position and the margin
            x, y = mpos[0] % (self.tile_size + self.margin_size), mpos[1] % (self.tile_size + self.margin_size)
            if x > self.margin_size and y > self.margin_size:
                tile = mpos[0] // self.tile_size, mpos[1] // self.tile_size
                if self.inGrid(tile) and tile in self.adjacent():
                    self.switch(tile, False)

        if event.type == pygame.KEYDOWN:
            for key, dx, dy in (
                (pygame.K_s, 0, -1),
                (pygame.K_z, 0, 1),
                (pygame.K_d, -1, 0),
                (pygame.K_q, 1, 0),
            ):
                if event.key == key:
                    x, y = self.opentile
                    tile = x + dx, y + dy
                    if self.inGrid(tile):
                        self.switch(tile, False)
            # Move randomly a tile.
            if event.key == pygame.K_SPACE:
                for _ in range(1000):
                    self.random()
    
    def drawText(self, text, size, x, y, R, G, B, center):
        """
        Draw text.

        :param text:    The text to draw on the  String.
        :param size:    The size of the text, Int.
        :param x:       The x position of the text, Int.
        :param y:       The y position of the text, Int.
        :param R:       The R color, Int.
        :param G:       The G color, Int.
        :param B:       The B color, Int.
        :param center:  If the text need to be in the center, Boolean.
        """
        font = pygame.font.Font(None, size)
        text = font.render(text, True, (R, G, B))
        if center:
            text_rect = text.get_rect()
            text_rect.midtop = (x, y)
            self.screen.blit(text, text_rect)
        else:
            self.screen.blit(text, (x, y))

    def drawShortcuts(self, is_player, qValues):
        """
        Draw in game shortcuts.

        :param is_player:   A Boolean, it checks if it is a player because, shorcuts are different in
                            the player mode or in the AI mode.
        """
        self.drawText("Shortcuts", TXT_CORE_SIZE, 500, 40, 255, 255, 255, False)
        self.drawText(
            "Pause: Escape", TXT_CORE_SIZE, 500, 70, 255, 255, 255, False
        )
        if is_player:
            self.drawText(
                "Move up: <z>", TXT_CORE_SIZE, 500, 100, 255, 255, 255, False
            )
            self.drawText(
                "Move down: <s>", TXT_CORE_SIZE, 500, 130, 255, 255, 255, False
            )
            self.drawText(
                "Move left: <q>", TXT_CORE_SIZE, 500, 160, 255, 255, 255, False
            )
            self.drawText(
                "Move right: <d>",
                TXT_CORE_SIZE,
                500,
                190,
                255,
                255,
                255,
                False,
            )
            self.drawText(
                "Random move: <Space>",
                TXT_CORE_SIZE,
                500,
                220,
                255,
                255,
                255,
                False,
            )
        else:
            self.drawText(
                "AI move: <Space>",
                TXT_CORE_SIZE,
                500,
                100,
                255,
                255,
                255,
                False,
            )
            self.drawText(
                "auto AI move: <a>",
                TXT_CORE_SIZE,
                500,
                130,
                255,
                255,
                255,
                False,
            )
            if qValues != None:
                self.drawText(
                    "State's Q-Values",
                    TXT_CORE_SIZE,
                    500,
                    190,
                    255,
                    255,
                    255,
                    False,
                )
                self.drawText(
                    "UP: {0:.2E}".format(qValues[0]),
                    TXT_CORE_SIZE,
                    500,
                    220,
                    255,
                    255,
                    255,
                    False,
                )
                self.drawText(
                    "RIGHT: {0:.2E}".format(qValues[1]),
                    TXT_CORE_SIZE,
                    500,
                    250,
                    255,
                    255,
                    255,
                    False,
                )
                self.drawText(
                    "DOWN: {0:.2E}".format(qValues[2]),
                    TXT_CORE_SIZE,
                    500,
                    280,
                    255,
                    255,
                    255,
                    False,
                )
                self.drawText(
                    "LEFT: {0:.2E}".format(qValues[3]),
                    TXT_CORE_SIZE,
                    500,
                    310,
                    255,
                    255,
                    255,
                    False,
                )
    def exit(self):
        """
        Exit the application.
        """
        pygame.quit()
        sys.exit()