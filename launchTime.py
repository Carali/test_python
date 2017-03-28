#/usr/bin/python
#encoding:utf-8
import csv
import os
import time

class App(object):
    def __init__(self):
        self.content= ""
        self.startTime=0
        cmd_init = 'adb root'
        os.popen(cmd_init)
    def launchApp(self):
        cmd =  'adb shell am start -W -n com.mobicloud.assistant/.Activity'
        self.content=os.popen(cmd)
    def stopApp(self):
        cmd = 'adb shell am force-stop com.mobicloud.assistant'
        #cmd = 'adb shell input keyevent 3'
        os.popen(cmd)
    def getLaunchedTime(self):
        for line in self.content.readlines():
            if "ThisTime" in line:
                self.startTime = line.split(":")[1]
                break
        return self.startTime


# 控制类


class Controller(object):

    def __init__(self,count):
        self.app = App()
        self.counter = count
        self.alldata=[("timestamp","elapsedTime")]

    def testProcess(self):
        self.app.launchApp()
        time.sleep(5)
        elpasedTime = self.app.getLaunchedTime()
        self.app.stopApp()
        time.sleep(3)
        currentTime = self.getCurrentTime()
        self.alldata.append(( currentTime,elpasedTime ))

    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        return currentTime

    def run(self):
        while self.counter > 0:
            self.testProcess()
            self.counter = self.counter -1


    def saveDataToCSV(self):
        csvfile= file('startTime.csv','wb')
        writer=csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()

    if __name__=="__main__":
        controller = Controller(10)
        controller.run()
        controller.saveDataToCSV()



