from gpiozero import Button
from gpiozero.pins.lgpio import LGPIOFactory
from time import sleep
import pygame
import pygame._sdl2.audio as sdl2_audio
import cv2

my_factory = LGPIOFactory()
button = Button(17, pin_factory=my_factory)
pygame.init()
#Get a list of available audio devices
audio_devices = sdl2_audio.get_audio_device_names(False)
print(audio_devices)
#Start pygame
pygame.mixer.init(devicename='UE MINI BOOM')
sound = pygame.mixer.Sound('/home/rpi/Documents/knowledgetree/sounds/snore_x.wav')

while True:
    if button.is_pressed:
        print("Pressed")
        playing = sound.play()
        while playing.get_busy():
            pygame.time.delay(100)
        break
    else:
        print("Released")
    sleep(1)
        
print("Program end")
pygame.mixer.stop()
pygame.mixer.quit()
pygame.quit()
button.close()
my_factory.close()
