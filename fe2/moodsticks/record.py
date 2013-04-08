#!/usr/bin/env python

#!/usr/bin/env python
#-*- coding: utf-8 -*-

##
## record.py - record.
##
## Copyright (c) 2013-2014 Willem Jan Faber
##
## this program is free software: you can redistribute it and/or modify
## it under the terms of the gnu general public license as published by
## the free software foundation, either version 3 of the license, or
## (at your option) any later version.
##
## this program is distributed in the hope that it will be useful,
## but without any warranty; without even the implied warranty of
## merchantability or fitness for a particular purpose. see the
## gnu general public license for more details.
##
## you should have received a copy of the gnu general public license
## along with this program. if not, see <http://www.gnu.org/licenses/>.
##


from leds import LED_controll

import random
import time
import analyse
import pyaudio
import numpy
import sys


from ctypes import *


chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
RECORD_SECONDS = 0.2

def record_sample():
    # This basicly is the record.py as found in the example directory for pyaudio

    #<stackoverflow>
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    def py_error_handler(filename, line, function, err, fmt):
        pass
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    #</stackoverflow>

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        input_device_index = 1,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)
    except:
        time.sleep(0.1)
        return
    raw_sample = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        try:
            data = stream.read(chunk)
            raw_sample.append(data)
        except:
            time.sleep(0.1)
            pass
	stream.stop_stream()
	stream.close()
	p.terminate()
	return(raw_sample)


def main():
    volume_array = []
    prev_state = "down"
    l = LED_controll()
    while True:
        raw_sample_data = record_sample()
        base_volume_established = False
        if raw_sample_data:
            for raw_sample in raw_sample_data:
                sample = numpy.fromstring(raw_sample, dtype=numpy.int16)
		vol = analyse.loudness(sample)
		if vol > -14:
                	volume_array.append(analyse.loudness(sample))
			print(vol)

            if len(volume_array) > 10:
                base_volume_established = True

            if base_volume_established:
                for i in range(0, len(volume_array) - 10):
                    volume_array.pop(0)
                current_input = [int(abs(i - sum(volume_array)/10)*10) for i in volume_array if i < 19]

                if current_input[0] > current_input[9] and current_input[0] > current_input[4] and not prev_state == "up" and current_input[0]-current_input[4] > 3:
                    print('up', current_input[4]-current_input[0])
                    prev_state = "up"
                    l.spaceship_min()
                    if current_input[0]-current_input[4] > 4:
                        l.flip_painting()
                    if current_input[0]-current_input[4] > 6:
                        l.flip_robot()
                        l.painting_min(2, rnd=0.9)
                        l.spaceship_min()

                if current_input[0] < current_input[9] and current_input[0] < current_input[4] and not prev_state == "down" and current_input[4]-current_input[0] > 3:
                    print('down', current_input[0]-current_input[4])
                    prev_state = "down"
                    l.spaceship_min()
                    if current_input[4]-current_input[0] > 4:
                        l.flip_painting()
                    if current_input[4]-current_input[0] > 6:
                        l.flip_robot()
                        l.painting_min(2, rnd=0.9)
                        l.spaceship_min()

                if current_input[0] < current_input[9] and current_input[0] < current_input[4]:
                    prev_state = "down"
                if current_input[0] > current_input[9] and current_input[0] > current_input[4]:
                    prev_state = "up"


                if abs(current_input[-1] - current_input[-2]) > 2:
                    if random.random() < 0.5:
                        l.spaceship_min(2, s=0.002, rnd=0.3)
                    else:
                        l.spaceship_max(2, s=0.002, rnd=0.9)
                if current_input[-1] > 20:
                    if random.random() > 0.5:
                        l.painting_max(rnd=0.8)
                    else:
                        l.spaceship_max(rnd=0.8)
                if current_input[-1] > 40:
                    l.painting_max()
                    l.spaceship_max()
                if current_input[-1] > 47:
                    for i in range(40):
                        l.flip_robot()

if __name__ == '__main__':
    main()
