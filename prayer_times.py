import json
import urllib2
import re
import Tkinter as tk
import datetime as dt
api_ep = "http://api.aladhan.com/timingsByCity?city=Glenolden&state=Pennsylvania&country=US&method=2"

time_pattern = re.compile("(\d+):(\d+)")


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



    
class mywindow(tk.Tk):
    def __init__(self):
       self.root = tk.Tk.__init__(self)
       self.update()
       
    def update(self):
           self.timings = getDictOfTimes()
           self.prayer_labels = []
           self.timing_labels = []
           self.keys = list(self.timings.keys())
           self.values = list(self.timings.values())
           for x in range(1 ,len(self.timings) + 1):
               cur1_label = tk.Label(self.root, text = self.keys[x-1])
               cur1_label.grid(column=0, row=x, sticky=tk.W)
               self.prayer_labels.append(cur1_label)
           
               cur2_label = tk.Label(self.root, text = conv24to12fmt(self.values[x-1]))
               cur2_label.grid(column=1, row=x)
               self.timing_labels.append(cur2_label)
           self.prayer_title = tk.Label(self.root,text="Prayer",fg="blue",font="Verdana 11")
           self.prayer_title.grid(row=0,column=0)

           self.timings_title = tk.Label(self.root,text="Time",fg="blue",font="Verdana 11")
           self.timings_title.grid(row=0,column=1)

           # self.timeleft_title = tk.Label(self.root, text="\n\n\nTime Left", font="Verdana 11")
           # self.timeleft_title.grid(row=8, column=0)
           
def main():           
	a = mywindow()
	a.mainloop()
       
if __name__ == "__main__":
	main()
        
        


    




