import requests
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

url = 'https://bandwagonhost.com/cart.php?gid=1'
key_word = u'Order Now'

# main function
def html_query():
	html_response = requests.get(url).content
	order_list = re.findall(key_word, html_response, re.I|re.S|re.M)
	order_num = len(order_list)
	if(order_num != 20):
		send_email(order_num)
	return
	
def send_email(num):
	mail_host="smtp.163.com"  
	mail_user="shihao1024@163.com"  
	mail_pass="shihao1992" 

	sender = 'shihao1024@163.com'
	receivers = ['shihao1024@163.com'] 
	subject = "bandwagonhost.com: "+str(num)+" order."
	
	message = MIMEText('', 'plain', 'utf-8')
	message['From'] = "shihao<shihao1024@163.com>"
	message['To'] =  "shihao<shihao1024@163.com>"
	message['Subject'] = Header(subject)

	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host, 25)   
		smtpObj.login(mail_user,mail_pass)
		smtpObj.sendmail(sender, receivers, message.as_string())
		print "send successfully"
	except smtplib.SMTPException:
		print "send unsuccessfully"
	return
	
def query_cycle():
	time_delay = 60
	query_times = 0
	while(1):
		try:
			if(query_times == 60):
				print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
				print "60 times completed, next cycle begin."
				query_times = 0
			html_query()
			query_times += 1
		except requests.exceptions.ConnectionError, ErrorAlert:
			print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
			print "Error: ", ErrorAlert
		time.sleep(time_delay)
	return

query_cycle()