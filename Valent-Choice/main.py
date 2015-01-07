from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

#TODO
# - randomize across playlist of songs
# - switch up button locations, create parameter to control
#   - use different .kv files (?)
# - get songs into .wav format

import time
import random
import os, sys

from os import environ
from os.path import join, dirname, realpath

from functools import partial




import pygame

from kivy.lang import Builder
from kivy.clock import Clock

from kivy.config import Config
Config.set('graphics','fullscreen','auto')
Config.write()

from kivy.core.window import Window
Window.fullscreen = True


# this is crucial, it allows us to add 'custom' properties (ala integer vars) to kv objects
from kivy.properties import ListProperty, ObjectProperty, NumericProperty

from kivy.graphics.vertex_instructions import (Rectangle,
                                               Ellipse,
                                               Line)
from kivy.graphics.context_instructions import Color
# from kivy.graphics import Color



### imports from the YoctoPuce libraries, for the relay
# from yoctopuce.yocto_api import *
# from yoctopuce.yocto_relay import *
#
# #needed?
# def die(msg):
#     sys.exit(msg + ' (check USB cable)')
#
# # and now initialize all the stuff
# errmsg = YRefParam()
# #Get access to your device, connected locally on USB for instance
# if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
#     sys.exit("init error" + errmsg.value)
# relay = YRelay.FirstRelay()
# #if relay is None: die('no device connected')
#
# ###
pygame.init()
pygame.mixer.init()

# custom modules
from accessory_functions import *  # inputs the methods used to work with external files and filenames
# below made redundant with above
#from parameter_input import *  # this inputs all the methods we need to parse the parameters from running plans, requires above modules?

#input from file must happen up here, before class definitions, in order to create initial values for the classes below to take
#we're using globals for the parameters

# first, general input methods that can be applied across all programs
# second, specific methods for extracting the parameters of a given task



class ParametersAndData:
    # holds the parameters and data (e.g. time) that gets passed around the functions and classes
    inputfile = open('params.txt')
    pdict = parse_params(inputfile)

    #dLen, itiLen, toLen, maxTrials, distractors, sampleList, choiceList = globalize(pdict)

    timeout, hold, top, mid, bottom = globalize(pdict)


    phase = int(sys.argv[1])


    inputfile.close()

    # active variables for time keeping
    sessionStartT = time.time()  # the reference time

    trial = 1

    #touch = 1

    # these will be modified on a rolling basis


    thisSongChoice = ''
    thisGenre = ''

    trialStartT = 0
    sampleOnT = 0
    samplePressedT = 0
    choiceOnT = 0
    choicePressedT = 0

    #selectedSample = 0
    thisSample = 0
    sampListPos = 100
    trialPorts = list()
    woutreplace_portlist = list()

    #failed_trial = False
    butt_pos = 0
    randStartPos = False
    failedAttempt = 0



    # and the expanding data, to be written
    # setup the data matrix (header first)
    # data = [['Trial', 'Accuracy', 'PicChosen', 'CorrectPic', 'PicsDisplayed',
    #          'PortPressed',  # 'CorrectPort', # sorry, no easy way to get this
    #          'ActivePorts',
    #          'TrialStart', 'SessionStart',  # 'AbsTime', # redundant
    #          'SampleOn', 'SampleSelect', 'ChoiceOn', 'ChoiceSelect']]

    data = [['StartTime','Touch','Time','ButtonChosen','Song','ButtonPosition']]


# and now, the instance:


parameVars = ParametersAndData


class Start(Screen):  ##should Anchor/Box/etc.layout be Screen?
    pad = ObjectProperty(parameVars)


    def inc_trial(self, pad):
        pad.trial = pad.trial + 1
        #pygame.mixer.music.stop()



    def shift_to_holding(self, pad):
        #global trialStartT
        pad.trialStartT = time.time() - pad.sessionStartT

        pad.butt_pos = 0
        pad.randStartPos = False
        pad.failedAttempt = 0


        pad.thisSongChoice = 'N/A'
        pad.thisGenre = '(start pressed)'
        update_data(pad)

        #Clock.schedule_once(self.sample_screen_on, delay)
        self.manager.current = 'holder'


