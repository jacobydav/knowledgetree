import gpiod
import time

from gpiod.line import Direction
from gpiod.line import Bias,Edge,Value

import pygame

def get_line_value(chip_path, line_offset):
    with gpiod.request_lines(
        chip_path,
        consumer="get-line-value",
        config={line_offset: gpiod.LineSettings(direction=Direction.INPUT,bias=Bias.PULL_UP)},
    ) as request:
        value = request.get_value(line_offset)
        print("{}={}".format(line_offset, value))
        return value


if __name__ == "__main__":
    try:
        pygame.mixer.init()
        sound = pygame.mixer.Sound('/home/rpi/Documents/knowledgetree/sounds/snore_x.wav')
        LOOPS = 200
        for i in range(LOOPS):
            btn_state = get_line_value("/dev/gpiochip0", 17)
            if btn_state == Value.INACTIVE:
                print("Button pressed")
                playing = sound.play()
                while playing.get_busy():
                    pygame.time.delay(100)

            time.sleep(1)
    except OSError as ex:
        print(ex, "\nCustomise the example configuration to suit your situation")


