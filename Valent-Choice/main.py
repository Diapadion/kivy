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

# this is for compiling the Kivy python app under Windows

def prep_win_standalone():
    class DummyStream():
        def __init__(self):
            pass

        def write(self, data):
            pass

        def read(self, data):
            pass

        def flush(self):
            pass

        def close(self):
            pass

    sys.stdin = DummyStream()
    sys.stdout = DummyStream()
    sys.stderr = DummyStream()
    sys.__stdin__ = DummyStream()
    sys.__stdout__ = DummyStream()
    sys.__stderr__ = DummyStream()

    exec_dir = dirname(realpath(sys.argv[0]))
    #environ['KIVY_DATA_DIR'] = join(exec_dir, 'data')
    environ['KIVY_DATA_DIR'] = 'C:\Program Files (x86)\Kivy-1.8.0-py3.3-win32\kivy\kivy\data'


import pygame

from kivy.lang import Builder
from kivy.clock import Clock

from kivy.config import Config#
Config.set('graphics','fullscreen','auto')
Config.write()

from kivy.core.window import Window
Window.fullscreen = False

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

    timeout, top, mid, bottom = globalize(pdict)


    #distractors = sys.argv[1]

    inputfile.close()

    # active variables for time keeping
    sessionStartT = time.time()  # the reference time

    touch = 1


    # these till be modified on a rolling basis


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



