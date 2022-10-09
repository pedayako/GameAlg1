import random
import pygame
def startGame():

    width = 600
    height = 600

    speed = 10.7
    speed_place = 10
    gravity = 1.7

    ground_width = 2 * width
    ground_height = 50

    pipe_width = 100
    pipe_height = 500
    pipe_gap = 100

    score = 0

    class Bird(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.death = False
            self.image_moveBird = [pygame.image.load('assets-FlapyyBird/bluebird-upflap.png').convert_alpha(),
                                   pygame.image.load('assets-FlapyyBird/bluebird-midflap.png').convert_alpha(),
                                   pygame.image.load('assets-FlapyyBird/bluebird-downflap.png').convert_alpha()]

            self.speed = speed
            self.curent_image_moveBird = 0
            self.image = pygame.image.load('assets-FlapyyBird/bluebird-upflap.png').convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect[0] = width/2
            self.rect[1] = height/2

            'print(self.rect)'

        def update(self):
            self.curent_image_moveBird = (self.curent_image_moveBird + 1) % 3
            self.image = self.image_moveBird[self.curent_image_moveBird]
            self.rect[1] += self.speed
            self.speed += gravity
            if self.rect[1] > 1000:
                self.rect[1] = 1000  #527

        def jump(self):
            self.speed = -speed

        def gameOver(self):
            font = pygame.font.Font('assets-FlapyyBird/fontOk.ttf', 70)
            text_surface = font.render('Game Over', True, (255, 255, 255))
            screen.blit(text_surface, dest=((width / 2) - 100, height / 2 - 100))

    class Ground(pygame.sprite.Sprite):
        def __init__(self, xpos):
            pygame.sprite.Sprite.__init__(self)
            self.image_ground = pygame.image.load('assets-FlapyyBird/ground1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image_ground, (ground_width, ground_height))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = height - ground_height

        def update(self):
            self.rect[0] -= speed_place

    class Pipe(pygame.sprite.Sprite):
        def __init__(self, inverted, xpos, ysize):
            pygame.sprite.Sprite.__init__(self)
            self.podepontuar = True
            self.image = pygame.image.load('assets-FlapyyBird/pipe.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (pipe_width, pipe_height))
            self.rect = self.image.get_rect()
            self.rect[0] = xpos

            if inverted:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect[1] = -(self.rect[3] - ysize)

            else:
                self.rect[1] = height - ysize
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            self.rect[0] -= speed_place

    def randomPipes(xpos):
        size = random.randint(100, 400)
        pipe = Pipe(False, xpos, size)
        pipe_inverted = Pipe(True, xpos, height - size - pipe_gap)
        return (pipe, pipe_inverted)

    def offScreen(sprite):
        return sprite.rect[0] < -(sprite.rect[2])

    def gameOver():
        font = pygame.font.Font('assets-FlapyyBird/fontOk.ttf', 65)
        text_surface = font.render('Game Over', True, (255, 255, 255))
        screen.blit(text_surface, dest=((width/2)-100, height/2-100))
        text_surface1 = font.render('Press Space to Start Over', True, (255, 255, 255))
        screen.blit(text_surface1, dest=((width / 2) - 280, height / 2))

    pygame.init()
    pygame.display.set_caption('Flappy Bird')
    screen = pygame.display.set_mode((width, height))
    background = pygame.image.load('assets-FlapyyBird/Background1.png').convert_alpha()
    background = pygame.transform.scale(background, (width, height))

    song_jump = pygame.mixer.music.load('assets-FlapyyBird/Jump.mp3')
    song_point = pygame.mixer.Sound('assets-FlapyyBird/Point.wav')
    song_collide = pygame.mixer.Sound('assets-FlapyyBird/Collide.wav')

    birdGroup = pygame.sprite.Group()
    bird = Bird()
    birdGroup.add(bird)

    pipeGroup = pygame.sprite.Group()
    for i in range(0, 2):
        pipes = randomPipes(width * i + 700)
        pipeGroup.add(pipes[0])
        pipeGroup.add(pipes[1])

    groundGroup = pygame.sprite.Group()
    for i in range(11):
        ground = Ground(ground_width * i - 20)
        groundGroup.add(ground)

    clock = pygame.time.Clock()

    while True:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                    pygame.mixer.music.play(1)
                if event.key == pygame.K_SPACE and bird.death:
                    startGame()

        screen.blit(background, (0, 0))

        if offScreen(groundGroup.sprites()[0]):
            groundGroup.remove(groundGroup.sprites()[0])
            new_ground = Ground(ground_width - 20)
            groundGroup.add(new_ground)

        if offScreen(pipeGroup.sprites()[0]):
            pipeGroup.remove(pipeGroup.sprites()[0])
            pipeGroup.remove(pipeGroup.sprites()[0])
            pipes = randomPipes(width * 2)
            pipeGroup.add(pipes[0])
            pipeGroup.add(pipes[1])

        for i in pipeGroup:
            if i.rect[0] < ((width/2)-75) and i.podepontuar:
                i.podepontuar = False
                score += 1
                speed_place += 0.2
                song_point.play()

        birdGroup.draw(screen)
        groundGroup.draw(screen)
        pipeGroup.draw(screen)

        if (pygame.sprite.groupcollide(birdGroup, groundGroup, False, False) or
            pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False)):
            (bird.death) = True
            #song_collide.play()
            speed = 0
            speed_place = 0
            song_collide.play()

        if bird.death:
            gameOver()

        pygame.font.init()
        font = pygame.font.Font('assets-FlapyyBird/fontOk.ttf', 70)
        text_surface = font.render(str(int(score/2)), True, (255, 255, 255))
        screen.blit(text_surface, dest=(width / 2, 50))

        birdGroup.update()
        pipeGroup.update()
        groundGroup.update()

        pygame.display.update()

startGame()
