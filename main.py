from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from random import randint
from kivy.graphics import Color, Rectangle

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1
            ball.change_color()

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    color = Color(1, 0, 0, 1)  # Initial color (red)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def change_color(self):
        self.color = Color(0, 1, 0, 1)  # Change color to green when hit

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    game_over = False

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        if not self.game_over:
            self.ball.move()

            # Bounce off top and bottom
            if (self.ball.y < 0) or (self.ball.y > self.height - 50):
                self.ball.velocity_y *= -1

            # Bounce off left and increase the score for player 2
            if self.ball.x < 0:
                self.ball.velocity_x *= -1
                self.player2.score += 1
                self.ball.change_color()  # Change color when it hits the paddle

            # Bounce off right and increase the score for player 1
            if self.ball.x > self.width - 50:
                self.ball.velocity_x *= -1
                self.player1.score += 1
                self.ball.change_color()  # Change color when it hits the paddle

            self.player1.bounce_ball(self.ball)
            self.player2.bounce_ball(self.ball)

            # Check if the game should end
            if self.player1.score >= 20 or self.player2.score >= 20:
                self.game_over = True
                self.declare_winner()

    def declare_winner(self):
        winner = "Player 1" if self.player1.score > self.player2.score else "Player 2"
        print(f"Game over! {winner} wins with a score of {max(self.player1.score, self.player2.score)}")

    def on_touch_move(self, touch):
        if touch.x < self.width * 1 / 4.0:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3 / 4.0:
            self.player2.center_y = touch.y

    def on_size(self, *args):
        # Update the background color when the size of the widget changes
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Background color (gray)
            Rectangle(pos=self.pos, size=self.size)

class PongApp(App):
    title = "Zux PingPong"  # Change the game name here

    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
