#!/usr/bin/env python
#-*- coding: utf-8 -*-

##
## leds.py - leds.
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


from twisted.internet.protocol import Factory, Protocol
from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic


import random
import RPi.GPIO as GPIO
import time

class config():
    ALIEN_LAMP = 21
    PAINTING = 13
    ROBOT = 15

    WL1 = 24
    WL2 = 26
    WL3 = 8

    WL_MIN = [WL3]
    WL_AVG = [WL1, WL2]
    WL_MAX = WL_ALL = [WL1, WL2, WL3]

    PAINTING_MIN = WL_PAINTING = [WL3]
    PAINTING_MAX = [PAINTING, WL3]

    SPACESHIP_MIN = [WL1, WL2]
    SPACESHIP_AVG = [ALIEN_LAMP, ROBOT]
    SPACESHIP_MAX = SPACESHIP_ALL = [ALIEN_LAMP, ROBOT, WL1, WL2]

    ALL_OUT = [ALIEN_LAMP, PAINTING, ROBOT, WL1, WL2, WL3]


class LED_effect():
    def __init__(self, PINS, r=0, s=0.02, rnd=False):
        if type(rnd) == bool and rnd:
            rnd = 0.5

        if not rnd:
            if r:
                for i in range(r):
                    time.sleep(s)
                    for led in PINS:
                        GPIO.output(led, GPIO.HIGH)
                    time.sleep(s)
                    for led in PINS:
                        GPIO.output(led, GPIO.LOW)
            else:
                for led in PINS:
                    GPIO.output(led, GPIO.HIGH)
                time.sleep(s)
                for led in PINS:
                    GPIO.output(led, GPIO.LOW)
        else:
            if r:
                for i in range(r):
                    time.sleep(s)
                    for led in PINS:
                        if random.random() > rnd:
                            GPIO.output(led, GPIO.HIGH)
                    time.sleep(s)
                    for led in PINS:
                        if random.random() > rnd:
                            GPIO.output(led, GPIO.LOW)
            else:
                for led in PINS:
                    if random.random() > rnd:
                        GPIO.output(led, GPIO.HIGH)
                time.sleep(s)
                for led in PINS:
                    if random.random() > rnd:
                        GPIO.output(led, GPIO.LOW)

class LED_controll():
    def __init__(self):
        self.config = config()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        for led in self.config.ALL_OUT:
            GPIO.setup(led, GPIO.OUT)
            print(led)

        self._initial_all_off()

    def _initial_all_off(self):
        for led in self.config.WL_MAX:
            GPIO.output(led, GPIO.LOW)

    def flip_robot(self, s=0.01):
        GPIO.output(self.config.ROBOT, GPIO.HIGH)
        time.sleep(s)
        GPIO.output(self.config.ROBOT, GPIO.LOW)
        time.sleep(s)
        GPIO.output(self.config.ROBOT, GPIO.HIGH)

    def flip_alien_lamp(self):
        GPIO.output(self.config.ALIEN_LAMP, GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(self.config.ALIEN_LAMP, GPIO.LOW)

    def flip_painting(self):
        GPIO.output(self.config.PAINTING, GPIO.HIGH)
        time.sleep(0.02)
        GPIO.output(self.config.PAINTING, GPIO.LOW)

    def spaceship_min(self, r=0, s=0.02, rnd=False):
        LED_effect(self.config.SPACESHIP_MIN, r, s, rnd)

    def spaceship_max(self, r=0, s=0.02, rnd=False):
        LED_effect(self.config.SPACESHIP_MAX, r, s, rnd)

    def painting_min(self, r=0, s=0.02, rnd=False):
        LED_effect(self.config.PAINTING_MIN, r, s, rnd)

    def painting_max(self, r=0, s=0.02, rnd=False):
        LED_effect(self.config.PAINTING_MAX, r, s, rnd)

    def spaceship_wl_off(self):
        for led in self.config.SPACESHIP_MIN:
            GPIO.output(led, GPIO.LOW)

    def painting_wl_off(self):
        for led in self.config.PAINTING_MIN:
            GPIO.output(led, GPIO.LOW)



#
# http://stackoverflow.com/questions/776120/multiple-simultaneous-network-connections-telnet-server-python
#
class MoodledProtocol(basic.LineReceiver):
    def connectionMade(self):
        message = 'Moodled server 0.01\r\nAwating commands..\r\nType: help will list all available commands'
        self.transport.write(message + '\r\n')

    def lineReceived(self, user):
        d = self.factory.getUser(user)

        def onError(err):
            return 'Internal server error, fatal exception!'
        d.addErrback(onError)

        def writeResponse(message):
            self.transport.write(message + '\r\n')
            self.transport.loseConnection()
        d.addCallback(writeResponse)

#
# http://twistedmatrix.com/documents/current/core/howto/tutorial/protocol.html
#
class MoodledFactory(protocol.ServerFactory):
    protocol = MoodledProtocol

    def __init__(self, **kwargs):
        self.users = kwargs

    def getUser(self, user):
        return defer.succeed(self.users.get(user, "No such user"))

class FingerSetterProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.lines = []

    def lineReceived(self, line):
        self.lines.append(line)

    def connectionLost(self, reason):
        user = self.lines[0]
        status = self.lines[1]
        self.factory.setUser(user, status)

class MoodledSetterFactory(protocol.ServerFactory):
    protocol = FingerSetterProtocol

    def __init__(self, fingerFactory):
        self.fingerFactory = fingerFactory

    def setUser(self, user, status):
        self.fingerFactory.users[user] = status


#application = service.Application('finger', uid=1, gid=1)
#serviceCollection = service.IServiceCollection(application)
#internet.TCPServer(79,ff).setServiceParent(serviceCollection)
#internet.TCPServer(1079,fsf).setServiceParent(serviceCollection)
#reactor.listenTCP(50001, fsf)
#reactor.run()


if __name__ == '__main__':
    #ff = MoodledFactory(moshez='Happy and well')
    #fsf = MoodledSetterFactory(ff)

    l = LED_controll()

    for i in range(0,20):
        l.painting_min(s=0.1, rnd=True)
        l.spaceship_min(s=0.1, rnd=True)

    for i in range(0,20):
        l.painting_min(s=0.01, rnd=True)
        l.spaceship_min(s=0.01, rnd=True)

    l.spaceship_wl_off()
    l.painting_wl_off()
    time.sleep(0.001)
    l.flip_painting()
    l.flip_alien_lamp()

    for i in range(0,120):
        l.flip_robot()


#for i in range(10,13):
#    l.painting_max(20, random.random()/i , rnd=True)
#    l.spaceship_max(20, random.random()/i , rnd=True)
