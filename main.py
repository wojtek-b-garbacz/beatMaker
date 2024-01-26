import pygame
from pygame import mixer
from pygame import midi

# midi.midis2events()

pygame.init()
pygame.midi.init()

input_device = pygame.midi.Input(pygame.midi.get_default_input_id())
# input_device = int(pygame.midi.get_default_input_id())
print(input_device.device_id)

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
light_gray = (170, 170, 170)
blue = (0, 255, 255)
red = (204, 51, 0)
green = (77, 153, 0)
gold = (212, 175, 55)
WIDTH = 360
HEIGHT = 640
active_length = 0
active_beat = 0
metro_on = True

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Moja perkusja')
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
medium_font = pygame.font.Font('Roboto-Bold.ttf', 24)
small_font = pygame.font.Font('Roboto-Bold.ttf', 16)

bpm_add1_rect = pygame.Rect(160, 60, 30, 30)
bpm_add5_rect = pygame.Rect(160, 110, 30, 30)
bpm_sub1_rect = pygame.Rect(290, 60, 30, 30)
bpm_sub5_rect = pygame.Rect(290, 110, 30, 30)

bpm_rect = pygame.Rect(200, 60, 80, 80)
midi_rect = pygame.Rect(20,300,320,40)

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
    r = pygame.Rect(i * 30 + 40, 60, 20, 80)
    m_boxes.append(r)


def draw_grid(active):
    for i in range(4):
        if active == 0 and i == 0:
            color = red
        elif active == i:
            color = green
        else:
            color = gray
        pygame.draw.rect(screen, color, m_boxes[i])  # , 0, 2)


def metronom():
    metro.play()
    # metro.play()


def bpm_box():
    # bpm_rect = pygame.draw.rect(screen, gray, [200, 60, 80, 80],0, 2)
    if metro_on:
        pygame.draw.rect(screen, green, bpm_rect)
        add_text = medium_font.render('ON', True, light_gray)
        screen.blit(add_text, (222, 106))
    else:
        add_text = medium_font.render('OFF', True, black)
        screen.blit(add_text, (214, 86))

    # bpm_rect = pygame.draw.rect(screen, gray, [200, 60, 80, 80])
    bpm_text1 = medium_font.render('BPM', True, white)
    screen.blit(bpm_text1, (199, 32))
    bpm_text2 = label_font.render(f'{bpm}', True, light_gray)
    screen.blit(bpm_text2, (213, 70))

    pygame.draw.rect(screen, gray, bpm_add1_rect)  # , 0, 2)
    pygame.draw.rect(screen, gray, bpm_add5_rect)  # , 0, 2)
    pygame.draw.rect(screen, gray, bpm_sub1_rect)  # , 0, 2)
    pygame.draw.rect(screen, gray, bpm_sub5_rect)  # , 0, 2)

    add_text = medium_font.render('+1', True, white)
    screen.blit(add_text, (163, 61))
    sub_text = medium_font.render('+5', True, white)
    screen.blit(sub_text, (162, 111))
    add_text = medium_font.render('-1', True, white)
    screen.blit(add_text, (293, 61))
    sub_text = medium_font.render('-5', True, white)
    screen.blit(sub_text, (292, 111))


run = True
while run:
    screen.fill(black)

    draw_grid(active_beat)
    bpm_box()

    pygame.draw.rect(screen, gray, midi_rect)
    midi_text = small_font.render("Dupsko", True, black)
    screen.blit(midi_text, (20, 300))

    if beat_changed:
        # metronom()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_position = pygame.mouse.get_pos()
            if bpm_rect.collidepoint(mouse_position):
                metro_on = not metro_on
            elif bpm_add1_rect.collidepoint(mouse_position):
                bpm += 1
            elif bpm_add5_rect.collidepoint(mouse_position):
                bpm += 5
            elif bpm_sub1_rect.collidepoint(mouse_position):
                bpm -= 1
            elif bpm_sub5_rect.collidepoint(mouse_position):
                bpm -= 5

    # input_device = pygame.midi.Input(pygame.midi.get_default_input_id())
    # print(input_device.device_id)


    if input_device.poll():
        midi_event = pygame.midi.Input.read(input_device, 1)
        #print(midi_event[0])

        # 1 0 0 1- 0 0 1 0 | 0 1 0 0 0 1 0 1 | 0 1 1 0 0 1 0 0
        # on/off - channel | note number     | velocity


        # [[153, 0, 24, 0], 8714]   - snare on
        # [[137, 0, 0, 0], 8714]    - snare off
        # [[153, 50, 1, 0], 24833]  - hiHat on
        # [[137, 50, 0, 0], 24833]  - hiHat off
        # [[153, 38, 127, 0], 38643]- bass on
        # [[137, 38, 0, 0], 38643]  - bass of

        [[status, channel, note, velocity], hwc] = midi_event[0]

        s_count = 0
        h_count = 0
        k_count = 0

        if status == 153:
            if channel == 0:
                s_count += 1
                print("Snare = " + str(s_count))
                snare.play()
            elif channel == 50:
                print("hiHat")
                hi_hat.play()
            elif channel == 38:
                print("Bass")
                kick.play()


    beat_length = 3600 // bpm  # bpm = beats per minute - 240 beat_lenth = 15 fps-ow czyli 1/4 sekundy zgadza sie

    if playing:
        if active_length < beat_length:  # to gra dzwiek przez beat_lenght
            active_length += 1
        else:
            active_length = 0
            if active_beat < BEATS - 1:  # beats = 4
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
    timer.tick(fps)  # zatrzymuje dzialanie programu do 1/60 sek

pygame.quit()
