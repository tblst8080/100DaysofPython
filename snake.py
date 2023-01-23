import turtle as t
import random as r
import time


class Snake:
    def __init__(self, length, color="white"):
        self.controller_mode = None  # switch to determine the control mode
        self.body = []
        self.color = color
        for x in range(0, length):
            self.body.append(t.Turtle(shape="square", visible = False))
            self.body[x].penup()
            self.body[x].shapesize(0.5)
            self.body[x].color(self.color)
            self.body[x].goto(-x * 10, 0)
        self.head = self.body[0]

    def go_forward(self):
        # rest of the body follows the head
        for x in range(len(self.body) - 1, 0, -1):
            posterior = self.body[x]
            anterior = self.body[x - 1]
            posterior.setposition(anterior.position())
            # position = new_position

        # head goes forward
        self.head.forward(10)

    def check_collision(self):
        for segment in range(2, len(self.body)):
            if abs(self.head.position() - self.body[segment].position()) < 10:
                return True

    def turn_left(self):
        self.head.left(90)

    def turn_right(self):
        self.head.right(90)

    def go_north(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def go_south(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def go_west(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def go_east(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def add_length(self):
        delta_x = self.body[-1].xcor() - self.body[-2].xcor()
        delta_y = self.body[-1].ycor() - self.body[-2].ycor()
        new_turtle = t.Turtle(shape="square", visible=False)
        self.body.append(new_turtle)
        self.body[-1].penup()
        self.body[-1].shapesize(0.5)
        self.body[-1].color(self.color)
        self.body[-1].setposition(self.body[-1].xcor() + delta_y, self.body[-1].ycor() + delta_x)
        self.body[-1].showturtle()

    def change_color(self, set_color=False):
        if not set_color:
            return self.color
        else:
            for x in self.body:
                t.colormode(255)
                x.color(set_color, set_color)
                self.color = set_color

    def hide(self):
        for x in self.body:
            x.hideturtle()

    def show(self):
        for x in self.body:
            x.showturtle()

    def controllers(self):
        """Event listener functions for controls. Controls depend on the mode selected."""
        if self.controller_mode == 1:
            t.onkey(fun=self.turn_left, key="Left")
            t.onkey(fun=self.turn_right, key="Right")
        elif self.controller_mode == 2:
            t.onkey(fun=self.go_west, key="Left")
            t.onkey(fun=self.go_east, key="Right")
            t.onkey(fun=self.go_north, key="Up")
            t.onkey(fun=self.go_south, key="Down")

    def change_controls(self, set_controls):
        self.controller_mode = set_controls

    def dissolve(self):
        done = False
        fps = 0.1
        while not done:
            done = True
            unfilled = []
            if fps > 0.002:
                fps -= 0.002
            time.sleep(fps)
            for segment in self.body:
                if segment.fillcolor() != "black":
                    unfilled.append(segment)
                    done = False
            try:
                unfilled[r.randint(0, len(unfilled) - 1)].color("black")
            except:
                pass
            t.update()

    def loop(self, WIDTH, HEIGHT):
        """Loops the snake to the other side when it passes the border"""
        head_x = self.body[0].xcor()
        head_y = self.body[0].ycor()
        if abs(head_x) + 5 >= WIDTH / 2:
            self.body[0].setx(-head_x + ((10 * head_x) / abs(head_x)))
        if abs(head_y) + 5 >= HEIGHT / 2:
            self.body[0].sety(-head_y + ((10 * head_y) / abs(head_y)))


class Writer:
    def __init__(self):
        self.writer = t.Turtle(visible=False)

    def generate(self, x, y, color, size, prompts):
        self.writer.penup()
        self.writer.pencolor(color)
        self.writer.goto(x, y)
        self.writer.write(arg=prompts, move=False, align='center', font=('Comic Sans', size, 'bold'))
        self.writer.hideturtle()

    def scribble(self, x, y, color, size, *prompts):
        self.writer.penup()
        self.writer.pencolor(color)
        self.writer.goto(x, y + (((len(prompts) - 1) * 3 * size)/2))
        for prompt in prompts:
            self.writer.write(arg=f"{prompt}", move=False, align='center', font=('Comic Sans', size, 'bold'))
            self.writer.sety(self.writer.ycor() - 3*size)
        self.writer.hideturtle()

    def remove(self):
        self.writer.reset()


class Scorekeeper:
    def __init__(self):
        self.keeper = t.Turtle(visible=False)
        self.scores = 0

    def generate(self, prompt, x, y, color, size):
        self.keeper.penup()
        self.keeper.pencolor(color)
        self.keeper.goto(x, y)
        self.keeper.write(arg=prompt, move=False, align='center', font=('Comic Sans', size, 'bold'))
        self.keeper.hideturtle()

    def remove(self):
        self.keeper.reset()

    def show_score(self):
        self.remove()
        self.generate(prompt=f"Score: {self.scores}", x=0, y=0, color="grey", size=15)

    def show_final_score(self):
        self.remove()
        self.keeper.pencolor("red")
        self.generate(prompt=f"Final score: {self.scores}", x=-50, y=0, color="grey", size=20)

    def add_score(self, amount = 1):
        self.scores += amount
