from tkinter import Entry, Frame, Tk, Label, Button
from tkinter.constants import LEFT
from win10toast import ToastNotifier #Module for calling Windows notifications
from pathlib import Path #Module for working with paths

class pomodoro():

    def __init__(self):
        self.path = Path(__file__).parent.absolute() #Get the absolute path to the directory of the current file
        self.toaster = ToastNotifier()
        self.window = Tk()
        self.timer = [0, 0] #List for keeping and calculating minutes and seconds (timer [0] - minutes, timer [1] - seconds)
        self.pomodorocount = 0 #Variable for storing performed pomodoros
        self.status = 1 #Variable for determining the state (0 - work, 1 - short break, 2 - long break)
        self.after_id = 0 #Variable to storing the identifier of the after method (to stop the timer, we will transmit this identifier to the after_cancel method)
        self.timestr = str(self.timer[0]) + ':' + str(self.timer[1]) #Variable type str to update label_time
        self.window.title('Pomodoro Timer')
        self.window.geometry('400x400')
        self.label_work = Label(text='Pomodoro')
        self.frame_work = Frame() #Used to group widgets
        self.entry_m_work = Entry(self.frame_work, width=5)
        self.entry_s_work = Entry(self.frame_work, width=5)
        text = '25'
        self.entry_m_work.insert(0, text) #We prescribe the initial values in the input field
        text = '0'
        self.entry_s_work.insert(0, text)
        self.label_relax = Label(text='Short break')
        self.frame_relax = Frame()
        self.entry_m_relax = Entry(self.frame_relax, width=5)
        self.entry_s_relax = Entry(self.frame_relax, width=5)
        text = '5'
        self.entry_m_relax.insert(0, text)
        text = '0'
        self.entry_s_relax.insert(0, text)
        self.label_longrelax = Label(text='Long break')
        self.frame_longrelax = Frame()
        self.entry_m_longrelax = Entry(self.frame_longrelax, width=5)
        self.entry_s_longrelax = Entry(self.frame_longrelax, width=5)
        text = '30'
        self.entry_m_longrelax.insert(0, text)
        text = '0'
        self.entry_s_longrelax.insert(0, text)
        self.label_infopomodoro = Label(text='Number of pomodoros: {}'.format(self.pomodorocount), font=("Times", 20))
        self.label_infostatus = Label(text='Get started!', fg = "blue", font=("Times", 20))
        self.label_time = Label(text='0:0', font=("Area", 100))
        self.frame_button = Frame()
        self.button_start = Button(self.frame_button, width=5, text='Start', command=self.start)
        self.button_reset = Button(self.frame_button, width=5, text='Reset', command=self.reset, state='disabled')

    def pack(self):
        #Use the pack method for widgets in this function 
        self.label_work.pack()
        self.frame_work.pack()
        self.entry_m_work.pack(side=LEFT)
        self.entry_s_work.pack(side=LEFT)
        self.label_relax.pack()
        self.frame_relax.pack()
        self.entry_m_relax.pack(side=LEFT)
        self.entry_s_relax.pack(side=LEFT)
        self.label_longrelax.pack()
        self.frame_longrelax.pack()
        self.entry_m_longrelax.pack(side=LEFT)
        self.entry_s_longrelax.pack(side=LEFT)
        self.label_infopomodoro.pack()
        self.label_infostatus.pack()
        self.label_time.pack()
        self.frame_button.pack()
        self.button_start.pack(side=LEFT)
        self.button_reset.pack(side=LEFT)

    def start(self):
        #The function is called by pressing the Start button
        self.button_start.configure(state='disabled')
        self.button_reset.configure(state='active')
        self.status_check()

    def tick(self):
        #Timer update function
        self.timer[1] -= 1 #We subtract one second
        if self.timer[1] == -1: #When the value becomes -1:
            self.timer[1] = 59 #Set the value of seconds in 59
            self.timer[0] -= 1 #We subtract one minute
        self.timestr = str(self.timer[0]) + ':' + str(self.timer[1]) #We combine values from the list to the timestr variable in the form of 0:0
        self.label_time.configure(text=self.timestr) #We update the label
        self.status_check() #Call the check function

    def status_check(self):
        #Status check function (work or break)
        if self.timestr == '0:0': #Checking whether the timer time ended
            if self.status == 0: #If you work
                self.pomodorocount += 1 #Add 1 to performed pomodoros
                self.label_infopomodoro.configure(text='Number of pomodoros: {}'.format(self.pomodorocount), font=("Times", 20)) #We update the label
                if self.pomodorocount % 4 == 0: #If the number of pomodoros is multiple 4
                    self.status = 2 #We update status in 2 (long break)
                    self.status_change() #Call the status change function
                else:
                    self.status = 1 #We update status in 1 (short break)
                    self.status_change() #Call the status change function
            elif self.status == 1 or self.status == 2: #If we break
                self.status = 0 #We update status in 0 (work)
                self.status_change() #Call the status change function
        else:
            self.after_id = self.label_time.after(1000, self.tick) #If the time did not end, call the after method to execute the tick function every second

    def status_change(self):
        #Status change function (check the value in the status variable) 
        if self.status == 0: #Work
            #Show notification + we prescribe an absolute path to the timer.ico icon (due to lying next to the current file)
            self.toaster.show_toast("Pomodoro Timer", "Time for work!", threaded=True, icon_path='{}\\timer.ico'.format(self.path)) 
            self.label_infostatus.configure(text='Time for work!', fg = "red", font=("Times", 20)) #We update the label with the status
            self.timer[0] = int(self.entry_m_work.get()) #Record the values of the input fields to the timer list
            self.timer[1] = int(self.entry_s_work.get())
        elif self.status == 1: #Short break
            self.toaster.show_toast("Pomodoro Timer", "Time for short break!", threaded=True, icon_path='{}\\timer.ico'.format(self.path))
            self.label_infostatus.configure(text='Time for short break!', fg = "green", font=("Times", 20))
            self.timer[0] = int(self.entry_m_relax.get())
            self.timer[1] = int(self.entry_s_relax.get())
        elif self.status == 2: #Long break
            self.toaster.show_toast("Pomodoro Timer", "Time for long break!", threaded=True, icon_path='{}\\timer.ico'.format(self.path))
            self.label_infostatus.configure(text='Time for long break!', fg = "lime", font=("Times", 20))
            self.timer[0] = int(self.entry_m_longrelax.get())
            self.timer[1] = int(self.entry_s_longrelax.get())
        if self.timer[1] > 60: #If in the input field of seconds it was a value of more than 60, then set the value of 60
            self.timer[1] = 60
        if self.timer[1] == 0: #If there was zero in the input field in the input field, then we subtract out of 1 minutes and set the value of seconds in 60
            self.timer[0] -= 1
            self.timer[1] = 60
        self.after_id = self.label_time.after(1000, self.tick) #Call an after method for executing the tick function every second 

    def reset(self):
        #Timer restart function - set the initial values of variables, update labels and buttons 
        self.button_reset.configure(state='disabled')
        self.label_time.after_cancel(self.after_id) #Stop the timer for the after identifier
        self.timer = [0, 0]
        self.pomodorocount = 0
        self.status = 1
        self.after_id = 0
        self.timestr = str(self.timer[0]) + ':' + str(self.timer[1])
        self.label_time.configure(text=self.timestr)
        self.button_start.configure(state='active')
        self.label_infopomodoro.configure(text='Number of pomodoros: {}'.format(self.pomodorocount), font=("Times", 20))
        self.label_infostatus.configure(text='Get started!', fg = "blue", font=("Times", 20))

    def mainloop(self):
        self.window.mainloop()

window = pomodoro()
window.pack()
window.mainloop()
