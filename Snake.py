from tkinter import *
import random

# Constants
TITLE = 'Snake Game'
GAME_WIDTH = 1000
GAME_HEIGHT = 500
SPEED = 50
SPACE_SIZE = 50
DIMENSION_X, DIMENSION_Y = GAME_WIDTH // SPACE_SIZE, GAME_HEIGHT // SPACE_SIZE
BODY_PARTS = 3

SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Window:
    def __init__(self):
        self.window = Tk()
        self.window.title(TITLE)
        self.canvas = None
        self.label = None
        self.score = 0
        self.Configuration()
        self.snake = None
        self.squares = []
        self.food = None
        self.food_square = None
        self.game_finished = False
        self.init_elements()
        self.bind_actions()
        self.render_elements()
        self.next_turn()


    def Configuration(self):
        self.window.resizable(False, False)  # Can be changed later on
        self.label = Label(self.window, text=f'Score:{self.score}', font=('consolas', 40))
        self.label.pack()

        self.canvas = Canvas(self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()
        self.window.update()

        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def init_elements(self):
        self.snake = Snake()
        self.food = Food()
        self.food.find_possible_position(self.snake)

    def render_elements(self):
        for coordinate in self.snake.coordinates:
            x, y = coordinate[0], coordinate[1]
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.snake.color,
                                                  tags='Snake')

            self.squares.append(square)
        self.food_square = self.canvas.create_oval(self.food.x, self.food.y, self.food.x + SPACE_SIZE,
                                                   self.food.y + SPACE_SIZE, fill=self.food.color, tags='Food')

    def bind_actions(self):
        self.window.bind('<Left>', lambda event: self.snake.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.snake.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.snake.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.snake.change_direction('down'))

    def game_over(self):
        del self.food
        for square in self.squares:
            self.canvas.delete(square)
        self.canvas.delete(self.food_square)
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, font=('consolas', 70),
                                text="GAME OVER", fill="red", tag="Game Over")


    def next_turn(self):
        if self.game_finished:
            self.game_over()
        else:
            x, y = self.snake.coordinates[-1][0], self.snake.coordinates[-1][1]
            if self.snake.direction == "up":
                y -= SPACE_SIZE
            if self.snake.direction == "down":
                y += SPACE_SIZE
            if self.snake.direction == "left":
                x -= SPACE_SIZE
            if self.snake.direction == "right":
                x += SPACE_SIZE

            self.snake.coordinates.append((x, y))
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.snake.color,
                                                  tags='Snake')
            self.squares.append(square)
            if self.snake.if_eaten(self.food):
                self.score += 1
                self.label.config(text=f'Score:{self.score}')
                self.canvas.delete('Food')
                self.food = Food()
                self.food.find_possible_position(self.snake)
                self.food_square = self.canvas.create_oval(self.food.x, self.food.y, self.food.x + SPACE_SIZE,
                                                           self.food.y + SPACE_SIZE, fill=self.food.color, tags='Food')
            else:
                self.snake.coordinates = self.snake.coordinates[1:]
                self.canvas.delete(self.squares[0])
                self.squares = self.squares[1:]
            if self.snake.check_collisions():
                self.game_finished = True
            self.window.after(SPEED, self.next_turn)


class Snake:
    def __init__(self):
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.direction = 'down'
        self.color = SNAKE_COLOR

    def change_direction(self, new_direction):
        if new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        if new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        if new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction

    def check_collisions(self):
        x, y = self.coordinates[-1][0], self.coordinates[-1][1]
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        for body_part in self.coordinates[:-1]:
            if x == body_part[0] and y == body_part[1]:
                return True
        return False

    def if_eaten(self, food):
        x, y = self.coordinates[-1][0], self.coordinates[-1][1]
        if x == food.x and y == food.y:
            return True
        return False

    # def __del__(self):
    #     self.coordinates = None
    #     self.direction = None


class Food:
    def __init__(self):
        self.x = random.randint(0, DIMENSION_X - 1) * SPACE_SIZE
        self.y = random.randint(0, DIMENSION_Y - 1) * SPACE_SIZE
        self.color = FOOD_COLOR

    def find_possible_position(self, snake):
        while [self.x, self.y] in snake.coordinates:
            self.x = random.randint(0, DIMENSION_X - 1) * SPACE_SIZE
            self.y = random.randint(0, DIMENSION_Y - 1) * SPACE_SIZE

    def __del__(self):
        self.x = None
        self.y = None


def main():
    game = Window()
    game.window.mainloop()


if __name__ == '__main__':
    main()
