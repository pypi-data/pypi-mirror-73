import json
import requests

class LongPoll:
	"""
	#: LongPoll server VK это сервер вк, 
	который позволяет получать события которые произошли
	при работе бота, подробнее о всех событиях можно узнать
	в офф. документации ВК; https://vk.com/dev/groups_events
	"""
	__slots__ = ('token', 'grp_id', 'v',
					'wait', 'url', 'http',
					'ts', 'server', 'key')

	def __init__(self, session, wait=25):
		self.token = session[0]
		self.grp_id = session[1]
		self.v = session[-1]
		self.wait = wait
		self.url = 'https://api.vk.com/method/'
		self.http = requests.Session()
		self.ts = None
		self.server = None
		self.key = None
		self.__update_data()

	def __update_data(self, updts=True):
		api_data = {
			'access_token': self.token,
			'v': self.v,
			'group_id': self.grp_id
			}
		r = self.http.post(f"{self.url}groups.getLongPollServer?", params=api_data).json()
		self.server = r['response']['server']
		self.key = r['response']['key']
		if updts:
			self.ts = r['response']['ts']

	def _lp_check(self):
		lp_data = {
			'act': 'a_check',
			'key': self.key,
			'wait': self.wait,
			'mode': 2,
			'ts': self.ts
		}
		r = self.http.post(self.server, params=lp_data, timeout=self.wait + 10).json()
		if "failed" in r:
			if r['failed'] == 1:
				self.__update_data()
			elif r['failed'] == 2:
				self.__update_data(updts=False)
			elif r['failed'] == 3:
				self.__update_data()
		else:
			return r['updates']

	def listening(self):
		"""
		#: Прослушивание LongPoll`a
		#: Когда происходит какое-либо событие в LongPoll VK
		данная функция возвращяет массив updates и сразу 
		же обновляет данные о LongPolle и ждёт следующего события;
		"""
		print('[29]: Started the listening LongPoll...\n')
		while True:
			for i in self._lp_check():
				yield i
				self.__update_data()