from requests import Session

session = Session()

def infinite_request(url):
	while True:
		try:
			return session.get(url, timeout=5).text
		except KeyboardInterrupt as e:
			raise e
		except:
			continue