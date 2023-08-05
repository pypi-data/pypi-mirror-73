from requests import Session

session = Session()

def blocked(text):
	return 'errors.aliyun.com' in text

def infinite_request(url):
	global session

	while True:
		try:
			txt = session.get(url, timeout=5).text
			
			if blocked(text):
				session = Session()
				continue
			else:
				return txt
		except KeyboardInterrupt as e:
			raise e
		except:
			continue