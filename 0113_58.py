#-*- coding:utf-8 -*-
import requests
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

url = 'http://ndes.csrc.gov.cn/alappl/home/volunteerLift?edCde=300009'
last_query = ()
key_word = u'基金募集'

# main function
def html_query():
	# 获取网页内容并分析
	html_response = requests.get(url).content.decode('utf-8')
	this_query = html_analyze(html_response)
	
	# 与上次查询进行对比，是否有更新
	global last_query
	diff_tuple = tuple(set(this_query).difference(set(last_query)))
	if len(diff_tuple) and len(last_query):
		print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		print len(diff_tuple), " messages are updated."
		key_query = find_key(diff_tuple)
		print "Find", len(key_query), "important message."
		send_email(diff_tuple, key_query)
	last_query = this_query
	return

# 对网页内容进行正则分析的函数，返回一个长度为10的，包含10个title字符串
def html_analyze(content):
	res = r'<.*?titleshow.*?>(.*?)<.*?>'
	ans = re.findall(res, content, re.I|re.S|re.M)
	return tuple(ans)
	
def send_email(html_tuple, msg_tuple):
	# 第三方 SMTP 服务
	mail_host="smtp.163.com"  #设置服务器
	mail_user="shihao1024@163.com"   #用户名
	mail_pass="shihao1992"   #口令

	sender = 'shihao1024@163.com'
	receivers = ['marygmd123@163.com', 'shihao1024@163.com']  # 接收邮件
	subject = "csrc.gov.cn: "+str(len(html_tuple))+" updated, "+str(len(msg_tuple))+" important."
	email_content = 'http://ndes.csrc.gov.cn/alappl/home/gongshi'
	content_row = 0
	for content in msg_tuple:
		content_row += 1
		email_content = email_content + '\n' + str(content_row) + '. ' + content
	
	message = MIMEText(email_content, 'plain', 'utf-8')
	message['From'] = "shihao<shihao1024@163.com>"
	message['To'] =  "guomengdi<marygmd123@163.com>"
	message['Subject'] = Header(subject)

	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
		smtpObj.login(mail_user,mail_pass)
		smtpObj.sendmail(sender, receivers, message.as_string())
		print "send successfully"
	except smtplib.SMTPException:
		print "send unsuccessfully"
	return

# 分析是否含有“基金募集”
def find_key(diff_tuple):
	key_query = []
	for query_content in diff_tuple:
		if not re.search(key_word, query_content):
			key_query.append(query_content)
			print 'find', type(query_content)
	return tuple(key_query)
	
# 网页查询函数
def query_cycle():
	while(1):
		# 间隔时间设置
		time_hour = int(time.strftime('%H',time.localtime(time.time())))
		time_day = int(time.strftime('%w',time.localtime(time.time())))
		if time_hour == 21:
			time_delay = 43200
		elif time_day == 0 or time_day == 6:
			time_delay = 3600
		elif time_hour == 12 or time_hour == 18:
			time_delay = 600
		else:
			time_delay = 3600

		# 查询
		try:
			print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			html_query()
		except requests.exceptions.ConnectionError, ErrorAlert:
			print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			print ErrorAlert
		time.sleep(time_delay)
	return

# 开始查询	
query_cycle()