class MusicChoice(Screen):
    pad = ObjectProperty(parameVars)

    def prepare_stimuli(self, pad):

        if pad.top == 'rock':
            if pad.mid == 'off':
                self.ids.top.on_press = partial(self.turn_on_rock,pad)
                self.ids.top.background_normal = 'zigzag.jpg'
                self.ids.top.background_down = 'zigzag.jpg'
                self.ids.middle.on_press = partial(self.turn_off,pad)
                self.ids.middle.background_normal = 'dots.jpg'
                self.ids.middle.background_down = 'dots.jpg'
                self.ids.bottom.on_press = partial(self.turn_on_classical,pad)
                self.ids.bottom.background_normal = 'stripes-up.jpg'
                self.ids.bottom.background_down = 'stripes-up.jpg'
            elif pad.mid == 'classical':
                self.ids.top.on_press = partial(self.turn_on_rock,pad)
                self.ids.top.background_normal = 'zigzag.jpg'
                self.ids.top.background_down = 'zigzag.jpg'
                self.ids.middle.on_press = partial(self.turn_on_classical,pad)
                self.ids.middle.background_normal = 'stripes-up.jpg'
                self.ids.middle.background_down = 'stripes-up.jpg'
                self.ids.bottom.on_press = partial(self.turn_off,pad)
                self.ids.bottom.background_normal = 'dots.jpg'
                self.ids.bottom.background_down = 'dots.jpg'
        elif pad.top == 'off':
            if pad.mid == 'rock':
                self.ids.top.on_press = partial(self.turn_off,pad)
                self.ids.top.background_normal = 'dots.jpg'
                self.ids.top.background_down = 'dots.jpg'
                self.ids.middle.on_press = partial(self.turn_on_rock,pad)
                self.ids.middle.background_normal = 'zigzag.jpg'
                self.ids.middle.background_down = 'zigzag.jpg'
                self.ids.bottom.on_press = partial(self.turn_on_classical,pad)
                self.ids.bottom.background_normal = 'stripes-up.jpg'
                self.ids.bottom.background_down = 'stripes-up.jpg'
            elif pad.mid == 'classical':
                self.ids.top.on_press = partial(self.turn_off,pad)
                self.ids.top.background_normal = 'dots.jpg'
                self.ids.top.background_down = 'dots.jpg'
                self.ids.middle.on_press = partial(self.turn_on_classical,pad)
                self.ids.middle.background_normal = 'stripes-up.jpg'
                self.ids.middle.background_down = 'stripes-up.jpg'
                self.ids.bottom.on_press = partial(self.turn_on_rock,pad)
                self.ids.bottom.background_normal = 'zigzag.jpg'
                self.ids.bottom.background_down = 'zigzag.jpg'
        elif pad.top == 'classical':
            if pad.mid == 'rock':
                self.ids.top.on_press = partial(self.turn_on_classical,pad)
                self.ids.top.background_normal = 'stripes-up.jpg'
                self.ids.top.background_down = 'stripes-up.jpg'
                self.ids.middle.on_press = partial(self.turn_on_rock,pad)
                self.ids.middle.background_normal = 'zigzag.jpg'
                self.ids.middle.background_down = 'zigzag.jpg'
                self.ids.bottom.on_press = partial(self.turn_off,pad)
                self.ids.bottom.background_normal = 'dots.jpg'
                self.ids.bottom.background_down = 'dots.jpg'
            elif pad.mid == 'off':
                self.ids.top.on_press = partial(self.turn_on_classical,pad)
                self.ids.top.background_normal = 'stripes-up.jpg'
                self.ids.top.background_down = 'stripes-up.jpg'
                self.ids.middle.on_press = partial(self.turn_off,pad)
                self.ids.middle.background_normal = 'dots.jpg'
                self.ids.middle.background_down = 'dots.jpg'
                self.ids.bottom.on_press = partial(self.turn_on_rock,pad)
                self.ids.bottom.background_normal = 'zigzag.jpg'
                self.ids.bottom.background_down = 'zigzag.jpg'

            enable_all_buttons(self)


    def load_name(self, *l):
        for id_str, widget in self.parent.ids.iteritems():
            if widget.__self__ is self:
                self.name = id_str
                return


    def update_data(self, pad):
        dickory = time.time() - pad.sessionStartT
        pad.data.append([pad.sessionStartT, pad.touch, dickory,
                         pad.thisGenre, pad.thisSongChoice])
            #, pad.buttonLocation])



        pad.touch = pad.touch + 1



    def turn_off(self, pad):
        pygame.mixer.music.stop()

        pad.thisSongChoice = ''
        pad.thisGenre = '(stop)'
        #print(self.loc)
        #pad.buttonLocation = self.ids
        self.update_data(pad)


    def turn_on_rock(self, pad):
        pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/rock_pop')) #change dir name to whatever
        pygame.mixer.music.load(os.curdir+'/rock_pop/'+pad.thisSongChoice)
        pygame.mixer.music.play()
        pad.thisGenre = 'pop'

        self.update_data(pad)

        #disable
        disable_all_buttons(self)
        Clock.schedule_once(self.turn_buttons_back_on, pad.timeout)

        #pad.buttonLocation = self.load_name()

        #pad.buttonLocation = self.id




    def turn_on_classical(self, pad):
        pad.thisSongChoice = random.choice(os.listdir(os.curdir+'/classical')) #change dir name to whatever
        pygame.mixer.music.load(os.curdir+'/classical/'+pad.thisSongChoice)
        pygame.mixer.music.play()
        pad.thisGenre = 'classical'

        self.update_data(pad)

        #disable
        disable_all_buttons(self)
        Clock.schedule_once(self.turn_buttons_back_on, pad.timeout)

        #pad.buttonLocation = self.ids
       # pad.buttonLocation = self.load_name()



    def turn_buttons_back_on(self,num):
        enable_all_buttons(self)









# this is really the end of the previous trial...
class InterTrialInterval(Screen):
    #Clock.schedule_once(self.start_trial, 3)

    pad = ObjectProperty(parameVars)

    def update_data(self, pad):
        pad.data.append([pad.trial, pad.success, pad.thisSample, pad.selectedSample, pad.choiceList
            , pad.chosenPort, pad.trialPorts
            , pad.trialStartT, pad.sessionStartT, pad.sampleOnT, pad.samplePressedT, pad.choiceOnT, pad.choicePressedT
        ])

        print(pad.data)

        pad.touch = pad.touch + 1

        if pad.touch > pad.maxTrials:
            App.get_running_app().stop()


    def start_touch(self, itit):
        self.manager.current = 'startStim'


