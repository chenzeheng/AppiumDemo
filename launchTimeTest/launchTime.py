#!/usr/bin/env python
# encoding: utf-8
import csv
import  os
#app类
import time

from openpyxl.compat import file


class App(object):
	def __init__(self):
		self.content=""
		self.startTime=0
	#启动app
	def launchAPP(self):
		cmd='adb shell am start -W -n com.android.browser/.BrowserActivity'
		self.content=os.popen(cmd)
	#停止app
	def StopApp(self):
		cmd='adb shell am force-stop  com.android.browser'
		os.popen(cmd)
	#获取启动时间
	def GetlaunchedTime(self):
		for line in self.content.readlines():
			if "ThisTime" in line:
				self.startTime=line.split(":")[1]
				break
		return self.startTime
#控制类
class Controller(object):
	def __init__(self,count):
		self.app= App()
		self.counter=count
		self.alldata=[("timestamp","elapsedtime")]
	#单次测试
	def testprocess(self):
		self.app.launchAPP()
		time.sleep(5)
		elpasedtime=self.app.GetlaunchedTime()
		self.app.StopApp()
		time.sleep(3)
		currentTime=self.getCurrentTime()
		self.alldata.append((currentTime,elpasedtime))
	#多次执行测试过程
	def run(self):
		while self.counter>0:
			self.testprocess()
			self.counter=self.counter-1
			
	#获取当前时间戳
	def getCurrentTime(self):
		currentTime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		return currentTime
	#数据存储
	def SaveDataToCSV(self):
		csvfile=open('startTime.csv','w')
		writer=csv.writer(csvfile)
		writer.writerows(self.alldata)
		csvfile.close()
	
if __name__ == "__main__":
	controller=Controller(10)
	controller.run()
	controller.SaveDataToCSV()
