import pygame
import numpy as np

WINDOW_SIZE = (1000,1000)
GRID = (10,10)
SQUARE_SIZE = min(WINDOW_SIZE[0]//(GRID[0]+1)-5,WINDOW_SIZE[1]//(GRID[1]+1)-5)

select_card = False
card_image = None


# Draw back of cards
class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        # init as pygame.sprite.Sprite
        super().__init__()

        self.original_image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, color, pygame.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE))

        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.clicked = False

    def update(self, event_list, new_image=None):

        if new_image != None and self.clicked:
            self.clicked = False
            self.image = new_image

        # On click change the status of the picture
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked
                    global select_card
                    select_card = True
                    return None
        return new_image


# Draw cards from pictures
class SpriteObject3(pygame.sprite.Sprite):
    def __init__(self, x, y, img_path):
        # init as pygame.sprite.Sprite
        super().__init__()

        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect(center = (x, y))

    def update(self, event_list, new_image=None):
        # On click change the status of the picture
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    global select_card, card_image
                    select_card = False
                    card_image = self.image



# Start game
pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# define coordinates
dx = window.get_width() // (GRID[0]+1)
dy = window.get_height() // (GRID[1]+1)

# Prepare grid of cards
tiles = []
def game_reset():
    global tiles,group,select_card
    tiles = []
    for px in range(GRID[0]):
        for py in range(GRID[1]):
            tiles += [SpriteObject(dx*(px+1), dy*(py+1), (128, 0, 0))]
    select_card = False

# Prepare grid of images to select
tiles2 = []
pic_n = 1
for px in range(4):
    for py in range(4):
        img_path = f'./imgs/pic{pic_n:02d}.png'
        tiles2 += [SpriteObject3(dx*(px+5), dy*(py+5), img_path)]
        pic_n += 1

#tiles = [
#    SpriteObject(dx, dy, (128, 0, 0)),
#    SpriteObject(2*dx, dy, (0, 128, 0)),
#    SpriteObject(dx, 2*dy, (0, 0, 128)),
#    SpriteObject(2*dx, 2*dy, (128, 128, 0)),
#    tt
#]

#tiles2 = [
#    SpriteObject2(dx, dy, (128, 0, 0)),
#    SpriteObject2(2*dx, dy, (0, 128, 0)),
#    SpriteObject2(dx, 2*dy, (0, 0, 128)),
#    SpriteObject2(2*dx, 2*dy, (128, 128, 0))
#]


game_reset()
run = True
new_image = None
while run:
    clock.tick(60)

    if select_card:
        group = pygame.sprite.Group(tiles2)
    else:
        group = pygame.sprite.Group(tiles)

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_reset()
            if event.key == pygame.K_q:
                run = False


    group.update(event_list,card_image)

    window.fill(0)
    group.draw(window)
    pygame.display.flip()

pygame.quit()
exit()