class Holding(Screen):  # aka time between start stim and sample
    pad = ObjectProperty(parameVars)

    def display_music_buttons(self, dt):
        self.manager.current = 'music'



class MusicChoice(Screen):
    pad = ObjectProperty(parameVars)

    def prepare_stimuli(self, pad):
        butt_pos = random.randint(1,6)
        randomize_buttons_layouts(self,pad,butt_pos)   # fairly self-explanatory
        # TODO this needs to randomize by TRIAL, not 'session'

        # appropriate button enabling
        print(self.ids.bottom.background_down)
        print(self.ids.top.background_down != 'zigzag.jpg')

        if pad.phase == 1:
            # classical button presented singly
            if self.ids.top.background_down != 'stripes-up.jpg':
                self.ids.top.disabled = True
            if self.ids.middle.background_down != 'stripes-up.jpg':
                self.ids.middle.disabled = True
            if self.ids.bottom.background_down != 'stripes-up.jpg':
                self.ids.bottom.disabled = True

        elif pad.phase == 2:
            # pop button presented singly
            if self.ids.top.background_down != 'zigzag.jpg':
                self.ids.top.disabled = True
            if self.ids.middle.background_down != 'zigzag.jpg':
                self.ids.middle.disabled = True
            if self.ids.bottom.background_down != 'zigzag.jpg':
                self.ids.bottom.disabled = True

        elif pad.phase == 3:
            if self.ids.top.background_down != 'dots.jpg':
                self.ids.top.disabled = True
            if self.ids.middle.background_down != 'dots.jpg':
                self.ids.middle.disabled = True
            if self.ids.bottom.background_down != 'dots.jpg':
                self.ids.bottom.disabled = True

        elif pad.phase == 4:
            enable_all_buttons(self)


        disable_all_buttons(self)



        Clock.schedule_once(self.failed_attempt, 30)

        if pad.phase == 1:
            pad.butt_pos = random.randint(1,3)   #formerly 3 => 6, and should be so again...(?)
            pad.thisGenre = 'pop'
            pad.randStartPos = True
            if pad.butt_pos == 1:
                self.ids.top.on_press = partial(self.turn_on_rock,pad)
                self.ids.top.background_normal = 'zigzag.jpg'
                self.ids.top.background_down = 'zigzag.jpg'
                self.ids.top.disabled = False
#                print("phase 1, pos 1")
            elif pad.butt_pos == 2:
                self.ids.middle.on_press = partial(self.turn_on_rock,pad)
                self.ids.middle.background_normal = 'zigzag.jpg'
                self.ids.middle.background_down = 'zigzag.jpg'
                self.ids.middle.disabled = False
#                print("phase 1, pos 2")
            elif pad.butt_pos == 3:
                self.ids.bottom.on_press = partial(self.turn_on_rock,pad)
                self.ids.bottom.background_normal = 'zigzag.jpg'
                self.ids.bottom.background_down = 'zigzag.jpg'
                self.ids.bottom.disabled = False
