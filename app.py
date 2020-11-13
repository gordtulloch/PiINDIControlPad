import tkinter as tk
import pytz
from datetime import datetime
import socket
import PyIndi
import time

class IndiClient(PyIndi.BaseClient):
    def __init__(self):
        super(IndiClient, self).__init__()
    def newDevice(self, d):
        global dmonitor
        # We catch the monitored device
        dmonitor=d
    def newProperty(self, p):
        global monitored
        global cmonitor
        # we catch the "CONNECTION" property of the monitored device
        if (p.getDeviceName()==monitored and p.getName() == "CONNECTION"):
            cmonitor=p.getSwitch()
    def removeProperty(self, p):
        pass
    def newBLOB(self, bp):
        pass
    def newSwitch(self, svp):
        pass
    def newNumber(self, nvp):
        global newval
        global prop
        # We only monitor Number properties of the monitored device
        prop=nvp
        newval=True
    def newText(self, tvp):
        pass
    def newLight(self, lvp):
        pass
    def newMessage(self, d, m):
        pass
    def serverConnected(self):
        pass
    def serverDisconnected(self, code):
        pass

# Mkhrs takes a time float number in and returns a formatted string as HH:MM:SS
def mkhrs(time):
  hours = int(time)
  minutes = (time*60) % 60
  seconds = (time*3600) % 60
  outstring = "%d:%02d:%02d" % (hours, minutes, seconds)
  return outstring

# nextObject reads a line from a tour.txt file and slews the telescope to that object
def prevObject():
    # to come
    return
    
# nextObject reads a line from a tour.txt file and slews the telescope to that object
def nextObject():
    # to come
    return

# Set up tkinter
root=tk.Tk()
root.configure(background='black')
# Uncomment this line to get fullscreen (a pain when debugging on a PC!)
#root.wm_attributes('-fullscreen','true')

# Set up INDI
monitored="Telescope Simulator"
dmonitor=None
cmonitor=None

indiclient=IndiClient()
indiclient.setServer("localhost",7624)

# we are only interested in the telescope device properties
indiclient.watchDevice(monitored)
indiclient.connectServer()

# wait CONNECTION property be defined
while not(cmonitor):
    time.sleep(0.05)

# if the monitored device is not connected, we do connect it
if not(dmonitor.isConnected()):
    # Property vectors are mapped to iterable Python objects
    # Hence we can access each element of the vector using Python indexing
    # each element of the "CONNECTION" vector is a ISwitch
    cmonitor[0].s=PyIndi.ISS_ON  # the "CONNECT" switch
    cmonitor[1].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
    indiclient.sendNewSwitch(cmonitor) # send this new value to the device

# Determine our IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
  # doesn't even have to be reachable
  s.connect(('10.255.255.255', 1))
  IP = s.getsockname()[0]
except:
  IP = '127.0.0.1'
finally:
  s.close()

# Set up grid
root.geometry("480x320")
for x in range(4):
    tk.Grid.columnconfigure(root, x, weight=1)
tk.Grid.rowconfigure(root, 2, weight=1)
tk.Grid.rowconfigure(root, 3, weight=1)
tk.Grid.rowconfigure(root, 4, weight=1)
tk.Grid.rowconfigure(root, 5, weight=1)
tk.Grid.rowconfigure(root, 6, weight=1)

# Top row
currDateText = tk.Label(root, text="", anchor="w") 
currDateText.configure(font='helvetica 12', fg='white', bg='black')
currDateText.grid(row=0, column=0, sticky="nsew")
currTimeText = tk.Label(root, text="", anchor="w") 
currTimeText.configure(font='helvetica 12', fg='white', bg='black')
currTimeText.grid(row=1, column=0, sticky="nsew")
currStatusText = tk.Label(root, text="", anchor="e") 
currStatusText.configure(font='helvetica 12', fg='white', bg='black')
currStatusText.grid(row=0, column=3, sticky="nsew")

# Middle Rows
currObjText = tk.Label(root, text="") 
currObjText.configure(font='helvetica 24', fg='white', bg='black')
currObjText.grid(row=2, column=0, columnspan=4, sticky="nsew")
currRAText = tk.Label(root, text="") 
currRAText.configure(font='helvetica 24', fg='white', bg='black')
currRAText.grid(row=3, column=0, columnspan=4, sticky="nsew")
currDECText = tk.Label(root, text="") 
currDECText.configure(font='helvetica 24', fg='white', bg='black')
currDECText.grid(row=4, column=0, columnspan=4,sticky="nsew")

# Buttons
nextButton=tk.Button(root, text="Next", command=nextObject(), fg='white', bg='black', padx=2, highlightbackground='white', highlightthickness=2, highlightcolor="black")
nextButton.grid(row=6, column=1, sticky="nsew")
nextButton=tk.Button(root, text="Prev", command=prevObject(), fg='white', bg='black', padx=2, highlightbackground='white', highlightthickness=2, highlightcolor="black")
nextButton.grid(row=6, column=2, sticky="nsew")

# Bottom Rows
currUTDateText = tk.Label(root, text="", anchor="w") 
currUTDateText.configure(font='helvetica 12', fg='white', bg='black')
currUTDateText.grid(row=7, column=0, sticky="nsew")
currUTTimeText = tk.Label(root, text="", anchor="w") 
currUTTimeText.configure(font='helvetica 12', fg='white', bg='black')
currUTTimeText.grid(row=8, column=0, sticky="nsew")
currIPText = tk.Label(root, text=IP, anchor="e") 
currIPText.configure(font='helvetica 12', fg='white', bg='black')
currIPText.grid(row=8, column=3, sticky="nsew")

# ************************ MAINLINE **************************
utc = pytz.utc
newval=False
prop=None
nrecv=0
currObjText.configure(text="Object: Unknown")

while (1):
    if (newval):
      if prop.name == "EQUATORIAL_EOD_COORD":
        for n in prop:
          if n.name == "RA":
             currRA =  n.value
          else:
             currDEC = n.value
        dateTimeObj = datetime.now()
        currDateText.configure(text=dateTimeObj.strftime("%d-%b-%Y"))
        currTimeText.configure(text=dateTimeObj.strftime("%H:%M:%S"))
        dateTimeObj = datetime.now(tz=utc)
        currUTDateText.configure(text=dateTimeObj.strftime("%d-%b-%Y"))
        currUTTimeText.configure(text=dateTimeObj.strftime("%H:%M:%S")+" UT")
        currRAText.configure(text="RA: "+mkhrs(currRA))
        currDECText.configure(text="DEC: "+str(currDEC))
        currStatusText.configure(text="TRACKING")
        root.update_idletasks()
        root.update()
        newval=False


