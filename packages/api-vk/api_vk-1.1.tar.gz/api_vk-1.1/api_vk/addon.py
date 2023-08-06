class LpAddon:
	"""
	#: LpAddon - LongPollAddon, упрощяет пользование LongPoll ом;
	#: Имеет один обязательный аргумент 'event' - событие;
	#: всё что делает данный класс, это берёт данные события из LongPolla
	и при вызове того объекта который вам нужен, он просто возращяет именно то,
	что вам нужно;
	"""
	def __init__(self, event: dict={'None': None}):
		self.event = event

	def __getattr__(self, value):
		self.attr = value
		return self

	def __call__(self):
		try:
			if 'None' in self.event:
				raise AttributeError('You forgot to specify a single argument \'event\'')
			else:
				return self.__get(self.attr)
		except TypeError:
			raise TypeError('The \'event\' argument must be a dict.')

	def __get(self, attr):
		if attr == 'chat_id':
			cid = int(self.event['object']['peer_id']) - 2000000000
			return cid

		elif attr == 'peer_id':
			return self.event['object']['peer_id']

		elif attr == 'from_id':
			return self.event['object']['from_id']

		elif attr == 'type':
			return self.event['type']

		elif attr == 'text':
			return self.event['object']['text']

		elif attr == 'fwd_messages':
			return self.event['object']['fwd_messages']

		elif attr == 'attachments':
			return self.event['object']['attachments']

		elif attr == 'reply_message':
			try:
				return self.event['object']['reply_message']
			except KeyError:
				return None

		elif attr == 'group_id':
			return self.event['group_id']