#                print("phase 1, pos 3")
#            else:
#                print("phase 1 failure")

        elif pad.phase == 2:
            pad.butt_pos = random.randint(1,3)
            pad.thisGenre = 'classical'
            pad.randStartPos = True
            if pad.butt_pos == 1:
                self.ids.top.on_press = partial(self.turn_on_classical,pad)
                self.ids.top.background_normal = 'stripes-up.jpg'
                self.ids.top.background_down = 'stripes-up.jpg'
                self.ids.top.disabled = False
            elif pad.butt_pos == 2:
                self.ids.middle.on_press = partial(self.turn_on_classical,pad)
                self.ids.middle.background_normal = 'stripes-up.jpg'
                self.ids.middle.background_down = 'stripes-up.jpg'
                self.ids.middle.disabled = False
            elif pad.butt_pos == 3:
                self.ids.bottom.on_press = partial(self.turn_on_classical,pad)
                self.ids.bottom.background_normal = 'stripes-up.jpg'
                self.ids.bottom.background_down = 'stripes-up.jpg'
                self.ids.bottom.disabled = False

        elif pad.phase == 3: # music is playing when trial starts, chimps must press stop button to be rewarded
            pad.butt_pos = random.randint(1,3)
            
            if (not random.getrandbits(1)):
                pad.thisGenre = 'classical'
                pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/classical')) #change dir name to whatever 
                pygame.mixer.music.load(os.curdir+'/classical/'+pad.thisSongChoice)
                Clock.schedule_once(self.failed_attempt, pygame.mixer.Sound(os.curdir+'/classical/'+pad.thisSongChoice).get_length())
                pygame.mixer.music.play()
            else:
                pad.thisGenre = 'pop'
                pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/rock_pop')) #change dir name to whatever
                pygame.mixer.music.load(os.curdir+'/rock_pop/'+pad.thisSongChoice)
                Clock.schedule_once(self.failed_attempt, pygame.mixer.Sound(os.curdir+'/rock_pop/'+pad.thisSongChoice).get_length())
                pygame.mixer.music.play()


            update_data(pad)
            
            if pad.butt_pos == 1:
                self.ids.top.on_press = partial(self.turn_off,pad)
                self.ids.top.background_normal = 'dots.jpg'
                self.ids.top.background_down = 'dots.jpg'
                self.ids.top.disabled = False
            elif pad.butt_pos == 2:
                self.ids.middle.on_press = partial(self.turn_off,pad)
                self.ids.middle.background_normal = 'dots.jpg'
                self.ids.middle.background_down = 'dots.jpg'
                self.ids.middle.disabled = False
            elif pad.butt_pos == 3:
                self.ids.bottom.on_press = partial(self.turn_off,pad)
                self.ids.bottom.background_normal = 'dots.jpg'
                self.ids.bottom.background_down = 'dots.jpg'
                self.ids.bottom.disabled = False




        else:
            print("phase failure")




        #randomize_buttons_layouts(self,pad,butt_pos)   # fairly self-explanatory
        # TODO this needs to randomize by TRIAL, not 'session'

        # appropriate button enabling

        # all below needs to be fixed

        # print(self.ids.bottom.background_down)
        # print(self.ids.top.background_down != 'zigzag.jpg')
        #
        # if pad.phase == 1:
        #     # classical button presented singly
        #     if self.ids.top.background_down != 'stripes-up.jpg':
        #         self.ids.top.disabled = True
        #     if self.ids.middle.background_down != 'stripes-up.jpg':
        #         self.ids.middle.disabled = True
        #     if self.ids.bottom.background_down != 'stripes-up.jpg':
        #         self.ids.bottom.disabled = True
        #
        # elif pad.phase == 2:
        #     # pop button presented singly
        #     if self.ids.top.background_down != 'zigzag.jpg':
        #         self.ids.top.disabled = True
        #     if self.ids.middle.background_down != 'zigzag.jpg':
        #         self.ids.middle.disabled = True
        #     if self.ids.bottom.background_down != 'zigzag.jpg':
        #         self.ids.bottom.disabled = True
        #
        # elif pad.phase == 3:
        #     if self.ids.top.background_down != 'dots.jpg':
        #         self.ids.top.disabled = True
        #     if self.ids.middle.background_down != 'dots.jpg':
        #         self.ids.middle.disabled = True
        #     if self.ids.bottom.background_down != 'dots.jpg':
        #         self.ids.bottom.disabled = True
        #
        # elif pad.phase == 4:
        #     enable_all_buttons(self)
        #
        # elif pad.phase == 5:
        #     enable_all_buttons(self)


    def load_name(self, *l):
        for id_str, widget in self.parent.ids.iteritems():
            if widget.__self__ is self:
                self.name = id_str
                return




    def turn_off(self, pad):
        pygame.mixer.music.stop()

        pad.thisSongChoice = ''
        pad.thisGenre = '(stop)'
        #print(self.loc)
        #pad.buttonLocation = self.ids
        update_data(pad)


    def turn_on_rock(self, pad):
        pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/rock_pop')) #change dir name to whatever
        pygame.mixer.music.load(os.curdir+'/rock_pop/'+pad.thisSongChoice)
        # if pad.randStartPos :
        #     pygame.mixer.music.play(0,random.randint(1,2))
        # else:
        pygame.mixer.music.play()


        update_data(pad)

        #disable
        disable_all_buttons(self)

        Clock.unschedule(self.failed_attempt)

        #Clock.schedule_once(self.turn_buttons_back_on, pad.timeout)
        Clock.schedule_once(self.new_trial, 3)

        #pad.buttonLocation = self.load_name()

        #pad.buttonLocation = self.id



    def turn_on_classical(self, pad):
        pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/classical')) #change dir name to whatever
        pygame.mixer.music.load(os.curdir+'/classical/'+pad.thisSongChoice)
        # if pad.randStartPos :
        #     pygame.mixer.music.play(0,random.randint(1,2))
        # else:
        pygame.mixer.music.play()

        update_data(pad)

        #disable
        disable_all_buttons(self)

        Clock.unschedule(self.failed_attempt)

        Clock.schedule_once(self.new_trial, 3)

        #pad.buttonLocation = self.ids
       # pad.buttonLocation = self.load_name()



    def turn_buttons_back_on(self,num):
        enable_all_buttons(self)




    def failed_attempt(self,num):

        Clock.unschedule(self.failed_attempt)

        self.manager.current = 'reset'



    def new_trial(self,num):
        pygame.mixer.music.stop()

        self.manager.current = 'holder'



