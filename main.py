import pygame
from pygame import mixer
from pygame import midi

# midi.midis2events()

s_count = 0
h_count = 0
k_count = 0

pygame.init()
pygame.midi.init()

input_device = pygame.midi.Input(pygame.midi.get_default_input_id())
# input_device = int(pygame.midi.get_default_input_id())
print(input_device.device_id)

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

pygame.mixer.set_num_channels(12)

run = True
while run:
    # input_device = pygame.midi.Input(pygame.midi.get_default_input_id())
    # print(input_device.device_id)

    if input_device.poll():
        midi_event = pygame.midi.Input.read(input_device, 1)
        # 1 0 0 1- 0 0 1 0 | 0 1 0 0 0 1 0 1 | 0 1 1 0 0 1 0 0
        # on/off - channel | note number     | velocity

        # [[153, 0, 24, 0], 8714]   - snare on
        # [[137, 0, 0, 0], 8714]    - snare off
        # [[153, 50, 1, 0], 24833]  - hiHat on
        # [[137, 50, 0, 0], 24833]  - hiHat off
        # [[153, 38, 127, 0], 38643]- bass on
        # [[137, 38, 0, 0], 38643]  - bass of

        [[status, channel, note, velocity], hwc] = midi_event[0]

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

pygame.quit()
