# -*- coding: utf-8 -*-
"""
Created on Thu May 13 16:30:27 2021

@author: HP
"""
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.clock import Clock
import matplotlib.pyplot as mat
from datetime import datetime


####UsefulFunc
def convertToTimeFormat(integer):
    arr = [str(integer//3600), str(integer//60), str(integer%60)]
    res = ""
    for i in range(len(arr)):
        res += (len(arr[i]) == 1)*"0" + arr[i] + ":" * (i!= len(arr) -1)
    return res

####Kivy
class MainScreen(Screen):
    pass
class Graphs(Screen):
    pass
    
class DetailedInfos(Screen):
    pass


class MyApp(App):
    count = 0
    pauseCount = 0
    totalPauseTime = 0
    dateOfStart = "None"
    activity = "None"
    pauseActivity = "None"
    last = 0
    started = False
    paused = False
    pausesNumber = 0
    def init(self):
        self.count = 0
        self.pauseCount = 0
        self.totalPauseTime = 0
        self.dateOfStart = "None"
        self.activity = "None"
        self.pauseActivity = "None"
        self.last = 0
        self.started = False
        self.paused = False
        self.pausesNumber = 0  
        
    
    
    def saveData(self, date, act, time, pt, pn):
        with open(str(date) + ".txt", "a+") as txt:
            content = txt.readlines()
        
        with open(str(date) + ".txt", "a") as txt:
            if act in content: 
                pass
            else: txt.writelines(act + "\n" + str(time) + "\n" + str(pt) + "\n" + str(pn) +"\n")
        #To renitialize variables
        self.init()

    def saveTempData(self, pa, last):
        pass
    
    #To start and end
    def strBtn(self):
        self.started = not self.started
        if not self.started:
            self.saveData(self.dateOfStart, self.activity,self.count, self.totalPauseTime, self.pausesNumber)
        else: self.dateOfStart = datetime.today().date()
            
        
    #To manage pauses
    def pauseBtn(self):
        self.paused = not self.paused
        self.pausesNumber += (self.paused)
        self.totalPauseTime += (not self.paused) * self.pauseCount
        self.last = self.pauseCount
    
    def pauseActBtn(self):
        self.pauseActivity = (self.root.ids.pauseActInput.text)
        self.saveTempData(self.pauseActivity, self.last)
        
    def actBtn(self):
        self.activity = (self.root.ids.actInput.text)
        
    def build(self):
       self.myLabel = Label(text = "00:00:00")
       self.startButton = Button(text ="00:00:00")
       self.pauseText = Label(text = "00:00:00")
       self.pauseButton = Button(text ="pause")
       self.pauseInfo = Label(text = "0")
       self.totalPauseText = Label(text = "0")
       Clock.schedule_interval(self.CountingSec, 1)
       Clock.schedule_interval(self.UpdatingTexts, 0.1)
       #Screen Manager and adding
       sm = ScreenManager()
       sm.add_widget(MainScreen(name='main'))
       sm.add_widget(Graphs(name='graphs'))
       
       return sm
   
    def CountingSec(self, dt):
        self.count = (self.count + 1* (not self.paused))*(self.started)
        self.pauseCount = (self.pauseCount + 1)*(self.paused)
    
    def UpdatingTexts(self, dt):
        self.myLabel.text = convertToTimeFormat(self.count)
        self.pauseText.text = convertToTimeFormat(self.pauseCount)
        self.pauseButton.text = "Continue"*(self.started)*(self.paused) + "Pause"*(self.started)*(not self.paused)
        self.startButton.text = "Start"*(not self.started) + "Stop"*self.started
        self.pauseInfo.text = str(self.pausesNumber)
        self.totalPauseText.text = convertToTimeFormat(self.totalPauseTime)
        
if __name__ == "__main__":
    MyApp().run()

    
    
    