class StartScreen(Screen):  ##should Anchor/Box/etc.layout be Screen?
    pad = ObjectProperty(parameVars)

    # unused...
    def new_trial(self, pad):
        pad.trial = pad.trial + 1


    def shift_to_sample(self, pad):
        #    global trialStartT
        pad.trialStartT = time.time() - pad.sessionStartT
        delay = 0.5  #this needs to be made into an input var

        #Clock.schedule_once(self.sample_screen_on, delay)
        self.manager.current = 'initialPause'

    ###
    # unless we need to have use of a more general blank delay screen,
    # the code below should *not* be used.

    #time.sleep(2)
    #sm.current = 'sample'


    #def sample_screen_on(self,dt):
    #self.manager.current = 'sample'


###

class EmptyPause(Screen):  # aka time between start stim and sample

    def display_sample(self, dt):
        self.manager.current = 'sample'


class SampleScreen(Screen):
    pad = ObjectProperty(parameVars)

    def prepare_stimuli(self, pad):
        portsUsed = []

        #self.ids.n6.background_color = (0.1, 1, 0.1, 0.00)

        # disable all the button-ports, re-enabling them on a case by case basis
        disable_all_buttons(self)



        # when there is a single item for the sample (or choice), the for loop iterates INTO the STRING
        # but it needs to be treated as a list of length one, very simply
        #
        # Solution (maybe permanent): only ever select one sample from the sample list
        #
        #pad.thisSample = random.choice(pad.sampleList)
        #pad.sampListPos = pad.sampleList.index(pad.thisSample)


        ### New code for selecting at random from the files in the 'stimuli' directory

        pad.thisSample = random.choice(os.listdir(os.curdir+'/stimuli')) #change dir name to whatever
        pad.thisSample = os.curdir+'/stimuli/'+pad.thisSample
        #print(pad.thisSample) #debug

        # choose which port to display in

        distInt = int(pad.distractors)

        pad.woutreplace_portlist = random.sample(list(range(1, 9)), (distInt+2)) # len(pad.choiceList))
        pad.trialPorts = list(pad.woutreplace_portlist)
        
        portNum = pad.woutreplace_portlist.pop()

        #portNum = random.choice(range(1, 9)) #16))
        # enable that port
        eStr = 'self.ids.n' + str(portNum)
        exec(eStr + '.background_normal = \'' + pad.thisSample + '\'')
        exec(eStr + '.background_down = \'' + pad.thisSample + '\'')
        exec(eStr + '.background_color = (1,1,1,1)')
        exec(eStr + '.disabled = False')

        # the older version below iterated through the sample list
        #woutreplace_portlist = random.sample(list(range(1,16)),  len(sampleList))
        #for n in sampleList:
        ##portNum = random.randint(1,16)
        #portNum = woutreplace_portlist.pop()
        #portsUsed.append(portNum)
        ##portID = lookup_port(portNum)
        #eStr = 'self.ids.n' + str(portNum)
        #exec(eStr + '.background_normal = \''+n+'\'')
        #exec(eStr + '.background_down = \''+n+'\'')
        #exec(eStr + '.background_color = (1,1,1,1)')
        #exec(eStr + '.disabled = False')

        pad.sampleOnT = time.time() - pad.trialStartT - pad.sessionStartT

    # when displaying the sample, we need to first change the stimuli to be what we want on the current trial

    def change_stimuli(self, pad):
        # probably will remove this function
        self.ids.n3.background_normal = 'whiteBkgd.png'

    #pass

    def shift_to_choice(self, marker, picPressed, pad):
        # record the button that was pressed
        print(marker)
        pad.samplePressedT = time.time() - pad.trialStartT - pad.sessionStartT
        self.manager.current = 'delay'
        # this needs to pick out WHICH stim in the list is chosen by the program... which should now be done above

        pad.selectedSample = picPressed



    # may also need to activate buttons from deactivated and invisible state...


