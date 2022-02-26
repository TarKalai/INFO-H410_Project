import pygame
from game_ui import WIDTH, HEIGHT, Slide2048
import os
# from EightPuzzle_astar import playAIGame
# from EightPuzzle_RL import initPlayerAI
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="8Puzzle game.")

    parser.add_argument(
        "-a",
        "--astar",
        action="store_true",
        help="Start the program in A* mode.",
    )
    parser.add_argument(
        "-r", 
        "--rl", 
        action="store_true", 
        help="Start the program in RL mode."
    )
    args = parser.parse_args()
    pygame.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption("2048 game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fpsclock = pygame.time.Clock()

    while True:
        slide2048 = Slide2048((4, 4), 120, 5, screen)
        #if args.astar:
        #    choice = slide2048.selectPlayerMenu("2048 using A* search")
        #elif args.rl:
        #    choice = slide2048.selectPlayerMenu(
        #        "2048 using Reinforcement Learning"
        #    )
        #else:
        #    parser.print_help()
        #    print()
        #    print("Please select an option (--astar, or --rl)")
        #    sys.exit()
        slide2048.draw()

        print("bonjour")



if __name__ == "__main__":
    main()
