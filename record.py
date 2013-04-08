#!/usr/bin/env python
#-*- coding: utf-8 -*-

##
## moodstick.py - moodstick.
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


"""
PyAudio example:
Record a few seconds of audio and save to a WAVE file.
"""


from fe2.mood import leds.LED_controll

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
WAVE_OUTPUT_FILENAME = "output.wav"

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
        return
    raw_sample = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        try:
            data = stream.read(chunk)
            raw_sample.append(data)
        except:
            pass
	stream.stop_stream()
	stream.close()
	p.terminate()
	return(raw_sample)


volume_array = []
for i in range(1000):
    raw_sample_data = record_sample()
    time.sleep(0.2)

    base_volume_established = False

    if raw_sample_data:
        for raw_sample in raw_sample_data:
            sample = numpy.fromstring(raw_sample, dtype=numpy.int16)
            volume_array.append(analyse.loudness(sample))

        if len(volume_array) > 10:
            base_volume_established = True

        if base_volume_established:


