
import sys, pygame
import time, random
import threading

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


SCORE_HIT_TOP_WALL = 75
SCORE_HIT_SIDE_WALL = 5
SCORE_HIT_PADDLE = 175

BACKGROUND_COLOR = (46, 52, 64)

SCORE_BOARD_TEXT_COLOR = (255, 255, 255)
SCORE_BOARD_FONT_SIZE = 24

PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
PADDLE_X_MOVE_AMOUNT = 10

PADDLE_COLOR = (255, 255, 255)
BALL_FILL_COLOR = (255, 255, 255)
BALL_BORDER_COLOR = (0, 0, 0)

BALL_INITIAL_MOVEMENT_XRANGE = -3, 3
BALL_INITIAL_MOVEMENT_YRANGE = -6, -4

BALL_BOUNCE_REDUCTION_FACTOR = 8
BALL_MOVEMENT_INCREASE_TIME = 1000
BALL_MOVEMENT_INCR_LIMIT = 2.5
BALL_MOVEMENT_INCR = 0.025

BALL_RADIUS = 4

FPS = 60
fpsClock = pygame.time.Clock()

class Utils:

    @staticmethod
    def getMiddlePosition():
        return [int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)]

    @staticmethod
    def getMiddleXPosition():
        return int(SCREEN_WIDTH / 2)

    @staticmethod
    def getRandomDirection():
        directions = ['right', 'left', 'down', 'up']
        initialDirection = directions[random.randint(0, 3)]
        return initialDirection

    @staticmethod
    def sign(n):
        if n<0:
            return -1
        elif n>0:
            return 1
        else: 0

class Sound:


    @staticmethod
    def init():
        Sound.SND_BALL_HIT_WALL = pygame.mixer.Sound("ballhitwall.wav")
        Sound.SND_BALL_HIT_PADDLE = pygame.mixer.Sound("ballhitpaddle.wav")

        Sound.SND_GAME_OVER = pygame.mixer.Sound("gameover.wav")
        Sound.SND_GAME_MUSIC = pygame.mixer.Sound("gamemusic.wav")

    @staticmethod
    def playBallHitWallSound():
        pygame.mixer.Sound.play(Sound.SND_BALL_HIT_WALL)
        pygame.mixer.music.stop()

    @staticmethod
    def playBallHitPaddleSound():
        pygame.mixer.Sound.play(Sound.SND_BALL_HIT_PADDLE)
        pygame.mixer.music.stop()

    @staticmethod
    def playGameOver():
        pygame.mixer.Sound.play(Sound.SND_GAME_OVER)
        pygame.mixer.Sound.set_volume(Sound.SND_GAME_OVER, 0.4)
        pygame.mixer.music.stop()

    @staticmethod
    def playGameMusic():
        pygame.mixer.stop()
        pygame.mixer.Sound.play(Sound.SND_GAME_MUSIC, -1)
        pygame.mixer.Sound.set_volume(Sound.SND_GAME_MUSIC, 0.6)
        pygame.mixer.music.stop()

class Scoreboard:

    @staticmethod
    def init():
        Scoreboard.score = 0
        Scoreboard.text = "Score: " + str(Scoreboard.score)

    @staticmethod
    def addScore(scoreAmount):
        Scoreboard.score += scoreAmount
        Scoreboard.text = "Score: " + str(Scoreboard.score)

class Renderer:

    @staticmethod
    def __drawBackground():
        screen.fill(BACKGROUND_COLOR)

    @staticmethod
    def __drawScoreboard():
        font = pygame.font.SysFont(None, SCORE_BOARD_FONT_SIZE)
        img = font.render(Scoreboard.text, True, SCORE_BOARD_TEXT_COLOR)
        screen.blit(img, (5, 8))

    @staticmethod
    def __drawPaddle():
        paddle = Paddle.paddle
        paddleRect = pygame.Rect((paddle.position[0],
                                paddle.position[1],
                                paddle.width, paddle.height))
        pygame.draw.rect(screen, PADDLE_COLOR, paddleRect)

    @staticmethod
    def __drawCircle():
        ball = Ball.ball
        pygame.draw.circle(screen, BALL_FILL_COLOR,
                           ball.position, ball.radius, 0)

    @staticmethod
    def draw():

        Renderer.__drawBackground()
        Renderer.__drawPaddle()
        Renderer.__drawCircle()
        Renderer.__drawScoreboard()

class Ball:

    def __init__(self, pos, movement=[0,0], radius=BALL_RADIUS):
        self.position = pos
        self.radius = radius
        self.movementFactor = 1
        self.originalMovement = [movement[0],movement[1]]
        self.movement = [movement[0],movement[1]]

    def update(self):
        self.position[0] += self.movement[0]
        self.position[1] += self.movement[1]

class Paddle:

    def __init__(self, pos):
        self.position = pos
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.direction = 'none'

    def update(self):
        if self.direction == 'right':
            self.position[0] += PADDLE_X_MOVE_AMOUNT
        elif paddle.direction == 'left':
            self.position[0] += -PADDLE_X_MOVE_AMOUNT


