#from kivy.graphics import Color
import csv
import time
import datetime # added 19/08

from kivy.graphics.context_instructions import Color




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

       ob.ids.top.disabled = True
       ob.ids.bottom.disabled = True
       ob.ids.middle.disabled = True

def enable_all_buttons(ob):

       # ob.ids.top.background_color = (0.1, 1, 0.1, 0.00)
       # ob.ids.bottom.background_color = (0.1, 1, 0.1, 0.00)
       # ob.ids.middle.background_color = (0.1, 1, 0.1, 0.00)

       ob.ids.top.disabled = False
       ob.ids.bottom.disabled = False
       ob.ids.middle.disabled = False

time.time()




       
       


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

    top = pdict['topButton:']
    middle = pdict['middleButton:']
    bottom = pdict['bottomButton:']


    return timeout, top, middle, bottom
