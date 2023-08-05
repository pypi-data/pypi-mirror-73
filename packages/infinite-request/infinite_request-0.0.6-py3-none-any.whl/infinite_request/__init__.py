from urllib import parse, request

def infinite_request(url):
	while True:
		try:
			req = request.Request(url=url)
			res = request.urlopen(req, timeout=5)
			res = res.read()
			return res.decode(encoding='utf-8')
		except KeyboardInterrupt as e:
			raise e
		except:
			continue


from requests import Session

session = Session()

def infinite_request_session(url):
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