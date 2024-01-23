import pygame
from pygame import mixer
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
light_gray = (170, 170, 170)
blue = (0, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
gold = (212, 175, 55)
WIDTH = 360
HEIGHT = 640
active_length = 0
active_beat = 0

# sounds
'''
hi_hat = mixer.Sound('sounds\kit2\hi hat.wav')
snare = mixer.Sound('sounds\kit2\snare.wav')
kick = mixer.Sound('sounds\kit2\kick.wav')
crash = mixer.Sound('sounds\kit2\crash.wav')
clap = mixer.Sound('sounds\kit2\clap.wav')
tom = mixer.Sound("sounds\kit2\\tom.wav")
'''
metro = mixer.Sound("sounds\metronome.wav")
metro1st = mixer.Sound("sounds\\netronome.wav")
hi_hat = mixer.Sound("sounds\hi hat.wav")
snare = mixer.Sound("sounds\snare.wav")
kick = mixer.Sound("sounds\kick.wav")
crash = mixer.Sound("sounds\crash.wav")
clap = mixer.Sound("sounds\clap.wav")
tom = mixer.Sound("sounds\\tom.wav")

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Moja perkusja')
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
medium_font = pygame.font.Font('Roboto-Bold.ttf', 24)
beat_changed = True
timer = pygame.time.Clock()
fps = 60
BEATS = 4
bpm = 240
instruments = 6
playing = True
pygame.mixer.set_num_channels(instruments * 3)

m_boxes = []
for i in range(4):
    r = pygame.Rect(i * 40 + 40, 60, 20, 80)
    m_boxes.append(r)


def draw_grid(active):
    for i in range(4):
        if active == 0 and i == 0:
            color = red
        elif active == i:
            color = green
        else:
            color = gray
        pygame.draw.rect(screen, color, m_boxes[i], 0, 2)


def metronom():
    metro.play()


def bpm_box():
    bpm_rect = pygame.draw.rect(screen, gray, [206, 60, 114, 80],0, 2)
    bpm_text1 = medium_font.render('BPM', True, gray)
    screen.blit(bpm_text1, (204, 35))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (238, 95))
    bpm_add_circle = pygame.draw.circle(screen, gray, [236, 168], 16, 0)
    bpm_sub_circle = pygame.draw.circle(screen, gray, [288, 168], 16, 0)
    add_text = medium_font.render('+5', True, white)
    screen.blit(add_text, (520, HEIGHT - 140))
    sub_text = medium_font.render('-5', True, white)
    screen.blit(sub_text, (520, HEIGHT - 90))



def bpl_box():
    # beats per loop buttons
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (612, HEIGHT - 130))
    beats_text2 = label_font.render(f'{BEATS}', True, white)
    screen.blit(beats_text2, (670, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, white)
    screen.blit(add_text2, (820, HEIGHT - 140))
    sub_text2 = medium_font.render('-1', True, white)
    screen.blit(sub_text2, (820, HEIGHT - 90))


def play_pause():
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))


run = True
while run:
    timer.tick(fps)     # zatrzymuje dzialanie programu do 1/60 sek
    screen.fill(black)

    draw_grid(active_beat)
    bpm_box()

    if beat_changed:
        metronom()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    beat_length = 3600 // bpm   # bpm = beats per minute - 240 beat_lenth = 15 fps-ow czyli 1/4 sekundy zgadza sie

    if playing:
        if active_length < beat_length:     # to gra dzwiek przez beat_lenght
            active_length += 1
        else:
            active_length = 0
            if active_beat < BEATS - 1:     # beats = 4
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

pygame.quit()
