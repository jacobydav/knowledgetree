import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound('/home/rpi/Documents/knowledgetree/sounds/snore_x.wav')
playing = sound.play()
while playing.get_busy():
    pygame.time.delay(100)