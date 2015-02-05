#from kivy.graphics import Color
import csv
import time
import datetime # added 19/08

from kivy.graphics.context_instructions import Color

from functools import partial




### Accessory functions



#def end_task():
       #App.stop()


      
def write_data(data,start):
       end = time.time()
       startTimeStr = time.strftime("%Y%m%d-%H%M%S")
       startTimeStr = datetime.datetime.fromtimestamp(int(start)).strftime("%Y-%m-%d_%H%M%S") # added 19/08
       endTimeStr = datetime.datetime.fromtimestamp(int(end)).strftime("%Y-%m-%d_%H%M%S") # added 19/08
       with open(startTimeStr + 'to' + endTimeStr + '-.csv', 'w', newline='') as fp:
              a = csv.writer(fp, delimiter=',')
              a.writerows(data)


def update_data(pad):
        dickory = time.time() - pad.sessionStartT
        pad.data.append([pad.sessionStartT, pad.trial, dickory,
                         pad.thisGenre, pad.thisSongChoice,pad.butt_pos,pad.failedAttempt,pad.rewarded,
                         pad.portPressed])
            #, pad.buttonLocation])

       #print(pad.data)
        #pad.trial = pad.trial + 1





# ... its called a dictionary, durrrrrrr
def lookup_port(value):
       if value == 1:
              port = 'n1'
       if value == 2:
              port = 'n2'       
       if value == 3:
              port = 'n3'
       if value == 4:
              port = 'n4'              
       if value == 5:
              port = 'n5'
       if value == 6:
              port = 'n6'
       if value == 7:
              port = 'n7'
       if value == 8:
              port = 'n8'       
       if value == 9:
              port = 'n9'       
       if value == 10:
              port = 'n10'       
       if value == 11:
              port = 'n11'       
       if value == 12:
              port = 'n12'      
       if value == 13:
              port = 'n13'      
       if value == 14:
              port = 'n14'      
       if value == 15:
              port = 'n15'      
       if value == 16:
              port = 'n16'               
           
       return port


def disable_all_buttons(ob):

       # ob.ids.top.background_color = (0.1, 1, 0.1, 0.00)
       # ob.ids.bottom.background_color = (0.1, 1, 0.1, 0.00)
       # ob.ids.middle.background_color = (0.1, 1, 0.1, 0.00)

       ob.ids.n1.disabled = True
       ob.ids.n2.disabled = True
       ob.ids.n3.disabled = True

def enable_all_buttons(ob):

       # ob.ids.top.background_color = (0.1, 1, 0.1, 0.00)
       # ob.ids.bottom.background_color = (0.1, 1, 0.1, 0.00)
       # ob.ids.middle.background_color = (0.1, 1, 0.1, 0.00)

       ob.ids.n1.disabled = False
       ob.ids.n2.disabled = False
       ob.ids.n3.disabled = False

time.time()

def randomize_buttons_layouts(self,pad,rint):
    if rint == 1 :
        self.ids.n1.on_press = partial(self.turn_on_rock,pad)
        self.ids.n1.background_normal = 'zigzag.jpg'
        self.ids.n1.background_down = 'zigzag.jpg'
        self.ids.n2.on_press = partial(self.turn_off,pad)
        self.ids.n2.background_normal = 'dots.jpg'
        self.ids.n2.background_down = 'dots.jpg'
        self.ids.n3.on_press = partial(self.turn_on_classical,pad)
        self.ids.n3.background_normal = 'stripes-up.jpg'
        self.ids.n3.background_down = 'stripes-up.jpg'
    elif rint == 2 :
        self.ids.n1.on_press = partial(self.turn_on_rock,pad)
        self.ids.n1.background_normal = 'zigzag.jpg'
        self.ids.n1.background_down = 'zigzag.jpg'
        self.ids.n2.on_press = partial(self.turn_on_classical,pad)
        self.ids.n2.background_normal = 'stripes-up.jpg'
        self.ids.n2.background_down = 'stripes-up.jpg'
        self.ids.n3.on_press = partial(self.turn_off,pad)
        self.ids.n3.background_normal = 'dots.jpg'
        self.ids.n3.background_down = 'dots.jpg'
    elif rint == 3 :
        self.ids.n1.on_press = partial(self.turn_off,pad)
        self.ids.n1.background_normal = 'dots.jpg'
        self.ids.n1.background_down = 'dots.jpg'
        self.ids.n2.on_press = partial(self.turn_on_rock,pad)
        self.ids.n2.background_normal = 'zigzag.jpg'
        self.ids.n2.background_down = 'zigzag.jpg'
        self.ids.n3.on_press = partial(self.turn_on_classical,pad)
        self.ids.n3.background_normal = 'stripes-up.jpg'
        self.ids.n3.background_down = 'stripes-up.jpg'
    elif rint == 4 :
        self.ids.n1.on_press = partial(self.turn_off,pad)
        self.ids.n1.background_normal = 'dots.jpg'
        self.ids.n1.background_down = 'dots.jpg'
        self.ids.n2.on_press = partial(self.turn_on_classical,pad)
        self.ids.n2.background_normal = 'stripes-up.jpg'
        self.ids.n2.background_down = 'stripes-up.jpg'
        self.ids.n3.on_press = partial(self.turn_on_rock,pad)
        self.ids.n3.background_normal = 'zigzag.jpg'
        self.ids.n3.background_down = 'zigzag.jpg'
    elif rint == 5 :
        self.ids.n1.on_press = partial(self.turn_on_classical,pad)
        self.ids.n1.background_normal = 'stripes-up.jpg'
        self.ids.n1.background_down = 'stripes-up.jpg'
        self.ids.n2.on_press = partial(self.turn_on_rock,pad)
        self.ids.n2.background_normal = 'zigzag.jpg'
        self.ids.n2.background_down = 'zigzag.jpg'
        self.ids.n3.on_press = partial(self.turn_off,pad)
        self.ids.n3.background_normal = 'dots.jpg'
        self.ids.n3.background_down = 'dots.jpg'
    elif rint == 6 :
        self.ids.n1.on_press = partial(self.turn_on_classical,pad)
        self.ids.n1.background_normal = 'stripes-up.jpg'
        self.ids.n1.background_down = 'stripes-up.jpg'
        self.ids.n2.on_press = partial(self.turn_off,pad)
        self.ids.n2.background_normal = 'dots.jpg'
        self.ids.n2.background_down = 'dots.jpg'
        self.ids.n3.on_press = partial(self.turn_on_rock,pad)
        self.ids.n3.background_normal = 'zigzag.jpg'
        self.ids.n3.background_down = 'zigzag.jpg'

       

