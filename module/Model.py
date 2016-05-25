#coding:utf-8

import  os
import  xml.dom.minidom
import sqlite3
import  MySQLdb
import  config


class Config(object):
	def __init__(self):
		pass

	def data_dirs(self,filePath):
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		DATA_DIRS = (
		os.path.join(BASE_DIR, filePath),
		)
		d='/'.join(DATA_DIRS)
		return d

class DataHelper(Config):
	def __init__(self):
		pass

	def getList(self):
		list=[['','',u'请您填写手机/邮箱/用户名'],['admin','',u'请您填写密码'],['admin','admin',u'请输入验证码']]
		return list

	def getXmlData(self,value):
		dom=xml.dom.minidom.parse(self.data_dirs('Data-Driver')+"/system.xml")
		db=dom.documentElement
		name=db.getElementsByTagName(value)
		nameValue=name[0]
		return nameValue.firstChild.data

	def getXmlUser(self,parent,child):
		dom=xml.dom.minidom.parse(self.data_dirs('Data-Driver')+"/system.xml")
		db=dom.documentElement
		itemlist=db.getElementsByTagName(parent)
		item=itemlist[0]
		return item.getAttribute(child)

class MySQLHelper(object):
	def __init__(self):
		self.__conn=config.conn

	def selectMySQL(self,index1,index2):
		rows=[]
		try:
			conn=MySQLdb.connect(**self.__conn)
			cur=conn.cursor()
		except Exception,e:
			print u'操作mysql数据库失败'
		else:
			cur.execute('select *  from element')
			data=cur.fetchall()
			for d in data:
				rows.append(d)
			return rows[index1][index2]
		finally:
			cur.close()
			conn.close()

	def get_One(self,sql,params):
		try:
			conn=MySQLdb.connect(**self.__conn)
			cur=conn.cursor()
			reCount=cur.execute(sql,params)
			data=cur.fetchone()
			return data
		except:
			print u'操作数据库失败'
		finally:
			cur.close()
			conn.close()

	def insertMySQL(self,sql,params):
		try:
			conn=MySQLdb.connect(**self.__conn)
			cur=conn.cursor()
			cur.execute(sql,params)
			conn.commit()
		except Exception,e:
			print u'操作mysql数据库失败'
		finally:
			cur.close()
			conn.close()

class User(object):
	def __init__(self):
		self.__helper=MySQLHelper()

	def get_One(self,id):
		sql='select *  from account where id=%s'
		params=(id,)
		return self.__helper.get_One(sql,params)

	def checkValidate(self,name,address):
		sql='select * from account where username=%s and passwd=%s'
		params=(name,address,)
		return self.__helper.get_One(sql,params)

if __name__=='__main__':
	per=MySQLHelper()
	print per.selectMySQL2()




