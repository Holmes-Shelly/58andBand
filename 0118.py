#-*- coding:utf-8 -*-
import requests
import re
import time
import base64
import io
from fontTools.ttLib import TTFont

# req = requests.session()
# url = 'https://rongcheng.58.com/whrcsq/zufang/j3/?PGTID=0d3090a7-046e-413b-b067-6af5194bd063&ClickID=1'

# headers = {
	# 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	# 'accept-encoding':'gzip, deflate',
	# 'accept-language':'en,zh;q=0.9,zh-CN;q=0.8,lb;q=0.7',
	# 'Cache-Control':'max-age=0',
	# 'Upgrade-Insecure-Requests':'1',
	# 'cookie':'commontopbar_new_city_info=522%7C%E8%8D%A3%E6%88%90%7Crongcheng; f=n; commontopbar_ipcity=qd%7C%E9%9D%92%E5%B2%9B%7C0; id58=c5/njVphg4qNMyALEOAkAg==; 58tj_uuid=e07705a3-a222-4f05-aac6-ab7f5bb6f7f5; als=0; __utma=253535702.793148155.1516340160.1516340160.1516340160.1; xxzl_deviceid=gG55ora%2BTdnWecKNRDJzkKd2icRHcLtd44Z74COlIHDv6FjW4PKJRS5m6sHIFRZ8; wmda_new_uuid=1; wmda_uuid=269d53e36c005c6ac5e3cef82bc651c2; wmda_visited_projects=%3B2385390625025; xxzl_smartid=6f40ca08ae1efe071b5b803a8fa806f7; city=qd; 58home=qd; ppStore_fingerprint=9D48D6955935981E84F4C6EA04661652A0639E72051CB01F%EF%BC%BF1547554785806; new_uv=16; utm_source=; spm=; init_refer=; wmda_session_id_2385390625025=1547637784967-a68bae6f-b759-d099; f=n; new_session=0; xzfzqtoken=VmQYUAsdWXDMPAHE1klkpAnZ0rUuSzLosQww3mIX8lpmfL%2BsYevhcBxwwesiqNWKin35brBb%2F%2FeSODvMgkQULA%3D%3D',
	# 'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	# }

def html_query():
	# req.headers = headers
	html_response_pre = open('0113.txt', 'r').read().decode('utf-8')
	# try:
		# html_response_pre = req.get(url).content.decode('utf-8')
	# except requests.exceptions.SSLError, ErrorAlert:
		# print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		# print "Error: ", ErrorAlert
		# return
	# if('ISDCaptcha' in html_response_pre):
		# print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		# print "Error: ISDCaptcha!"
		# return
	html_response = num_replace(html_response_pre)
	res = r'<h2>.*?>\s+(.*?)\s+<.*?</h2>.*?<div class="sendTime">\s+(\S+)\s+</div>.*?<b class="strongbox">(.*?)</b>'
	ans = re.findall(res, html_response, re.I|re.S|re.M)
	for ans_d in ans:
		sendtime = ans_d[1]
		if(sendtime[-3:] == u'小时前'):
			house_detail = ', '.join(ans_d)
			if(int(sendtime[0:len(sendtime)-3]) < 22):
				print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), "Find 1.", house_detail
	return

def num_replace(resp):
	base64_str = re.findall('base64,(.*)\'\) format', resp)[0]
	bin_data = base64.b64decode(base64_str)
	fonts = TTFont(io.BytesIO(bin_data))
	bestcmap = fonts.getBestCmap()
	# print "bestcmap:", bestcmap
	# newmap = {}
	resp_ = resp
	for key,value in bestcmap.items():
		new_value = int(re.findall(r'(\d+)',value)[0])-1
		new_key = hex(key).replace('0x', '&#x') + ';'
		# newmap[new_key] = new_value
		if new_key in resp_:
			resp_ = resp_.replace(new_key, str(new_value))
	# print "newmap:", newmap
	return resp_

# def file_write(content):
	# f = open('0118.txt', 'w')
	# f.write(content.encode('utf-8'))
	# f.write('\n')
	# f.close
	# return
	
html_query()