class ChoiceScreen(Screen):
    # when displaying this screen, we need to first change the stimuli to be what we want on this trial
    pad = ObjectProperty(parameVars)

    def prepare_choices(self, pad):
        # disable all the button-ports, re-enabling them on a case by case basis
        disable_all_buttons(self)


        print('made it')

        # TODO
        # code in to specify the number of distractors,
        # making sure to have the sample visible
        #pad.picsShown = list()

        distInt = int(pad.distractors)

        #woutreplace_portlist = random.sample(list(range(1, 9)), (distInt+1)) # len(pad.choiceList))  #FORMERLY 9 = 16
        #pad.trialPorts = list(woutreplace_portlist)



        # first we must take care of the sample

        portNum = pad.woutreplace_portlist.pop()
        eStr = 'self.ids.n' + str(portNum)

        #self.ids.portID.background_normal = n
        exec(eStr + '.background_normal = \'' + pad.thisSample + '\'')
        #self.ids.portID.background_down = n
        exec(eStr + '.background_down = \'' + pad.thisSample + '\'')
        # and then re-enable the button, and give it attributes
        exec(eStr + '.background_color = (1,1,1,1)')
        exec(eStr + '.disabled = False')
        #exec(eStr + '.on_release = self.shift_to_choice()')
        pad.choiceOnT = time.time() - pad.trialStartT - pad.sessionStartT

        #for n in pad.choiceList:
        for n in range(distInt):
            #portNum = random.randint(1,16)
            portNum = pad.woutreplace_portlist.pop()
            #portID = lookup_port(portNum)

            image = random.choice(os.listdir(os.curdir+'/stimuli')) #change dir name to whatever
            image = os.curdir+'/stimuli/'+image

            print(image)

            eStr = 'self.ids.n' + str(portNum)

            #self.ids.portID.background_normal = n
            exec(eStr + '.background_normal = \'' + image + '\'')
            #self.ids.portID.background_down = n
            exec(eStr + '.background_down = \'' + image + '\'')
            # and then re-enable the button, and give it attributes
            exec(eStr + '.background_color = (1,1,1,1)')
            exec(eStr + '.disabled = False')
            #exec(eStr + '.on_release = self.shift_to_choice()')
            pad.choiceOnT = time.time() - pad.trialStartT - pad.sessionStartT

    def trial_result(self, marker, selectedChoice, pad):

        # this needs to match based on WHEN the image is declared within the list
        # NOT by picture identity
        #
        pad.choicePressedT = time.time() - pad.trialStartT - pad.sessionStartT
        pad.chosenPort = marker

        if (pad.thisSample == selectedChoice):
        #if (pad.sampListPos == pad.choiceList.index(selectedChoice)):
            pad.success = 1
            self.manager.current = 'correct'

        else:
            pad.success = 0
            self.manager.current = 'incorrect'





#root_widget = Builder.load_file('C:/Program Files (x86)/Kivy-1.8.0-py3.3-win32/kivy/mine/sample.kv')
#Builder.load_file('Z:/kivy/DMTS/DMTS.kv')
#Builder.load_file('C:/Users/Diapadion/Dropbox/python - kivy/Valent-Choice/ValentChoice.kv')
Builder.load_file('C:/Users/s1229179/Dropbox/python - kivy/Valent-Choice/ValentChoice.kv')
#Builder.load_file('/home/dremalt/Desktop/zoo-programs/Valent-Choice/ValentChoice.kv')

# before beginning the task, we need to import the parameters for the session
# saving the parameters as globals ... or is this bad practice ???
delayLength = 3
dLen = delayLength

sm = ScreenManager()
sm = ScreenManager(transition=NoTransition())

# sm.add_widget(ROC_MusicChoice(name='ROC'))
# sm.add_widget(ORC_MusicChoice(name='ORC'))
# sm.add_widget(CRO_MusicChoice(name='CRO'))
# sm.add_widget(RCO_MusicChoice(name='RCO'))
# sm.add_widget(COR_MusicChoice(name='COR'))
# sm.add_widget(OCR_MusicChoice(name='OCR'))


sm.add_widget(MusicChoice(name='music'))


sm.add_widget(SampleScreen(name='sample'))

sm.add_widget(StartScreen(name='startStim'))
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
