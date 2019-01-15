#-*- coding:utf-8 -*-
import requests
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

req = requests.session()
url = 'https://rongcheng.58.com/whrcsq/zufang/j3/?PGTID=0d3090a7-046e-413b-b067-6af5194bd063&ClickID=1'
dic = {'&#x9fa4;':1,'&#x9f92;':2,'&#x993c;':3,'&#x9a4b;':4,'&#x9476;':5,'&#x9fa5;':6,'&#x958f;':7,'&#x9e3a;':8,'&#x9f64;':9,'&#x9ea3;':0} 

def html_query():
	html_response = req.get(url).content.decode('utf-8')
	# file_write(html_response)
	# html_response = open('0113.txt', 'r').read()

	res = r'<h2>.*?>\s+(.*?)\s+<.*?</h2>.*?<div class="sendTime">\s+(\S+)\s+</div>.*?<b class="strongbox">(.*?)</b>'
	ans = re.findall(res, html_response, re.I|re.S|re.M)
	for ans_d in ans:
		sendtime = ans_d[1]
		if(sendtime[-3:] == u'分钟前'):
			print sendtime[0:len(sendtime)-3]
			if(int(sendtime[0:len(sendtime)-3]) < 20):
				print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				send_email(', '.join(ans_d))
	return

def send_email(msg):
	# 第三方 SMTP 服务
	mail_host="smtp.163.com"  #设置服务器
	mail_user="shihao1024@163.com"   #用户名
	mail_pass="shihao1992"   #口令

	sender = 'shihao1024@163.com'
	receivers = 'shihao1024@163.com'  # 接收邮件

	message = MIMEText(url, 'plain', 'utf-8')
	message['From'] = "shihao<shihao1024@163.com>"
	message['To'] = "shihao<shihao1024@163.com>"

	subject = msg
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
	
# 网页查询函数
def query_cycle():
	cycle_time = 0
	while(1):
		try:
			html_query()
			cycle_time += 1
			if(cycle_time == 12):
				print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				print "12 times completed."
				cycle_time = 0
		except requests.exceptions.SSLError, ErrorAlert:
			print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			print "Error: ", ErrorAlert
			send_email("Msg from 58bot: Wrong again!")
		time.sleep(1200)
	return

# def file_write(content):
	# f = open('0113.txt', 'w')
	# f.write(content.encode('utf-8'))
	# f.write('\n')
	# f.close
	# return
	
# 开始查询	
query_cycle()
# html_query()