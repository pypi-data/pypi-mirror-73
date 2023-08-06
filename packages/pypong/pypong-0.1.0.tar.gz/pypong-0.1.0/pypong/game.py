from os import path
from random import randint

import pygame

TITLE = 'PyPONG'
WIDTH, HEIGHT = 800, 600
WIN_SIZE = (WIDTH, HEIGHT)
BLOCK = 20
HALF_BLOCK = BLOCK / 2
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TOP = 0
BOTTOM = HEIGHT
MID_WIDTH = WIDTH / 2
MID_HEIGHT = HEIGHT / 2
ASSETS_PATH = path.join(path.dirname(__file__), 'assets')
FONT = path.join(ASSETS_PATH, 'font', 'Teko-Regular.ttf')
SFX = path.join(ASSETS_PATH, 'sfx')


class Paddle(pygame.sprite.Sprite):
    def __init__(self, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((HALF_BLOCK, BLOCK * 3))
        image.fill(WHITE)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        if self.rect.y < TOP:
            self.rect.y = TOP
        elif self.rect.y > (BOTTOM - self.rect.height):
            self.rect.y = BOTTOM - self.rect.height


class Cpu(Paddle):
    def __init__(self, game, *args, **kwargs):
        position = (WIDTH - BLOCK * 2, HEIGHT / 2)
        super().__init__(position, *args, **kwargs)
        self.game = game

    def update(self):
        if self.game.ball.velocity.x > 0:
            diff = self.rect.centery - self.game.ball.rect.centery
            if diff != 0:
                speed = self.game.ball.velocity.x % abs(diff)
                speed = -speed if diff > 0 else speed
                self.rect.centery += speed
        super().update()


class Player(Paddle):
    def __init__(self, *args, **kwargs):
        position = (BLOCK * 2, HEIGHT / 2)
        super().__init__(position, *args, **kwargs)

    def update(self):
        _, y = pygame.mouse.get_pos()
        bottom = HEIGHT - self.rect.height
        self.rect.y = bottom if y > bottom else y
        super().update()


class Ball(pygame.sprite.Sprite):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((BLOCK, BLOCK))
        image.fill(BLACK)
        image.set_colorkey(BLACK)
        pygame.draw.circle(image, WHITE, (HALF_BLOCK, HALF_BLOCK), HALF_BLOCK)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (MID_WIDTH, HEIGHT / 2)
        self.radius = HALF_BLOCK
        self.velocity = pygame.Vector2(randint(23, 28), randint(-6, 6))
        self.game = game
        self.last_hit = 0

    def update(self):
        if self.rect.top <= TOP:
            self.rect.top = TOP
            self.velocity.y *= -1
            self.game.sfx['wall'].play()
        elif self.rect.bottom >= BOTTOM:
            self.rect.bottom = BOTTOM
            self.velocity.y *= -1
            self.game.sfx['wall'].play()
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.hit()
        self.out()

    def bounce(self):
        velocityx = randint(23, 28)
        self.velocity.x = -velocityx if self.velocity.x > 0 else velocityx
        self.velocity.y = randint(-6, 6)
        self.game.sfx['bounce'].play()

    def hit(self):
        hits = pygame.sprite.spritecollide(
            self,
            self.game.paddles,
            False,
            pygame.sprite.collide_rect_ratio(0.85),
        )
        if hits:
            now = pygame.time.get_ticks()
            elapsed_time = now - self.last_hit
            if elapsed_time > 500:
                self.last_hit = now
                self.bounce()
            paddle = hits.pop()
            if isinstance(paddle, Player):
                if (
                    self.rect.left < paddle.rect.right
                    and self.rect.top >= paddle.rect.top
                    and self.rect.bottom <= paddle.rect.bottom
                ):
                    self.rect.left = paddle.rect.right
            else:
                if (
                    self.rect.right > paddle.rect.left
                    and self.rect.top >= paddle.rect.top
                    and self.rect.bottom <= paddle.rect.bottom
                ):
                    self.rect.right = paddle.rect.left

    def out(self):
        player_scored = self.rect.x >= (WIDTH - self.rect.width)
        cpu_scored = self.rect.x <= 0
        if player_scored or cpu_scored:
            self.kill()
            self.game.score(player=int(player_scored), cpu=int(cpu_scored))
            self.game.sfx['missed'].play()


class Net(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface((2, HEIGHT))
        image.fill(BLACK)
        image.set_colorkey(BLACK)
        points = tuple(range(0, HEIGHT, 10))
        coords = ((points[i], points[i + 1]) for i in range(len(points) - 1))
        for i, coord in enumerate(coords):
            if i % 2 != 0:
                start, end = coord
                pygame.draw.line(image, WHITE, (0, start), (0, end), 2)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.midtop = (MID_WIDTH, 0)


class Score(pygame.sprite.Sprite):
    def __init__(self, value, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = pygame.font.Font(FONT, 80)
        self.value = value
        self.position = position

    def update(self):
        self.image = self.font.render(str(self.value), True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.midtop = self.position


class SplashScreen(pygame.sprite.Sprite):
    def __init__(self, text=TITLE, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface(WIN_SIZE)
        image.fill(BLACK)
        image.set_colorkey(BLACK)

        font_big = pygame.font.Font(FONT, 80)
        title = font_big.render(text, True, WHITE)
        title_rect = title.get_rect()
        title_rect.midbottom = (MID_WIDTH, MID_HEIGHT)
        image.blit(title, title_rect)

        font_small = pygame.font.Font(FONT, 30)
        hint = font_small.render('Press any key to play', True, WHITE)
        hint_rect = hint.get_rect()
        hint_rect.midtop = (MID_WIDTH, MID_HEIGHT)
        image.blit(hint, hint_rect)

        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()
        self.sfx = {
            sound: pygame.mixer.Sound(path.join(SFX, f'{sound}.wav'))
            for sound in ('bounce', 'missed', 'wall')
        }

    def reset(self):
        self.sprites.empty()
        self.paddles.empty()
        self.net = Net((self.sprites,))
        self.score_left = Score(0, (WIDTH * 0.25, 50), (self.sprites))
        self.score_right = Score(0, (WIDTH * 0.75, 50), (self.sprites))
        self.player = Player((self.sprites, self.paddles))
        self.cpu = Cpu(self, (self.sprites, self.paddles))
        self.serve()
        self.splash_screen = None

    def start(self):
        self.sprites.empty()
        self.splash_screen = SplashScreen(TITLE, (self.sprites,))
        self.running = True

    def over(self):
        if self.score_left.value == 11 or self.score_right.value == 11:
            self.sprites.empty()
            self.splash_screen = SplashScreen('GAME OVER', (self.sprites,))
            return True

    def score(self, player=0, cpu=0):
        self.score_left.value += player
        self.score_right.value += cpu
        self.over() or self.serve()

    def serve(self):
        self.ball = Ball(self, (self.sprites,))

    def update(self):
        self.sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if self.splash_screen:
                    self.reset()
                    return

    def loop(self):
        while self.running:
            self.clock.tick(FPS)
            self.update()
            self.draw()
            self.events()

    def run(self):
        self.start()
        self.loop()
        pygame.quit()


def main():
    Game().run()


if __name__ == '__main__':
    main()