def disable_grid(ob, pad):
    ob.ids.n1.background_normal = 'grayBkgd.png'
    ob.ids.n1.background_down = 'grayBkgd.png'
    ob.ids.n1.on_press = partial(ob.empty_touch, ob.ids.n1.marker, pad)
    ob.ids.n2.background_normal = 'grayBkgd.png'
    ob.ids.n2.background_down = 'grayBkgd.png'
    ob.ids.n2.on_press = partial(ob.empty_touch, ob.ids.n2.marker,pad)
    ob.ids.n3.background_normal = 'grayBkgd.png'
    ob.ids.n3.background_down = 'grayBkgd.png'
    ob.ids.n3.on_press = partial(ob.empty_touch, ob.ids.n3.marker,pad)
    ob.ids.n4.background_normal = 'grayBkgd.png'
    ob.ids.n4.background_down = 'grayBkgd.png'
    ob.ids.n4.on_press = partial(ob.empty_touch, ob.ids.n4.marker,pad)
    ob.ids.n5.background_normal = 'grayBkgd.png'
    ob.ids.n5.background_down = 'grayBkgd.png'
    ob.ids.n5.on_press = partial(ob.empty_touch, ob.ids.n5.marker,pad)
    ob.ids.n6.background_normal = 'grayBkgd.png'
    ob.ids.n6.background_down = 'grayBkgd.png'
    ob.ids.n6.on_press = partial(ob.empty_touch, ob.ids.n6.marker,pad)
    ob.ids.n7.background_normal = 'grayBkgd.png'
    ob.ids.n7.background_down = 'grayBkgd.png'
    ob.ids.n7.on_press = partial(ob.empty_touch, ob.ids.n7.marker,pad)
    ob.ids.n8.background_normal = 'grayBkgd.png'
    ob.ids.n8.background_down = 'grayBkgd.png'
    ob.ids.n8.on_press = partial(ob.empty_touch, ob.ids.n8.marker,pad)
    ob.ids.n9.background_normal = 'grayBkgd.png'
    ob.ids.n9.background_down = 'grayBkgd.png'
    ob.ids.n9.on_press = partial(ob.empty_touch, ob.ids.n9.marker,pad)


   #  ob.ids.n1.background_color = (0.1, 1, 0.1, 0.00)
   # ob.ids.n2.background_color = (0.1, 1, 0.1, 0.00)
   # ob.ids.n3.background_color = (0.1, 1, 0.1, 0.00)
   # ob.ids.n4.background_color = (0.1, 1, 0.1, 0.00)
   # ob.ids.n5.background_color = (0.1, 1, 0.1, 0.00)
   # ob.ids.n6.background_color = (0.1, 1, 0.1, 0.00)
   # ob.ids.n7.background_color = (0.1, 1, 0.1, 0.00)
   # ob.ids.n8.background_color = (0.1, 1, 0.1, 0.00)
   # ob.ids.n9.background_color = (0.1, 1, 0.1, 0.00)


#handlers = {"date:"
            #"trials:"
            #"iti:"
            #"timeout:"
            #"delay:"
            #"samples:"
            #"choices:"
            #}
            
            
def parse_params(inputfile):                                               
       
       d = {}
              
       for line in inputfile:
              splt = str.split(line)
              if (len(splt)>2):
                     d[splt[0]] = splt[1-len(splt):]              
              else:
                     d[splt[0]] = splt[1]
       return d







def globalize(pdict):

#    global dLen

    timeout = float(pdict['timeout:'])
    hold = float(pdict['holdingTime:'])

    top = pdict['topButton:']
    middle = pdict['middleButton:']
    bottom = pdict['bottomButton:']

    maxTrials = float(pdict['trials:'])
    testingTrials = float(pdict['test_trials:'])


    return timeout, hold, top, middle, bottom, maxTrials, testingTrials

