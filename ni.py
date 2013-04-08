#!/usr/bin/env python
#-*- coding: utf-8 -*-

##
## ni.py - ni.
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



import RPi.GPIO as GPIO
import time
import random
import sys

WL1=24
WL2=26

ALIEN_LAMP=21
PAINTING=13
ROBOT=15


all_out = [WL1, WL2, ALIEN_LAMP, PAINTING, ROBOT]
GPIO.setmode(GPIO.BOARD)

for item in all_out:
	GPIO.setup(item, GPIO.OUT)

GPIO.output(ROBOT, GPIO.HIGH)
GPIO.output(WL1, GPIO.LOW)
GPIO.output(WL2, GPIO.LOW)
GPIO.output(ALIEN_LAMP, GPIO.HIGH)


def wl(t=0.02):
	r = random.random()
	if r < 0.2:
		GPIO.output(WL1, GPIO.HIGH)
		GPIO.output(WL2, GPIO.HIGH)
		time.sleep(t)
		GPIO.output(WL1, GPIO.LOW)
		GPIO.output(WL2, GPIO.LOW)
		time.sleep(t)
	elif r < 0.4:
		GPIO.output(WL1, GPIO.LOW)
		GPIO.output(WL2, GPIO.LOW)
		time.sleep(t)
		GPIO.output(WL1, GPIO.HIGH)
		GPIO.output(WL2, GPIO.HIGH)
		time.sleep(t)
	elif r < 0.6:
		for i in range(20):
			GPIO.output(WL1, GPIO.HIGH)
			GPIO.output(WL2, GPIO.HIGH)
			time.sleep(t)
			GPIO.output(WL1, GPIO.LOW)
			GPIO.output(WL2, GPIO.LOW)
			time.sleep(t)
	elif r < 0.8:
		for i in range(int(20*random.random())):
			GPIO.output(WL2, GPIO.HIGH)
			GPIO.output(WL1, GPIO.LOW)
			time.sleep(0.09)
			GPIO.output(WL2, GPIO.LOW)
			GPIO.output(WL1, GPIO.HIGH)
			time.sleep(0.09)
		GPIO.output(WL1, GPIO.LOW)
		GPIO.output(WL2, GPIO.LOW)



def painting(t=0.02):
	r = random.random()
	if r < 0.5:
		GPIO.output(PAINTING, GPIO.LOW)
		time.sleep(t)
		GPIO.output(PAINTING, GPIO.HIGH)
		time.sleep(t)
	else:
		for i in range(int(10*random.random())):
			GPIO.output(PAINTING, GPIO.LOW)
			time.sleep(t)
			GPIO.output(PAINTING, GPIO.HIGH)
			time.sleep(t)

def alien_lamp(t=0.02):
	GPIO.output(ALIEN_LAMP, GPIO.LOW)
	time.sleep(t)
	GPIO.output(ALIEN_LAMP, GPIO.HIGH)
	time.sleep(t)


def robot(t=0.02):
	for i in range(int(100*random.random())):
		GPIO.output(ROBOT, GPIO.LOW)
		GPIO.output(ROBOT, GPIO.HIGH)
		time.sleep(t)
		GPIO.output(ROBOT, GPIO.LOW)

for i in range(1,10):
	wl()

for i in range(1, 13):
	painting()

for i in range(1, 13):
	alien_lamp()

for i in range(1, 13):
	robot()

while True:
	r = random.random()

	if r < 0.2:
		wl()
	elif r < 0.3:
		painting()
	elif r < 0.4:
		alien_lamp()
	elif r < 0.5:
		robot()
	elif r < 0.6:
		alien_lamp()
		robot()
	elif r < 0.7:
		painting()
		wl()
	elif r < 0.8:
		painting()
		alien_lamp()
	elif r < 0.9:
		painting()
		robot()
	else:
		r = random.random()
		if r< 0.5:
			r=r/10
			robot(r)
			painting(r)
			alien_lamp(r)
			wl(r)
		else:
			robot()
			painting()
			alien_lamp()
			wl()

	#time.sleep(10/(1+random.random()))
	
