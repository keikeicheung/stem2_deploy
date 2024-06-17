from enum import Enum
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output

score_board = {}

full_score = {
    "beginner": 40,
    "ultimate": 60
}

maze_demo_str = """#####
#000E
#0###
#0###
#B###"""

maze1_str = """#E#####
#0#000#
#0#B#0#
#0###0#
#00000#
#######"""

maze2_str = """############
#00#0000000#
E0##0#0##0##
#0000#00#00#
#0####0#####
#0##0000000#
#0000#####0#
#####0000#0#
#000#0##000#
#000#0##0#0#
#0#00000000#
#B##########"""


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Bot:
    __step = 0
    __pos = None
    __direction = None
    maze = None

    def __init__(self, direction, maze):
        self.__direction = direction
        row, col = np.where(maze == 2)
        self.maze = maze
        self.__pos = [row, col]

    def move(self, direction):
        self.__step += 1
        if self.can_move(direction):
            if direction == Direction.UP:
                self.__pos[0] -= 1
                self.__direction = Direction.UP
            elif direction == Direction.DOWN:
                self.__pos[0] += 1
                self.__direction = Direction.DOWN
            elif direction == Direction.LEFT:
                self.__pos[1] -= 1
                self.__direction = Direction.LEFT
            elif direction == Direction.RIGHT:
                self.__pos[1] += 1
                self.__direction = Direction.RIGHT

    def can_move(self, dir):
        if dir == Direction.UP:
            return self.__pos[0] - 1 >= 0 and self.maze[self.__pos[0] - 1, self.__pos[1]] != 1
        elif dir == Direction.DOWN:
            return self.__pos[0] + 1 < len(self.maze) and self.maze[self.__pos[0] + 1, self.__pos[1]] != 1
        elif dir == Direction.LEFT:
            return self.__pos[1] - 1 >= 0 and self.maze[self.__pos[0], self.__pos[1] - 1] != 1
        elif dir == Direction.RIGHT:
            return self.__pos[1] + 1 < len(self.maze[0]) and self.maze[self.__pos[0], self.__pos[1] + 1] != 1
        else:
            return False

    def get_step(self):
        return self.__step

    def reset_step(self):
        self.__step = 0

    def get_y(self):
        return self.__pos[0]

    def get_x(self):
        return self.__pos[1]

    def get_direction(self):
        return self.__direction


def generate_2d_maze(maze_str):
    maze_lines = maze_str.splitlines()
    maze_array = []
    for line in maze_lines:
        row = []
        for char in line:
            if char == '0':
                row.append(0)
            elif char == '#':
                row.append(1)
            elif char == 'B':
                row.append(2)
            elif char == 'E':
                row.append(3)
        maze_array.append(row)
    return np.array(maze_array)


def only_one_step(bot):
    return bot.get_step() <= 1


def draw_maze(maze, bot=None):
    clear_output(wait=True)
    maze_copy = np.copy(maze)
    if bot is not None:
        maze_copy[np.where(maze == 2)] = 0
        maze_copy[bot.get_y(), bot.get_x()] = 2
        bot.reset_step()
    fig, ax = plt.subplots(figsize=(len(maze_copy) * 0.5, len(maze_copy[0]) * 0.5))

    cmap = plt.get_cmap("binary")
    cmap.set_under(color="black")
    cmap.set_over(color="red")

    ax.imshow(maze_copy, cmap=cmap, vmin=0, vmax=3)
    ax.axis("off")

    plt.pause(0.1)
    plt.close(fig)


def finish(maze, bot):
    return maze[bot.get_y(), bot.get_x()] == 3


def run_maze(maze, run, steps, score_key, demo = False):
    counter = 0
    bot = Bot(Direction.UP, maze)
    while counter < steps:
        run(bot)
        if bot.get_step() > 1:
            raise Exception("You cannot ask the bot to move two steps in one round. It's gonna be exhausting 3_3)")
        draw_maze(maze, bot)
        counter += 1
        if finish(maze, bot):
            if demo:
                print("That is how a maze master does things!")
            else:
                score_board[score_key] = full_score[score_key]
                print(f'Thank you! You are doing a great job! Here is your {full_score[score_key]} points.')
            break
    if not finish(maze, bot):
        score_board[score_key] = 0
        print("Sorry you failed to help the bot...")


maze_demo = generate_2d_maze(maze_demo_str)
maze_beginner = generate_2d_maze(maze1_str)
maze_ultimate = generate_2d_maze(maze2_str)


def show_scoreboard():
    print("Here is your scores for the games:")
    print(f'Beginner Maze: {score_board["beginner"]}')
    print(f'Ultimate Maze: {score_board["ultimate"]}')