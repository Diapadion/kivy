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

## imports from the YoctoPuce libraries, for the relay
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


# this is crucial, it allows us to add 'custom' properties (ala integer vars) to kv objects
from kivy.properties import ListProperty, ObjectProperty, NumericProperty

from kivy.graphics.vertex_instructions import (Rectangle,
                                               Ellipse,
                                               Line)
from kivy.graphics.context_instructions import Color
# from kivy.graphics import Color

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

    timeout, hold, top, mid, bottom, maxTrials, testingTrials = globalize(pdict)
    # maxTrials can be 10 or less, but not more

    phase =6 # needed for legacy effects

    maxTrials = testingTrials



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
    lastAttemptSuccess = True

    actualStart = False

    subtype4 = random.sample([1,1,1,2,2,2,3,3,3,],9)
    subtype4.append(random.sample([2,3],1))
#    lastSubtype = 0
    lastSubtype = int(sys.argv[1])


    # subtype5 = random.sample([1,1,1,1,1,1,1,1,1,1,
    #                           2,2,2,2,2,2,2,2,2,2,
    #                           3,3,3,3,3,3,3,3,3,3,
    #                           4,4,4,4,4,4,4,4,4,4,5],41)
    subtype5 = subtype4

    rewarded = 0

    # phase 6 vars
    portPressed = 0

  #  http://aricoozo.com/fascinating-large-scale-portrait-paintings-by-erik-maniscalco/



    # and the expanding data, to be written
    # setup the data matrix (header first)
    # data = [['Trial', 'Accuracy', 'PicChosen', 'CorrectPic', 'PicsDisplayed',
    #          'PortPressed',  # 'CorrectPort', # sorry, no easy way to get this
    #          'ActivePorts',
    #          'TrialStart', 'SessionStart',  # 'AbsTime', # redundant
    #          'SampleOn', 'SampleSelect', 'ChoiceOn', 'ChoiceSelect']]

    data = [['StartTime','Trial','Time','MusicPlaying','Song','ButtonPosition/Layout','FailedAttempt','Rewarded','PortPressed']]


# and now, the instance:


parameVars = ParametersAndData


class Start(Screen):  ##should Anchor/Box/etc.layout be Screen?
    pad = ObjectProperty(parameVars)


    # currently unused
    def inc_trial(self, pad):
        pad.trial = pad.trial + 1
        #pygame.mixer.music.stop()

    def stop_music(self):
        pygame.mixer.music.stop()


    def shift_to_holding(self, pad):
        #global trialStartT
        pad.trialStartT = time.time() - pad.sessionStartT

        pad.butt_pos = 0
        pad.randStartPos = False
        pad.failedAttempt = 0
        pad.actualStart = True



        pad.thisSongChoice = 'N/A'
        pad.thisGenre = '(start pressed)'
        update_data(pad)

        #Clock.schedule_once(self.sample_screen_on, delay)
        self.manager.current = 'holder'


class Holding(Screen):  # aka time between start stim and sample
    pad = ObjectProperty(parameVars)

    def display_music_buttons(self, dt):

        self.manager.current = 'music'


    def check_endpoint(self,pad):
        if pad.trial > pad.maxTrials:
            App.get_running_app().stop()


        pad.trialStartT = time.time() - pad.sessionStartT

        pad.randStartPos = False
        pad.failedAttempt = 0
        pad.actualStart = True




class MusicChoice(Screen):
    pad = ObjectProperty(parameVars)

    def prepare_stimuli(self, pad):

        # randomly allocate buttons
        pad.butt_pos = random.sample(range(1,10), 3)
        # 1st, pop; 2nd, classical; 3rd, off
        disable_grid(self, pad)


        # some legacy stuff to keep it from misperforming
        pad.rewarded = 0

        if pad.actualStart:
            #Clock.schedule_once(self.failed_attempt, pad.timeout)
            disable_grid(self, pad)



        # if pad.lastAttemptSuccess:
        #     pad.lastSubtype = pad.subtype5.pop(0)
