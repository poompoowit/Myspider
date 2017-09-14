#! python3
# -*- coding: utf-8 -*-
#Phuwit Vititayanon 5710503509
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode
import urllib.parse
import os
import re
import requests
def open_file(path):
	my_file = Path(path)
	if my_file.is_file():
		file = open(path, "r")
		list_data = file.readlines()
		data = []
		for ele in list_data:
			data.append(ele.replace("\n",""))
		list_data = data
		print ('\x1b[5;30;47m' +'open file : '+path+ '\x1b[0m')
	else:
		list_data = []
		print ('\x1b[0;30;41m' + "Not found :"+path + '\x1b[0m')
	return list_data

def save_file(path,data):
	try:
		file = open(path, "w")
		for ele in data:
			file.write(ele+'\n')
		file.close()
		print ('\x1b[5;30;47m' +'saved file : '+path+ '\x1b[0m')
	except:
		print ('\x1b[0;30;41m' + "error save :"+path + '\x1b[0m')

def check_robots(url_base):
	try:
		checker = urlopen(url_base  + '/robots.txt')
		string = checker.read().decode("utf8")
		start = False
		found = False
		for line in string.splitlines():
			if line == 'User-agent: *':
				start = True
				found = True
			if start == True:
				if "Disallow:" in line:
					link = line.split()
					restrict.append(url_base+link[1].replace("*",".*"))
				if line == '':
					start = False
		if found:
			robots.append(url_base)
			print ('\x1b[5;30;42m' + "found robots.txt :"+url_base+ '\x1b[0m')
	except:
		check = 'none'

def add_queue(url_base,url):
	domain = url_base.split('/')[0]+'//'+url_base.split('/')[2]+'/'
	if url not in queue:
		if url not in crawled:
			if "http" in url:
				# if re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
				if "ku.ac.th" in url:
					pass_check = True
					for ele in restrict:
						if re.match(ele, url):
							pass_check = False
					if pass_check:
						queue.append(url)
			else:
				# url = url.replace(".","")
				if (domain+url) not in queue:
					if (domain+url) not in crawled:
						queue.append(domain+url)

def check_for_redirects(url):
	try:
		r = requests.get(url, allow_redirects=False, timeout=2)
		print(r.status_code)
		if 200 != r.status_code and 302 != r.status_code and 303 != r.status_code and 301 != r.status_code:
		# if  400 <= r.status_code:
			return '[redirect]'
		else:
			return '[no redirect]'
	except requests.exceptions.Timeout:
		return '[timeout]'
	except requests.exceptions.ConnectionError:
		return '[connection error]'
	except:
		return '[connection error]'

def crawler(url,count):
	tried.append(url)
	orl_url = url
	parsed_url = urlparse(url)
	parameters = parse_qs(parsed_url.query)
	url = parsed_url._replace(query=urlencode(parameters, doseq=True)).geturl()
	# print(url)
	redirect_url = check_for_redirects(url)
	if redirect_url == '[redirect]' :
		print ('\x1b[0;30;41m' + "redirect or error in url :"+url + '\x1b[0m')
		return count
	elif redirect_url == '[timeout]' :
		print ('\x1b[0;30;41m' + "timeout in url :"+url + '\x1b[0m')
		return count
	elif redirect_url == '[connection error]' :
		print ('\x1b[0;30;41m' + "connection error in url :"+url + '\x1b[0m')
		return count
	else:
		try:
			conn = urlopen(url)
			http_message = conn.info()
			if(http_message.get_content_type() != 'text/html'):
				print ('\x1b[0;30;41m' + "Url not HTML :"+url + '\x1b[0m')
				return count
			check_robots(url)
			html = conn.read()
			soup = BeautifulSoup(html,"lxml")
			links = soup.find_all('a')
			for tag in links:
				link = tag.get('href',None)
				if link is not None:
					add_queue(url,link)
			
			path = orl_url.replace("http://","")
			path = path.replace("https://","")
			delete_char = '<>:"\\|?*'
			for char in delete_char:
				path = path.replace(char,'')
			path = './html/'+path+'.html'
			os.makedirs(os.path.dirname(path), exist_ok=True)
			f = open(path, "w")
			f.write(str(soup.prettify("utf-8")))
			f.close()
			crawled.append(orl_url)
			print('\x1b[5;30;43m' +'['+str(count)+'/'+str(number)+'] '+'crawler url :'+url+ '\x1b[0m')
			count +=1
			return count
		except:
			print ('\x1b[0;30;41m' + "error in url :"+url + '\x1b[0m')
			return count

if __name__ == '__main__':
	number = int(input("Number of web to crawl: "))
	path_queue = "./queue.txt"
	path_crawled = "./crawled.txt"
	path_robots = "./robots.txt"
	path_restrict = "./restrict.txt"
	path_tried = "./tried.txt"
	queue = open_file(path_queue)
	crawled = open_file(path_crawled)
	robots = open_file(path_robots)
	restrict = open_file(path_restrict)
	tried = open_file(path_tried)
	count = 1
	if not queue:
		queue.append('https://std.regis.ku.ac.th/')
		queue.append('https://knowbita.cpe.ku.ac.th/')
		queue.append('https://lms.ku.ac.th/')
		queue.append('http://www.grad.ku.ac.th/')
		queue.append('http://ifrpd.ku.ac.th/')
		queue.append('http://www.vettech.ku.ac.th/')
		queue.append('http://www.ee.ku.ac.th/')
		queue.append('http://www.eto.ku.ac.th//')
		queue.append('http://www.coop.ku.ac.th/')
		queue.append('http://www.cai.ku.ac.th/')
		queue.append('http://www.interprogram.ku.ac.th/')
		queue.append('https://eassess.ku.ac.th/')
		queue.append('https://www.cpe.ku.ac.th/')
		queue.append('http://www.east.human.ku.ac.th/')
		queue.append('http://ase.eng.ku.ac.th/')
		queue.append('http://www.gerd.eng.ku.ac.th/')
		queue.append('http://www.kps.ku.ac.th/')
		queue.append('http://dnatec.kps.ku.ac.th/')
		queue.append('http://www.kus.ku.ac.th/')
		queue.append('http://www.bce.eco.ku.ac.th/')
		queue.append('http://doipui.aerdi.ku.ac.th/')
		queue.append('http://dna.kps.ku.ac.th/')
		queue.append('http://www.mfpe.eng.ku.ac.th/')
		queue.append('http://www.wre.eng.ku.ac.th/')
		queue.append('http://vet.ku.ac.th/')
		queue.append('http://iup.eng.ku.ac.th/')
		queue.append('http://doed.edu.ku.ac.th/')
	while count <= number:
		count = crawler(queue[0],count)
		queue = queue[1:]
		if count%50==0:
			save_file(path_queue,queue)
			save_file(path_restrict,restrict)
			save_file(path_robots,robots)
			save_file(path_crawled,crawled)
			save_file(path_tried,tried)
		# count +=1
	save_file(path_queue,queue)
	save_file(path_restrict,restrict)
	save_file(path_robots,robots)
	save_file(path_crawled,crawled)
	save_file(path_tried,tried)