# this is really the end of the previous trial...
class ResetInterval(Screen):  # aka time between music choice and start stim
    #Clock.schedule_once(self.start_trial, 3)

    pad = ObjectProperty(parameVars)

    def log_failure(self, pad):
        #pad.thisSongChoice = '(timed out)'
        pad.failedAttempt = '1'
        update_data(pad)


    def start_new_trial(self, dt):

        self.manager.current = 'startStim'


    ###
    # unless we need to have use of a more general blank delay screen,
    # the code below should *not* be used.

    #time.sleep(2)
    #sm.current = 'sample'


    #def sample_screen_on(self,dt):
    #self.manager.current = 'sample'



#root_widget = Builder.load_file('C:/Program Files (x86)/Kivy-1.8.0-py3.3-win32/kivy/mine/sample.kv')
#Builder.load_file('E:/Valent-Choice/ValentChoice.kv')
#Builder.load_file('Z:/kivy/DMTS/DMTS.kv')
#Builder.load_file('C:/Users/Diapadion/Dropbox/python - kivy/Valent-Choice/ValentChoice.kv')
#Builder.load_file('C:/Users/s1229179/git-repos/kivy/Valent-Choice/ValentChoice.kv')
#Builder.load_file('C:/Users/Diapadion/Documents/GitHub/kivy/Valent-Choice/ValentChoice.kv')
#
#Builder.load_file('/home/emma/Desktop/Emma/ValentChoice.kv')
#




sm = ScreenManager()
sm = ScreenManager(transition=NoTransition())

# sm.add_widget(ROC_MusicChoice(name='ROC'))
# sm.add_widget(ORC_MusicChoice(name='ORC'))
# sm.add_widget(CRO_MusicChoice(name='CRO'))
# sm.add_widget(RCO_MusicChoice(name='RCO'))
# sm.add_widget(COR_MusicChoice(name='COR'))
# sm.add_widget(OCR_MusicChoice(name='OCR'))


sm.add_widget(MusicChoice(name='music'))


sm.add_widget(Holding(name='holder'))
sm.add_widget(ResetInterval(name='reset'))

sm.add_widget(Start(name='startStim'))
# must specify length of pauses for these, time must become variable


#sm.add_widget(PosReinforce(name='incorrect'))



sm.current = 'startStim'


class DMTSApp(App):
    def on_stop(self):
        write_data(parameVars.data,parameVars.sessionStartT)

    #pass
    # use this to write the data, at whichever point the program is at



    def build(self):
        return sm


    #def on_start(self):
    #sm.ids.delay.locDelay = 5


if __name__ == "__main__":
    DMTSApp().run()
