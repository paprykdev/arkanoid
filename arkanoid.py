import curses
import random


class Paddle:
    def __init__(self, window, height, width):
        self.window = window
        self.height = height
        self.width = width
        self.x = width // 2 - 5
        self.y = self.height - 1
        self.paddle_width = 10

    def draw(self):
        self.window.addstr(self.y, self.x, "===========")

    def move_left(self):
        if self.x > 0:
            self.x -= 1

    def move_right(self):
        if self.x < self.width - self.paddle_width - 2:
            self.x += 1


class Ball:
    def __init__(self, window, height, width):
        self.window = window
        self.height = height
        self.width = width
        self.x = width // 2
        self.y = height // 2
        self.dx = 0
        self.dy = 1

    def draw(self):
        self.window.addch(self.y, self.x, "o")

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x == 0 or self.x == self.width - 1:
            self.dx = -self.dx
        if self.y == 0:
            self.dy = -self.dy

    def bounce(self):
        self.dy = -self.dy

    def bounce_left(self):
        self.dy = -self.dy
        self.dx = -1

    def bounce_right(self):
        self.dy = -self.dy
        self.dx = 1


class Brick:
    def __init__(self, window, i, j):
        self.window = window
        self.x = j * 3 - 1
        self.y = i
        self.width = 3

    def draw(self):
        self.window.addstr(self.y, self.x, "###")


def end_game(score, window, height, width):
    window.clear()
    window.addstr(height // 2, width // 2 - 4, "Game Over")
    window.addstr(height // 2 + 1, width // 2 - 4, f"Score: {score}")
    window.addstr(height // 2 + 3, width // 2 - 10, "Press any key to exit")
    window.addstr(height // 2 + 4, width // 2 - 10, "or Ctrl+C to restart")
    window.refresh()
    while True:
        key = window.getch()
        if key != -1 and key != curses.KEY_LEFT and key != curses.KEY_RIGHT:
            break
    window.clear()
    window.refresh()


def main(stdscr):
    try:
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.timeout(100)
        height, width = stdscr.getmaxyx()
        window = curses.newwin(height, width, 0, 0)
        window.keypad(1)
        window.timeout(100)

        paddle = Paddle(window, height, width)
        paddle.draw()

        ball = Ball(window, height, width)
        ball.draw()

        score = 0

        bricks = []
        for i in range(1, random.randint(5, 15)):
            for j in range(1, width // 3):
                if random.randint(0, 1):
                    bricks.append(Brick(window, i, j))

        while True:
            key = window.getch()
            if key == curses.KEY_LEFT:
                paddle.move_left()
            elif key == curses.KEY_RIGHT:
                paddle.move_right()

            ball.move()

            if ball.y == height - 2:
                cond2 = ball.x < paddle.x + paddle.paddle_width // 2
                cond1 = ball.x >= paddle.x
                cond3 = ball.x >= paddle.x + paddle.paddle_width // 2
                cond4 = ball.x < paddle.x + paddle.paddle_width
                if cond1 and cond2:
                    ball.bounce_left()
                elif cond3 and cond4:
                    ball.bounce_right()
                else:
                    break

            for brick in bricks:
                if ball.y == brick.y and\
                        ball.x >= brick.x and \
                        ball.x < brick.x + brick.width:
                    bricks.remove(brick)
                    score += 10
                    ball.bounce()
                    break

            if not bricks:
                break

            window.clear()
            paddle.draw()
            ball.draw()
            for brick in bricks:
                brick.draw()
            window.refresh()

        end_game(score, window, height, width)
    except KeyboardInterrupt:
        try:
            for timer in range(2, 0, -1):
                string = f"Restarting in {timer}.."
                window.clear()
                window.addstr(height // 2, width // 2 - len(string) // 2, string)
                window.refresh()
                curses.napms(1000)
            main(stdscr)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    curses.wrapper(main)
