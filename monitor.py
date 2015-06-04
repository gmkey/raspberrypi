#!/usr/bin/env python
#-*- coding: utf-8 -*-

##
## monitor.py - monitor
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



import os
import pygame
import time
import random
import urllib
import Image
import StringIO

class Monitor:
    screen = None
    colorkey = [0, 0, 0]


    scheveningen_tide = 'http://getij.rws.nl/getij_resultaat.cfm?location=SCHEVNGN'
    scheveningen_baseurl = 'http://www.scheveningenlive.nl/'
    scheveningen_webcams = ['cam_1.jpg', 'cam2.jpg', 'cam3.jpg', 'pier.jpg']

    last_fetch_try = 0
    last_fetch_success = 0

    last_surface = None


    def __init__(self):
        pygame.display.init()
        pygame.mouse.set_visible(False)
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self.screen.fill((0, 0, 0))
        pygame.font.init()
        self.font_small = pygame.font.SysFont("freesans", 50)
        self.text = self.font_small.render('Test', True, (200,30,30))
        pygame.display.update()


    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."


    def refresh_image(self, surface):
        if time.time() > self.last_fetch_try + 60:
            self.last_fetch_try = time.time()
            x_scale = 318
            y_scale = 201
            for i in range(4):
                url = self.scheveningen_baseurl + self.scheveningen_webcams[i]
                f = StringIO.StringIO(urllib.urlopen(url).read())
                im_surf = pygame.image.load(f, "cam.jpg")
                im_surf = pygame.transform.scale(im_surf, (x_scale, y_scale))
                im_surf.set_colorkey(self.colorkey)
                im_surf.set_alpha(100)
                if i < 2:
                    surface.blit(im_surf, (5 + i * x_scale, 0))
                else:
                    i = i - 2
                    surface.blit(im_surf, (5 + i * x_scale, y_scale + 5))
            self.last_surface = surface.copy()
            return(surface)
        return(self.last_surface)

    def test(self):
        i = 0
        import math
        while True:
            self.screen.fill((0,0,0))
            webcams_bg = self.screen.copy()
            webcams_bg = self.refresh_image(webcams_bg)
            self.screen.blit(webcams_bg, (0,0))
            i+=1
            if i>360:
                i=0
            self.screen.blit(self.text, (int(math.sin(i)*100)+100,int(math.sin(i)*100)+100))
            pygame.display.flip()

monitor = Monitor()
monitor.test()
