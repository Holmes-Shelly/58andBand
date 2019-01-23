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
url = 'https://qd.58.com/jingjijiaoche/0/pve_5864_7_999999/?PGTID=0d301ef1-0007-af12-011d-42748daec82a&ClickID=7'

headers = {
	'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'accept-encoding':'gzip, deflate',
	'accept-language':'en,zh;q=0.9,zh-CN;q=0.8,lb;q=0.7',
	'Cache-Control':'max-age=0',
	'Upgrade-Insecure-Requests':'1',
	'cookie':'f=n; commontopbar_new_city_info=122%7C%E9%9D%92%E5%B2%9B%7Cqd; city=qd; f=n; commontopbar_new_city_info=122%7C%E9%9D%92%E5%B2%9B%7Cqd; city=qd; id58=c5/njVphg4qNMyALEOAkAg==; 58tj_uuid=e07705a3-a222-4f05-aac6-ab7f5bb6f7f5; __utma=253535702.793148155.1516340160.1516340160.1516340160.1; xxzl_deviceid=gG55ora%2BTdnWecKNRDJzkKd2icRHcLtd44Z74COlIHDv6FjW4PKJRS5m6sHIFRZ8; wmda_new_uuid=1; wmda_uuid=269d53e36c005c6ac5e3cef82bc651c2; xxzl_smartid=6f40ca08ae1efe071b5b803a8fa806f7; city=qd; 58home=qd; f=n; commontopbar_new_city_info=122%7C%E9%9D%92%E5%B2%9B%7Cqd; new_uv=18; utm_source=; spm=; init_refer=https%253A%252F%252Fcn.bing.com%252F; commontopbar_ipcity=qd%7C%E9%9D%92%E5%B2%9B%7C0; als=0; sessionid=33124d1a-3c54-46d5-aff4-4eb87df65e65; wmda_session_id_1732038237441=1548117494887-be71a0e8-9246-3140; wmda_visited_projects=%3B2385390625025%3B1732038237441; new_session=0; gr_user_id=7d35a13c-9a48-4c97-89fb-033560a78eb0; xxzl_sid="7aDq5S-NA7-LOL-SvI-289I4LNtx"; ppStore_fingerprint=9D48D6955935981E84F4C6EA04661652A0639E72051CB01F%EF%BC%BF1548119447477; xxzl_token="plYvI5bKh8uq/sHZ1agGTTEZkLxX5+huTULyp+HQ3sAFa/q6UOejFY08eTut5596in35brBb//eSODvMgkQULA=="',
	'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	}

def html_query():
	req.headers = headers
	# html_response = open('0122.html', 'r').read().decode('utf-8')
	try:
		html_response = req.get(url).content.decode('utf-8')
	except requests.exceptions.SSLError, ErrorAlert:
		print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), "Error: SSLError!"
		send_email("Msg from 58bot: SSLError!")
		return
	# file_write(html_response)
	res = r'<li.*?img [a-z]{3}=\"(https://pic.*?)\".*?alt=\"(.*?)\".*?href=\"(https://qd.58.com/ershouche/.*?)\".*?info_param.*?span>(.*?)</span><span>(.*?)<.*?h3>([0-9\.]+)<span.*?guess_like post_time\">(.*?)<.*?<\/li>'
	ans = re.findall(res, html_response, re.I|re.S|re.M)
	print "Find", len(ans)
	for ans_d in ans:	
		sendtime = ans_d[-1]
		if(sendtime[-3:] == u'分钟前'):
			if(int(sendtime[0:len(sendtime)-3]) < 60):
				print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), "Find 1."
				print '\n'.join(ans_d)
				send_email(ans_d)
	return

def send_email(car_detail):
	mail_host="smtp.163.com" 
	mail_user="shihao1024@163.com"  
	mail_pass="shihao1992"  

	sender = 'shihao1024@163.com'
	receivers = ['shihao1024@163.com']
	
	mail_content = "<a href='"+car_detail[2]+"'>"+car_detail[1]+"</a><img src='"+car_detail[0]+"'></img><p>"+car_detail[3]+" "+car_detail[4]+"</p><p>"+car_detail[5]+u"万 "+car_detail[6]+"</p>"
	message = MIMEText(mail_content, 'html', 'utf-8')
	message['From'] = "shihao<shihao1024@163.com>"
	message['To'] = "shihao<shihao1024@163.com>"

	subject = car_detail[1]
	message['Subject'] = Header(subject)

	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host, 25) 
		smtpObj.login(mail_user,mail_pass)
		smtpObj.sendmail(sender, receivers, message.as_string())
		# print "delivery successful"
	except smtplib.SMTPException:
		print "delivery failed"
	return

def query_cycle():
	cycle_time = 0
	print "----------Start monitoring----------"
	while(1):
		time_delay = 1200
		time_hour = int(time.strftime('%H',time.localtime(time.time())))
		if time_hour == 22:
			time_delay = 32400		

		html_query()
		cycle_time += 1
		if(cycle_time % 3 == 0):
			print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), cycle_time, "times completed."
		time.sleep(time_delay)
	return

# def file_write(content):
	# f = open('0123.txt', 'w')
	# f.write(content.encode('utf-8'))
	# f.write('\n')
	# f.close
	# return
	
# query_cycle()
html_query()