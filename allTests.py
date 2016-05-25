#coding:utf-8
import  unittest,os,sys,HTMLTestRunner,time
reload(sys)
sys.setdefaultencoding('utf-8')
import  time as t
import  os
from module.Model import Config,DataHelper


config=Config()

#批量获取测试用例
def suite():
	dir_case=unittest.defaultTestLoader.discover(
		config.data_dirs('TestCase'),
		# 'D:/web/zl-webdriver/TestCase',
		pattern='test_*.py',
		top_level_dir=None
	)
	return dir_case


#获取当前的时间
def getNowTime():
	return time.strftime("%Y-%m-%d %H_%M_%S",time.localtime(time.time()))


#执行测试用例，生成测试报告
def runAutomation():
	filename=config.data_dirs('Report')+'/'+getNowTime()+'InterfaceReport.html'
	fp=file(filename,'wb')
	runner=HTMLTestRunner.HTMLTestRunner(
		stream=fp,
		title=u'接口平台自动化测试报告',
		description=''
	)
	runner.run(suite())

#获取最新的自动化测试报告
def newReport():
	lists=os.listdir(Config.report_dirs()+'/')
	lists.sort(key=lambda fn:os.path.getmtime(config.data_dirs('Report')+'/'+"\\"+fn) if not os.path.isdir(config.data_dirs('Report')+'/'+"\\"+fn) else 0)
	print u'接口平台最新的自动化测试报告为：',lists[-1]
	print os.path.join(config.data_dirs('Report')+'/',lists[-1])


#定时执行自动化测试用例
def scheduledTask():
	Flang=True
	while Flang:
		timing=t.strftime('%H_%M',t.localtime(t.time()))
		if timing=='08_48':
			print u'开始执行接口平台自动化测试用例'
			runAutomation()
			newReport()
			print u'执行自动化测试用例已完成，准备退出！'
			break
		else:
			#获取当前时间，每隔5秒打印一次
			t.sleep(5)
			print t.strftime('%H:%M:%S %x',t.localtime(t.time()))

if __name__=='__main__':
	runAutomation()