#             pad.lastSubtype = random.sample([1,2,3],2) #new, but unneeded


        # including the allocation of music-playing trial types
        if pad.trial == 1:
            if pad.lastSubtype == 1: # pop is playing
                pad.thisGenre = 'pop'
                pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/rock_pop')) #change dir name to whatever
                pygame.mixer.music.load(os.curdir+'/rock_pop/'+pad.thisSongChoice)
                pygame.mixer.music.play()
            elif pad.lastSubtype == 2: # classical is playing
                pad.thisGenre = 'classical'
                pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/classical')) #change dir name to whatever
                pygame.mixer.music.load(os.curdir+'/classical/'+pad.thisSongChoice)
                pygame.mixer.music.play()
            else: # nothing is playing
                pad.thisGenre = '(silent)'
                pad.thisSongChoice = 'N/A'

        if pad.actualStart:
            update_data(pad)


        # "disable" all ports
        # i.e. make them look inactive


        # assign ports with music button appearance and behaviors

        # pop
        portNum = pad.butt_pos[0]
        eStr = 'self.ids.n' + str(portNum)
        exec(eStr + '.background_normal = \'zigzag.jpg\'')
        exec(eStr + '.background_down = \'zigzag.jpg\'')

    #   exec(eStr + '.on_press = self.turn_on_rock(pad)')
        exec(eStr + '.on_press = partial(self.turn_on_rock,pad)')

        # classical
        portNum = pad.butt_pos[1]
        eStr = 'self.ids.n' + str(portNum)
        exec(eStr + '.background_normal = \'stripes-up.jpg\'')
        #exec(eStr + '.on_press = self.turn_on_classical(pad)')
        exec(eStr + '.on_press = partial(self.turn_on_classical,pad)')

        # off
        portNum = pad.butt_pos[2]
        eStr = 'self.ids.n' + str(portNum)
        exec(eStr + '.background_normal = \'dots.jpg\'')
        #exec(eStr + '.on_press = self.turn_off(pad)')
        exec(eStr + '.on_press = partial(self.turn_off ,pad)')


        #portID = lookup_port(portNum)



    #do nothing yet
    print('ack')







    def load_name(self, *l):
        for id_str, widget in self.parent.ids.iteritems():
            if widget.__self__ is self:
                self.name = id_str
                return

    def empty_touch(self, mark, pad):
        # records data when participant presses an 'empty' space

        #print(self.marker)
        # mark = self.marker

        pad.failedAttempt = 2
        pad.portPressed = mark

        update_data(pad)

        pad.failedAttempt = 0
        pad.portPressed = 0


    def turn_off(self, pad):
        pygame.mixer.music.stop()

        pad.thisSongChoice = ''
        pad.thisGenre = '(stop)'
        pad.rewarded = 1
        #print(self.loc)
        #pad.buttonLocation = self.ids
        if pad.phase == 6:
            pad.portPressed = pad.butt_pos[2]
            disable_grid(self, pad)
        else:
            disable_all_buttons(self)

        update_data(pad)
        pad.trial = pad.trial + 1
        pad.rewarded = 0
        #self.dispense_reward()
        pad.portPressed = 0

        Clock.schedule_once(self.new_trial, 3)


    def turn_on_rock(self, pad):
        pad.thisGenre = 'pop'
        pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/rock_pop')) #change dir name to whatever
        pygame.mixer.music.load(os.curdir+'/rock_pop/'+pad.thisSongChoice)
        # if pad.randStartPos :
        #     pygame.mixer.music.play(0,random.randint(1,2))
        # else:
        pygame.mixer.music.play(-1)


        pad.rewarded = 1
        if pad.phase == 6:
            pad.portPressed = pad.butt_pos[0]
            disable_grid(self, pad)
        else:
            disable_all_buttons(self)


        update_data(pad)
        pad.trial = pad.trial + 1
        pad.rewarded = 0
        #self.dispense_reward()
        pad.portPressed = 0


        Clock.unschedule(self.failed_attempt)
        pad.lastAttemptSuccess = True
        #Clock.schedule_once(self.turn_buttons_back_on, pad.timeout)
        Clock.schedule_once(self.new_trial, 3)

        #pad.buttonLocation = self.load_name()

        #pad.buttonLocation = self.id



    def turn_on_classical(self, pad):
        pad.thisGenre = 'classical'
        pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/classical')) #change dir name to whatever
        pygame.mixer.music.load(os.curdir+'/classical/'+pad.thisSongChoice)
        # if pad.randStartPos :
        #     pygame.mixer.music.play(0,random.randint(1,2))
        # else:
        #pygame.mixer.music.set_endevent(pygame.mixer.music.play())

        pygame.mixer.music.play(-1)

        pad.rewarded = 1
        if pad.phase == 6:
            pad.portPressed = pad.butt_pos[1]
            disable_grid(self, pad)
        else:
            disable_all_buttons(self)

        update_data(pad)
        pad.trial = pad.trial + 1
        pad.rewarded = 0

        #self.dispense_reward()
        pad.portPressed = 0

        Clock.unschedule(self.failed_attempt)
        pad.lastAttemptSuccess = True
        Clock.schedule_once(self.new_trial, 3)

        #pad.buttonLocation = self.ids
       # pad.buttonLocation = self.load_name()




    def dispense_reward(self):
        # relay.set_state(YRelay.STATE_B)
        # time.sleep(0.1)
        # relay.set_state(YRelay.STATE_A)
        return

    def failed_attempt(self,num):

        Clock.unschedule(self.failed_attempt)

        self.manager.current = 'reset'



    def new_trial(self,num):
        #pygame.mixer.music.stop() # not anymore...

        self.manager.current = 'holder'



# this is really the end of the previous trial...
class ResetInterval(Screen):  # aka time between music choice and start stim
    #Clock.schedule_once(self.start_trial, 3)

    pad = ObjectProperty(parameVars)

    def log_failure(self, pad):
        #pad.thisSongChoice = '(timed out)'
        pad.failedAttempt = 1
        pad.lastAttemptSuccess = False  # TODO propagate this
        pad.thisSongChoice = '(no press)'
        pad.rewarded = 0
        pad.portPressed = 0
        update_data(pad)


    def start_new_trial(self, dt):

        self.manager.current = 'startStim'


    def check_endpoint(self,pad):
        if pad.trial > pad.maxTrials:
            App.get_running_app().stop()



    ###
    # unless we need to have use of a more general blank delay screen,
    # the code below should *not* be used.

    #time.sleep(2)
    #sm.current = 'sample'


    #def sample_screen_on(self,dt):
    #self.manager.current = 'sample'

if parameVars.phase == 6:
    Builder.load_file('C:/Users/s1229179/git-repos/kivy/Valent-Choice/ValentGrid.kv')
    #Builder.load_file('/home/emma/Desktop/Emma/ValentGrid.kv')

else:
    #root_widget = Builder.load_file('C:/Program Files (x86)/Kivy-1.8.0-py3.3-win32/kivy/mine/sample.kv')
    #Builder.load_file('E:/Valent-Choice/ValentChoice.kv')
    #Builder.load_file('Z:/kivy/DMTS/DMTS.kv')
    #Builder.load_file('C:/Users/Diapadion/Dropbox/python - kivy/Valent-Choice/ValentChoice.kv')
    Builder.load_file('C:/Users/s1229179/git-repos/kivy/Valent-Choice/ValentChoice.kv')
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


sm.current = 'music'



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
