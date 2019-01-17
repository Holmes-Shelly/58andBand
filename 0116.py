#-*- coding:utf-8 -*-
import requests
import re
import time
import base64
import io
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from fontTools.ttLib import TTFont

req = requests.session()
url = 'https://rongcheng.58.com/whrcsq/zufang/j3/?PGTID=0d3090a7-046e-413b-b067-6af5194bd063&ClickID=1'

headers = {
	'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'accept-encoding':'gzip, deflate',
	'accept-language':'en,zh;q=0.9,zh-CN;q=0.8,lb;q=0.7',
	'Cache-Control':'max-age=0',
	'Upgrade-Insecure-Requests':'1',
	'cookie':'commontopbar_new_city_info=522%7C%E8%8D%A3%E6%88%90%7Crongcheng; f=n; commontopbar_ipcity=qd%7C%E9%9D%92%E5%B2%9B%7C0; id58=c5/njVphg4qNMyALEOAkAg==; 58tj_uuid=e07705a3-a222-4f05-aac6-ab7f5bb6f7f5; als=0; __utma=253535702.793148155.1516340160.1516340160.1516340160.1; xxzl_deviceid=gG55ora%2BTdnWecKNRDJzkKd2icRHcLtd44Z74COlIHDv6FjW4PKJRS5m6sHIFRZ8; wmda_new_uuid=1; wmda_uuid=269d53e36c005c6ac5e3cef82bc651c2; wmda_visited_projects=%3B2385390625025; xxzl_smartid=6f40ca08ae1efe071b5b803a8fa806f7; city=qd; 58home=qd; ppStore_fingerprint=9D48D6955935981E84F4C6EA04661652A0639E72051CB01F%EF%BC%BF1547554785806; new_uv=16; utm_source=; spm=; init_refer=; wmda_session_id_2385390625025=1547637784967-a68bae6f-b759-d099; f=n; new_session=0; xzfzqtoken=VmQYUAsdWXDMPAHE1klkpAnZ0rUuSzLosQww3mIX8lpmfL%2BsYevhcBxwwesiqNWKin35brBb%2F%2FeSODvMgkQULA%3D%3D',
	'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	}

def html_query():
	req.headers = headers
	html_response = get_list(req.get(url).content.decode('utf-8'))
	# file_write(html_response)
	# html_response = get_list(open('0113.txt', 'r').read().decode('utf-8'))
	if('ISDCaptcha' in html_response):
		print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		print "Error: ISDCaptcha!"
		send_email("Msg from 58bot: ISDCaptcha!")
		return
	res = r'<h2>.*?>\s+(.*?)\s+<.*?</h2>.*?<div class="sendTime">\s+(\S+)\s+</div>.*?<b class="strongbox">(.*?)</b>'
	ans = re.findall(res, html_response, re.I|re.S|re.M)
	for ans_d in ans:
		sendtime = ans_d[1]
		if(sendtime[-3:] == u'分钟前'):
			house_detail = ', '.join(ans_d)
			if(int(sendtime[0:len(sendtime)-3]) < 22):
				print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				print "Find 1."# , house_detail
				send_email(house_detail)
	return

def send_email(msg):
	# 第三方 SMTP 服务
	mail_host="smtp.163.com"  #设置服务器
	mail_user="shihao1024@163.com"   #用户名
	mail_pass="shihao1992"   #口令

	sender = 'shihao1024@163.com'
	receivers = ['shihao1024@163.com']  # 接收邮件

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

def get_list(resp):
	base64_str = re.findall('data:application/font-ttf;charset=utf-8;base64,(.*)\'\) format\(\'truetype\'\)}', resp)
	bin_data = base64.b64decode(base64_str[0])
	fonts = TTFont(io.BytesIO(bin_data))
	bestcmap = fonts.getBestCmap()
	newmap = {}
	for key in bestcmap.keys():
		# print(key)
		# print(re.findall(r'(\d+)',bestcmap[key]))
		value = int(re.findall(r'(\d+)',bestcmap[key])[0])-1
		key = hex(key)
		newmap[key] = value
	# print('==========', newmap)
	resp_ = resp
	for key,value in newmap.items():
		key_ = key.replace('0x', '&#x') + ';'
		if key_ in resp_:
			resp_ = resp_.replace(key_, str(value))
	return resp_

# 网页查询函数
def query_cycle():
	cycle_time = 0
	while(1):
			time_hour = int(time.strftime('%H',time.localtime(time.time())))
	      if time_hour == 22:
		     time_delay = 36000
	      else:
		     time_delay = 1200
try:
			html_query()
			cycle_time += 1
			# print cycle_time
			if(cycle_time % 3 == 0):
				print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				print cycle_time, " times completed."
		except requests.exceptions.SSLError, ErrorAlert:
			print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			print "Error: ", ErrorAlert
			send_email("Msg from 58bot: SSLError!")
		time.sleep(time_delay)
	return

# def file_write(content):
	# f = open('0116.txt', 'w')
	# f.write(content.encode('utf-8'))
	# f.write('\n')
	# f.close
	# return
	
# 开始查询	
query_cycle()
# html_query()
