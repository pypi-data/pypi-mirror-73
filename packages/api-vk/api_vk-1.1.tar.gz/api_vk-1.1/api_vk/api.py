import requests
import json

class ApiErr(Exception):
	def __init__(self, exc):
		self.exc = exc
		
class ApiVK:
	"""
	#: ApiVK - позволяет обращятся к методам ВКонтакте;
	#: Данный класс имеет 2 обязательных и один не обязательный аргумент.
	#: 1. token[str] - токен группы полученый в настройках, 
	инструкциия в офф. документации ВК; https://vk.com/dev/bots_docs?f=1.1.%20Получение%20ключа%20доступа
	#: 2. group_id[int] - Идентификатор группы (положительное число)
	#: 3. v[float] - версия Api | Default = 5.95
	"""
	__slots__ = ('token', 'grp_id', 
					'v', '_method', 
					'api_url', 'http')

	def __init__(self, token=None, group_id=0, v=5.95):
		self.token = token
		self.grp_id = group_id
		self.v = v
		self.http = requests.Session()
		self.api_url = 'https://api.vk.com/method/'
		self._method = None

	def __getattr__(self, value):
		self.method = value
		return self

	def __call__(self, **kwargs):
		return self._api_request(method=self.method, params=kwargs)

	def _api_request(self, method: str=None, params: dict={"None": None}):
		data = {
			'access_token': self.token,
			'v': self.v,
			**params
			}
		r = self.http.post(f"{self.api_url}{method}?", params=data).json()
		return self.__proccessing(r)

	def __proccessing(self, resp: dict={"None": None}):
		if 'error' in resp:
			err = 'Code ({}): {}'.format(resp['error']['error_code'], resp['error']['error_msg'])
			raise ApiErr(err)
		else:
			return resp['response']

	def Session(self):
		"""
		#: Данная функция нужна для быстрой передачи всех не обходимых
		данных в class LongPoll.
		"""
		return self.token, self.grp_id, self.v

	@property
	def method(self):
		"""
		#: Pass;
		"""

	@method.getter
	def method(self):
		res = self._method
		self._method = None
		return res

	@method.setter
	def method(self, value):
		if self._method is None:
			self._method = value
		else:
			self._method += '.{}'.format(value)