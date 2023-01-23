import turtle as t
from snake import Snake, Writer, Scorekeeper
from food import Fodder, TimeBomb, MineField
import time

color_set = ['red', 'yellow', 'orange', 'green', 'blue']


class Game:
    def __init__(self):
        # Set game boundaries/dimensions
        self.loading = None
        self.difficulty = None
        self.WIDTH = 400
        self.HEIGHT = 400

        # Game settings
        self.stage_2 = 15
        self.stage_3 = 30
        self.stage_4 = 45
        self.stage_lock = False

        self.control_mode = 1

        # In-game objects
    def set_objects(self):
        self.GameSnake = Snake(3, color="white")  # generate Snake variable
        self.GameSnake.controller_mode = self.control_mode
        self.feed = Fodder(height=self.HEIGHT, width=self.WIDTH)  # generate food object
        self.bomb = TimeBomb(height=self.HEIGHT, width=self.WIDTH)  # generates time bomb
        self.mine = MineField(height=self.HEIGHT, width=self.WIDTH)
        self.all_objects = [self.feed.obj]

        # Functional Objects
        self.messenger = Writer()  # writes messages inside the game
        self.scoreboard = Scorekeeper()  # turtle shows score
        self.scoreboard.scores = 0
        self.GameScreen = False

        # Screen Setting
    def set_screen(self):
        self.GameScreen = t.Screen()  # generate screen
        self.GameScreen.bgcolor("Black")  # set the background black
        self.GameScreen.setup(width=self.WIDTH + 10, height=self.HEIGHT + 10)  # set up pop-up window dimensions
        self.GameScreen.title(titlestring="Welcome to the Snake Game")  # Screen title
        self.GameScreen.tracer(False)  # turns animation off (until update)

    def title_card(self):
        """Shows the title card message. Prompts window for selecting control modes."""
        self.set_objects()
        self.set_screen()
        t.listen()
        self.messenger.generate(prompts="Welcome to the Snake Game!", x=0, y=0, color="white", size=15)
        time.sleep(2)
        self.choose_mode()
        self.GameScreen.update()
        return self.start_game()

    def start_game(self):
        """Runs the Game"""
        self.set_screen()
        self.scoreboard.scores = 0
        self.difficulty = [255, 255, 255]
        self.messenger.remove()
        self.draw_border()
        self.GameSnake.show()
        for segment in self.GameSnake.body:
            self.all_objects.append(segment)
        self.hints()
        self.scoreboard.show_score()
        self.feed.generate(exclusion_list=self.all_objects)
        self.moving()
        self.game_over()
        self.GameScreen.clearscreen()
        self.set_objects()
        return self.start_game()

    def game_over(self):
        self.GameSnake.dissolve()
        time.sleep(.6)
        self.GameScreen.clearscreen()  # generate screen
        self.loading = True
        self.GameScreen.tracer(False)
        self.GameScreen.bgcolor("black")  # set the background black
        self.messenger.generate(prompts=f"GAME OVER", x=0, y=30, color="red", size=30)
        self.messenger.generate(prompts=f"FINAL SCORE: {self.scoreboard.scores}", x=0, y=-30, color="red", size=30)
        self.messenger.generate(prompts=f"Press any key to restart", x=0, y=-self.HEIGHT / 2 + 10, color="grey",
                                size=10)
        self.GameSnake = Snake(7, color="black")
        while self.loading:
            self.GameSnake.show()
            self.GameScreen.listen()
            time.sleep(0.06)
            self.GameSnake.go_forward()
            self.GameSnake.loop(HEIGHT=self.HEIGHT, WIDTH=self.WIDTH)  # spatial loop if snake passes boundary
            self.GameScreen.update()
            self.GameScreen.onkeypress(fun=self.close_loading)


    def moving(self):  # performs the following functions for every round of motion
        """A series of automatic functions while the game is ongoing."""
        continue_moving = True
        while continue_moving:
            t.listen()  # listen for user input (directions)
            time.sleep(0.065)
            self.GameSnake.controllers()  # checks for direction change
            self.GameScreen.onkey(fun=self.choose_mode, key='c')  # allows user access screen for switching modes
            self.GameScreen.onkey(fun=self.show_rules, key='r')
            self.GameSnake.go_forward()  # snake goes forward by 1 unit
            self.GameSnake.loop(WIDTH=self.WIDTH, HEIGHT=self.HEIGHT)  # spatial loop if snake passes boundary
            self.calibrate_level()
            self.GameScreen.update()  # update screen
            self.eating()  # regenerate food if eaten (set after screen update to avoid unwanted flashes of animation)
            if self.condition_dead():  # check if snake is still alive
                continue_moving = False

    def eating(self):
        """Checks if food (square turtle object) is eaten.
        If food is eaten, function generates a new food in a random location within the boundaries. """

        # food
        if abs(self.feed.obj.position() - self.GameSnake.body[0].position()) < 13:
            self.GameSnake.add_length()  # grow the snake
            self.all_objects.append(self.GameSnake.body[-1])
            self.feed.generate(exclusion_list=self.all_objects)  # generate additional food

            self.scoreboard.add_score()
            self.scoreboard.show_score()

            # lightening effect at stage 3
            if self.scoreboard.scores >= self.stage_4:
                for x in range(0, 3):
                    if self.difficulty[x] <= 215:
                        self.difficulty[x] += 40
                self.GameSnake.change_color(set_color=self.difficulty)

            # trigger for mine in stage 4
            if self.scoreboard.scores >= self.stage_3:
                self.mine.generate(exclusion_list=self.all_objects)

        # time bombs
        if self.scoreboard.scores >= self.stage_2:
            # if normal bomb:
            if self.bomb.obj.fillcolor() != "yellow":
                # if bomb is eaten:
                if abs(self.bomb.obj.position() - self.GameSnake.body[0].position()) < 14:
                    self.GameSnake.add_length()  # grow the snake
                    self.all_objects.append(self.GameSnake.body[-1])
                    self.bomb.generate(exclusion_list=self.all_objects)
                    self.scoreboard.add_score()
                    self.scoreboard.show_score()

                    # darkening difficulty
                    if self.scoreboard.scores >= self.stage_4:
                        for x in range(0, 3):
                            if self.difficulty[x] >= 40:
                                self.difficulty[x] -= 40
                            elif self.difficulty[x] < 40:
                                self.difficulty[x] = 5
                        self.GameSnake.change_color(set_color=self.difficulty)
            # Yellow bomb:
            else:
                if abs(self.bomb.obj.position() - self.GameSnake.body[0].position()) < 14:
                    self.GameSnake.add_length()  # grow the snake
                    self.all_objects.append(self.GameSnake.body[-1])
                    self.bomb.generate(exclusion_list=self.all_objects)
                    self.scoreboard.add_score(amount=int(self.bomb.count_down))
                    self.scoreboard.show_score()
                elif self.bomb.count_down <= 0:
                    self.bomb.generate(exclusion_list=self.all_objects)
                    self.scoreboard.show_score()

        # mines
        if self.scoreboard.scores >= self.stage_3:
            if abs(self.mine.obj.position() - self.GameSnake.body[0].position()) < 14:
                self.mine.detonate()

    def choose_mode(self):
        """Opens window for user to choose controls."""
        self.bomb.pause()
        self.control_mode = int(self.GameScreen.numinput(title="Choose your controls",
                                                                                 prompt="1 to use Left/Right keys \n2 to use Up/Down/Left/Right "
                                                                                        "keys",
                                                                                 minval=1,
                                                                                 maxval=2))
        self.GameSnake.change_controls(set_controls=self.control_mode)
        self.bomb.resume()

    def draw_border(self):
        """a separate turtle draws the game boundaries"""
        border_pen = t.Turtle(visible=False)
        border_pen.penup()
        border_pen.color("white")
        border_pen.goto(self.WIDTH / 2, self.HEIGHT / 2)
        border_pen.down()
        for x in range(0, 2):
            border_pen.right(90)
            border_pen.forward(self.HEIGHT)
            border_pen.right(90)
            border_pen.forward(self.WIDTH)

    def calibrate_level(self):
        if self.scoreboard.scores >= self.stage_2:
            if not self.bomb.obj.isvisible():
                self.show_rules()
                self.bomb.start_obj(exclude=self.all_objects)
                self.all_objects.append(self.bomb.obj)
            self.bomb.animate()
            self.bomb.tracker()
            if self.scoreboard.scores >= self.stage_3:
                if not self.mine.obj.isvisible():
                    self.show_rules()
                    self.mine.start_obj(exclude=self.all_objects)
                    self.all_objects.append(self.mine.obj)
                self.mine.animate()
                if self.scoreboard.scores >= self.stage_4 and not self.stage_lock:
                    self.stage_lock = True
                    self.show_rules()

    def close_loading(self):
        self.loading = False

    def show_rules(self):
        self.hide_all()
        rule1 = ["Eat the white squares to earn points", ]
        # f"New rules past {self.stage_2} points!"]
        rule2 = ["Catch the red bombs under 10 seconds",
                 "Retrieve the yellow bomb early to win extra points!"]
        # f"New rules past {self.stage_3} points!"]
        rule3 = ["Avoid the purple spikes, they spawn with the white squares", ]
        # f"New rules past {self.stage_4} points!"]
        rule4 = ["Eating the red bombs makes you darker",
                 "Pick the white squares to regain whiteness"]
        guidebook = {
            self.stage_2: rule2,
            self.stage_3: rule3,
            self.stage_4: rule4,
        }
        disclosure = rule1
        for x in guidebook:
            if self.scoreboard.scores >= x:
                # del disclosure[-1]
                # disclosure.extend(guidebook[x])
                disclosure = guidebook[x]
        self.messenger.scribble(0, 0, "white", 10, *disclosure)
        self.GameScreen.update()
        time.sleep(4)
        self.messenger.remove()
        self.hints()
        self.show_all()

    def hide_all(self):
        self.GameSnake.hide()
        self.feed.hide()
        self.bomb.hide()
        self.mine.hide()
        self.bomb.timekeeper.hideturtle()

    def show_all(self):
        self.GameSnake.show()
        self.feed.show()
        if self.scoreboard.scores > self.stage_2:
            self.bomb.show()
            if self.scoreboard.scores > self.stage_3:
                self.mine.show()

    def hints(self):
        self.messenger.generate(prompts=f"Press C to change controls      Press R to check the rules", x=0,
                                y=-self.HEIGHT / 2 + 10, color="grey",
                                size=10)

    def condition_dead(self):
        if self.GameSnake.check_collision() or self.bomb.timeout or self.mine.exploded:
            self.feed.hide()
            self.bomb.hide()
            self.mine.hide()
            self.messenger.remove()
            self.scoreboard.remove()
            t.update()
            return True


# TODO: time bomb and mine still overlaps
my_Game = Game()
my_Game.title_card()
my_Game.start_game()

# my_Game.GameScreen.mainloop()