class GameWorld:

    @staticmethod
    def init():

        Sound.init()
        Scoreboard.init()

        Ball.ball = Ball(Utils.getMiddlePosition(), [random.randint(BALL_INITIAL_MOVEMENT_XRANGE[0], BALL_INITIAL_MOVEMENT_XRANGE[1]),
                                                     random.randint(BALL_INITIAL_MOVEMENT_YRANGE[0], BALL_INITIAL_MOVEMENT_YRANGE[1])])
        Paddle.paddle = Paddle([Utils.getMiddleXPosition()-PADDLE_WIDTH/2, SCREEN_HEIGHT-PADDLE_HEIGHT*2])

        Sound.playGameMusic()


    @staticmethod
    def reset():
        Scoreboard.init()

        del Paddle.paddle
        del Ball.ball

        Paddle.paddle = Paddle([Utils.getMiddleXPosition() - PADDLE_WIDTH / 2, SCREEN_HEIGHT - PADDLE_HEIGHT * 2])
        Ball.ball = Ball(Utils.getMiddlePosition(), [random.randint(BALL_INITIAL_MOVEMENT_XRANGE[0], BALL_INITIAL_MOVEMENT_XRANGE[1]),
                                                     random.randint(BALL_INITIAL_MOVEMENT_YRANGE[0], BALL_INITIAL_MOVEMENT_YRANGE[1])])


        Sound.playGameMusic()


    @staticmethod
    def quit():
        return None

    @staticmethod
    def update():

        paddle = Paddle.paddle
        ball = Ball.ball
        paddle.update()
        ball.update()

        if paddle.position[0] <= 0:
            paddle.position[0] = 1
        elif paddle.position[0] + paddle.width >= SCREEN_WIDTH:
            paddle.position[0] = SCREEN_WIDTH - paddle.width - 1

        if ball.position[0]-ball.radius <= 0:
            ball.position[0] = ball.radius+1
            ball.movement[0] *= -1
            Scoreboard.addScore(SCORE_HIT_SIDE_WALL)
            Sound.playBallHitWallSound()
        elif ball.position[0]+ball.radius >= SCREEN_WIDTH:
            ball.position[0] = SCREEN_WIDTH-ball.radius-1
            ball.movement[0] *= -1
            Scoreboard.addScore(SCORE_HIT_SIDE_WALL)
            Sound.playBallHitWallSound()
        elif ball.position[1]-ball.radius <= 0:
            ball.position[1] = ball.radius+1
            ball.movement[1] *= -1
            Scoreboard.addScore(SCORE_HIT_TOP_WALL)
            Sound.playBallHitWallSound()
        elif ball.position[1] > SCREEN_HEIGHT + ball.radius * 15:
            GameWorld.reset()
            Sound.playGameOver()
            return None

        if ball.position[1]+ball.radius>=paddle.position[1] and \
                ball.position[0]+ball.radius >= paddle.position[0] and \
                ball.position[0]-ball.radius <= paddle.position[0]+paddle.width and \
                ball.position[1]+ball.radius<=paddle.position[1]+paddle.height*2:

            Sound.playBallHitPaddleSound()

            if ball.position[0] < paddle.position[0]+paddle.width/2:
                maxval = abs(ball.position[0] - (paddle.position[0] + paddle.width / 2)) / BALL_BOUNCE_REDUCTION_FACTOR
                ball.movement[0] = -maxval * ball.movementFactor
            elif ball.position[0] >= paddle.position[0]+paddle.width/2:
                maxval = abs(((paddle.position[0] + paddle.width / 2) - ball.position[0])) / BALL_BOUNCE_REDUCTION_FACTOR
                ball.movement[0] = maxval * ball.movementFactor

            ball.movement[1] *= -1
            ball.position[1] = paddle.position[1]-ball.radius-1
            Scoreboard.addScore(SCORE_HIT_PADDLE)


if __name__ == '__main__':
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Wall Pong")

    prev_time = time.time()

    GameWorld.init()

    EVENT_BALL_INCR = pygame.USEREVENT + 1
    pygame.time.set_timer(EVENT_BALL_INCR, BALL_MOVEMENT_INCREASE_TIME, 999999)

    running = True
    while running:

        paddle = Paddle.paddle
        ball = Ball.ball

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENT_BALL_INCR:
                ball.movementFactor += BALL_MOVEMENT_INCR
                if ball.movementFactor > BALL_MOVEMENT_INCR_LIMIT:
                    ball.movementFactor = BALL_MOVEMENT_INCR_LIMIT
                ball.movement[1] = Utils.sign(ball.movement[1]) * abs(ball.originalMovement[1]) * ball.movementFactor

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and paddle.direction is not 'right':
            paddle.direction = 'left'
        elif keys[pygame.K_RIGHT] and paddle.direction is not 'left':
            paddle.direction = 'right'
        else:
            paddle.direction = 'none'

        GameWorld.update()
        Renderer.draw()

        pygame.display.flip()
        fpsClock.tick(FPS)

    GameWorld.quit()
