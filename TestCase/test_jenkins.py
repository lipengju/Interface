#coding:utf-8

'''
使用requests实现jenkins的所有get请求方法
序列化：python dict-->json
反序列化：json->python dict
'''

import  requests
from requests.auth import HTTPBasicAuth
import unittest
import  json

class JenkinsTestCase(unittest.TestCase):
	def setUp(self):
		self.build_job_url='http://localhost:8080/jenkins/job/check_python_version/build'
		self.disable_job_url='http://localhost:8080/jenkins/job/check_python_version/disable'
		self.enable_job_url='http://localhost:8080/jenkins/job/check_python_version/enable'
		self.job_url='http://localhost:8080/jenkins/job/check_python_version/api/json?pretty=true'

	def test_get_all_job(self):
		'''GET:http://localhost:8080/jenkins/api/json'''
		json_result=requests.get('http://localhost:8080/jenkins/api/json',auth=('admin','admin')).json()
		self.assertEqual(json_result['jobs'][0]['name'],'app')
		self.assertEqual(json_result['jobs'][0]['url'],'http://localhost:8080/jenkins/job/app/')

	def test_get_all_job_names(self):
		'''GET:http://localhost:8080/jenkins/api/json?tree=jobs[name]'''
		r=requests.get('http://localhost:8080/jenkins/api/json?tree=jobs[name]')
		result=r.text
		json_result=json.loads(result)
		self.assertEqual(json_result['jobs'][0]['name'],'app')
		self.assertEqual(json_result['jobs'][-1]['name'],'check_python_version')

	def test_get_all_job_name_sample_way(self):
		'''GET:http://localhost:8080/jenkins/api/json?tree=jobs[name]简洁版'''
		json_result=requests.get('http://localhost:8080/jenkins/api/json?tree=jobs[name]').json()
		self.assertEqual(json_result['jobs'][0]['name'],'app')
		self.assertEqual(json_result['jobs'][-1]['name'],'check_python_version')

	def test_get_all_job_name_url(self):
		'''GET:http://localhost:8080/jenkins/api/json?tree=jobs[name,url]'''
		json_result=requests.get('http://localhost:8080/jenkins/api/json',auth=('admin','admin')).json()
		self.assertEqual(json_result['jobs'][0]['name'],'app')
		self.assertEqual(json_result['jobs'][-1]['url'],'http://localhost:8080/jenkins/job/check_python_version/')

	def test_post_build_check_python_version(self):
		#执行job接口
		'''POST:http://localhost:8080/jenkins/job/check_python_version/build'''
		r=requests.post(self.build_job_url,data={},auth=('admin','admin'))
		self.assertEqual(r.status_code,201)
		t.sleep(12)

	def test_post_check_python_version_disable(self):
		#禁用job
		'''POST:http://localhost:8080/jenkins/job/check_python_version/disable'''
		self.assertTrue(self.get_job_status())
		r=requests.post(self.disable_job_url,data={},auth=('admin','admin'))
		self.assertEqual(r.status_code,200)
		self.assertFalse(self.get_job_status())
		requests.post(self.enable_job_url,data={},auth=('admin','admin'))

	def test_post_check_python_version_enable(self):
		#启用job
		'''POST:http://localhost:8080/jenkins/job/check_python_version/enable'''
		self.assertTrue(self.get_job_status())
		requests.post(self.disable_job_url,data={},auth=('admin','admin'))
		self.assertFalse(self.get_job_status())
		requests.post(self.enable_job_url,data={},auth=('admin','admin'))
		self.assertTrue(self.get_job_status())

	def get_job_status(self):
		json_info=requests.get(self.job_url,auth=('admin','admin')).json()
		return json_info['buildable']

	def tearDown(self):
		pass

if __name__=='__main__':
	unittest.main(verbosity=2)