import turtle as t
import random as r
import time

COLOR = "white"
DEFAULT_HEIGHT = 400
DEFAULT_WIDTH = 400


class Objects:
    def __init__(self, height, width):
        # generating food turtle
        self.obj = t.Turtle(visible=False)
        self.obj.penup()
        self.buffer = None

        self.HEIGHT = height
        self.WIDTH = width

    # sends food to random spot on green
    def generate(self, exclusion_list):
        x_spot = r.randint(-self.WIDTH / 2 + self.buffer, self.WIDTH / 2 - self.buffer)
        y_spot = r.randint(-self.HEIGHT / 2 + self.buffer, self.HEIGHT / 2 - self.buffer)
        self.obj.goto(x_spot, y_spot)
        self.obj.showturtle()
        for exclusion in exclusion_list:
            if exclusion != self.obj:
                if abs(self.obj.xcor() - exclusion.xcor()) < 20 and abs(self.obj.ycor() - exclusion.ycor()) < 20:
                    return self.generate(exclusion_list)

    def hide(self):
        self.obj.hideturtle()

    def show(self):
        self.obj.showturtle()

    def start_obj(self, exclude):
        if not self.obj.isvisible():
            self.generate(exclusion_list=exclude)


class Fodder(Objects):
    def __init__(self, height, width):
        super().__init__(height, width)
        # generating food turtle
        self.obj.shape("square")
        self.obj.color(COLOR)
        self.obj.shapesize(.6)
        self.buffer = 10


class TimeBomb(Objects):
    def __init__(self, height, width):
        super().__init__(height, width)
        # generating food turtle
        self.obj.shape("circle")
        self.obj.color("red")
        self.obj.shapesize(1)
        self.buffer = 15  # distance from edge

        # keeps time
        self.timekeeper = t.Turtle(visible=False)
        self.start_time = 0
        self.count_down = 0
        self.paused_time = None

        # animation frame
        self.animate_frame = 0

        # explosion switch
        self.timeout = False

        # golden bomb
        self.luck = 20
        self.random_pull = None



    def generate(self, exclusion_list = None):
        super().generate(exclusion_list)
        self.roll_golden()
        self.start_time = time.perf_counter()

    def tracker(self):
        self.count_down = 11 - (time.perf_counter() - self.start_time)
        self.timekeeper.reset()
        self.timekeeper.penup()
        self.timekeeper.pencolor(self.obj.fillcolor())
        self.timekeeper.goto(self.WIDTH / 2, self.HEIGHT / 2 - 40)
        self.timekeeper.write(arg=f"{int(self.count_down)}s", move=False, align='right',
                              font=('Comic Sans', 20, 'bold'))
        self.timekeeper.hideturtle()
        if self.count_down <= 0 and self.obj.isvisible():  # out of time
            if self.obj.fillcolor() != "yellow":
                self.explosion()
                self.timeout = True
            else:
                pass
            self.timekeeper.reset()

    def animate(self):
        self.animate_frame += 1
        if self.animate_frame == 2:
            self.animate_frame = 0
            if self.obj.shapesize() == (1, 1, 1):
                self.obj.shapesize(.8, .8, .8)
            elif self.obj.shapesize() == (.8, .8, .8):
                self.obj.shapesize(.5, .5, .5)
            else:
                self.obj.shapesize(1, 1, 1)

    def explosion(self):
        t.colormode(255)
        set_color = [255, 0, 0]
        for x in range(0, 200):
            time.sleep(0.01)
            self.animate_frame += 0.6 * (x + 1) / 30
            set_color[1] = x
            set_color[2] = x
            self.obj.color((set_color[0], set_color[1], set_color[2]))
            self.obj.shapesize(self.animate_frame)
            t.update()
        self.obj.hideturtle()

    def roll_golden(self):
        if self.random_pull != self.luck:
            self.random_pull = r.randint(0, self.luck)
        else:
            self.random_pull = 0
        if self.random_pull == self.luck:
            self.obj.color("yellow")
            return True
        else:
            self.obj.color("red")
            return False

    def pause(self):
        self.paused_time = self.count_down
        self.count_down = None

    def resume(self):
        self.count_down = self.paused_time
        self.start_time = self.paused_time + time.perf_counter() - 11




class MineField(Objects):
    def __init__(self, height, width):
        super().__init__(height, width)
        # generating food turtle
        self.obj.shape('triangle')
        self.obj.color("purple")
        self.obj.shapesize(1)
        self.buffer = 15

        self.HEIGHT = height
        self.WIDTH = width

        self.animate_frame = 0

        self.exploded = False

        # sends food to random spot on green

    def generate(self, exclusion_list):
        super().generate(exclusion_list)

    def animate(self):
        self.animate_frame += 1
        if self.animate_frame == 1:
            self.animate_frame = 0
            self.obj.left(10)

    def detonate(self):
        for x in range(0, 20):
            self.obj.shapesize(1.5)
            time.sleep(0.02)
            self.obj.left(20)
            t.update()
        self.exploded = True

    def hide(self):
        super().hide()

    def show(self):
        super().show()

