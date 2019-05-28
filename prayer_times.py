import time
import threading
import json
import urllib2
import re
import Tkinter as tk
import datetime as dt
api_ep = "http://api.aladhan.com/timingsByCity?city=Glenolden&state=Pennsylvania&country=US&method=2"

time_pattern = re.compile("(\d+):(\d+)")

PRAYER_NAMES = ["Fajr","Dhuhr","Asr","Maghrib","Isha"]

def getDictOfTimes():
    data = urllib2.urlopen(api_ep)
    json_data = json.loads(data.read())
    timings = {}
    timings["Fajr"] = json_data['data']['timings']['Fajr']
    timings["Dhuhr"] = json_data['data']['timings']['Dhuhr']
    timings["Asr"] = json_data['data']['timings']['Asr']
    timings["Maghrib"] = json_data['data']['timings']['Maghrib']
    timings["Isha"] = json_data['data']['timings']['Isha']
    return timings

def conv24to12fmt(time_val):
    noon_flag = "a.m"
    matches = time_pattern.findall(time_val)
    hours, minutes = matches[0]
    hours, minutes = int(hours), int(minutes)
    if hours > 12:
        hours -= 12
        noon_flag = "p.m"
    return "%d:%02d %s" % (hours, minutes, noon_flag)


def get_time_as_string():
    str_time = time.strftime("%H:%M")
    return str_time

def get_next_prayer_time(timing_dict):
    current_time = get_time_as_string()
    prayer_name = "Fajr" 
    for key in PRAYER_NAMES:
	#print str(current_time) + " > " + str(timing_dict[key]) + "is " + str(current_time > timing_dict[key])
	if current_time > timing_dict[key]:
	    prayer_name = key
    	    break
    return prayer_name 

def time_until_maghrib(timing_dict):
	current_time = get_time_as_string()
	maghrib_time = timing_dict["Maghrib"]
	if current_time > maghrib_time:
		return "You can eat now"
	else:
		return subtract_time(maghrib_time, current_time)


# time1 - time2
def subtract_time(time_str1, time_str2):
	max_time = max([time_str1, time_str2])
	#print "MAXTIME: " + max_time
	min_time = min([time_str1, time_str2])
	#print "MINTIME: " + min_time
	max_hours, max_mins = max_time.split(":")
	min_hours, min_mins = min_time.split(":")

	seconds = int(time.strftime("%S"))
	hours_left = int(max_hours) - int(min_hours)
	mins_left = int(max_mins) - int(min_mins)
	if mins_left < 0:
		hours_left -= 1
		mins_left += 60
	if seconds > 0:
		mins_left -= 1
		seconds = 60 - seconds
	return "\n\n\n%d hrs, %d mins %d secs left" % (hours_left, mins_left, seconds)




def comparable_time(time_val):
    string_pieces = time_val.split(" ")
    hours, mins = string_pieces[0].split(":")
    hours = int(hours)
    mins = int(mins)
    am_pm = string_pieces[1]
    if am_pm == "pm":
	hours += 12
    return (hours)*60 + mins
	
def updating_method(*args):
    gui = args[0]
    while gui.active:
	gui.update_time_left()
	#print "Time Update:"
    	time.sleep(1)



class mywindow(tk.Tk):
    def __init__(self):
       self.root = tk.Tk.__init__(self)
       self.active = True
       self.update()
       
    def update(self):
           self.timings = getDictOfTimes()
           self.prayer_labels = []
           self.timing_labels = []
           self.keys = list(self.timings.keys())
           self.values = list(self.timings.values())
           for y, pname in enumerate(PRAYER_NAMES):
	       x=y+1
               cur1_label = tk.Label(self.root, text = pname)
               cur1_label.grid(column=0, row=x, sticky=tk.W)
               self.prayer_labels.append(cur1_label)
           
               cur2_label = tk.Label(self.root, text = conv24to12fmt(self.timings[pname]))
               cur2_label.grid(column=1, row=x)
               self.timing_labels.append(cur2_label)
           self.prayer_title = tk.Label(self.root,text="Prayer",fg="blue",font="Verdana 11")
           self.prayer_title.grid(row=0,column=0)

           self.timings_title = tk.Label(self.root,text="Time",fg="blue",font="Verdana 11")
           self.timings_title.grid(row=0,column=1)

           self.timeleft_title = tk.Label(self.root, text="\n\n\nTime Left", font="Verdana 11")
           self.timeleft_title.grid(row=8, column=0)

	   self.time_left = tk.Label(self.root, text=time_until_maghrib(self.timings), font="Arial")
	   self.time_left.grid(row=8, column=1)
    def get_timing_labels(self):
    	return self.timing_labels
    
    def update_times(self):
	self.timings = getDictOfTimes()
	self.update()

    def update_time_left(self):
    	self.time_left["text"] = time_until_maghrib(self.timings)
	           
    def deactivate(self):
    	self.active = False
	self.destroy()

def main():           
	a = mywindow()
	clock_thread = threading.Thread(target=updating_method, args =[a])
	a.protocol("WM_DELETE_WINDOW", a.deactivate)
	clock_thread.start()
	timing_labels = a.get_timing_labels()
	timings = a.timings
	#print time_until_maghrib(timings)
	a.mainloop()
if __name__ == "__main__":
	main()
        
        


    




