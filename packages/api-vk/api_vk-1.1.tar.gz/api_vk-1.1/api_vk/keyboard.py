import json

class KeyBoard:
	"""
	#: Клавиатура используется чат ботами в ВК;
	#: Данный класс принимает два не обязательных аргумента;
	#: 1. one_time - Отвечает за скрытие 
	клавиатуры после нажатия | Default = False;
	#: 2. inline - Отвечает за отображение кнопок 
	на сообщение или в клавиатуре | Default = False;
	"""
	def __init__(self, one_time=False, inline=False):
		self.kb = {"inline": inline, "one_time": one_time}
		self.buttons = []

	def Button_Add(self, text='', color='secondary'):
		"""
		#: Позволяет добавить кнопку в клавиатуру;
		#: Принимает один обязательный аргумент и второй не обязательный;
		#: 1. text - текст кнопки [str];
		#: 2. color - цвет кнопки | Default = secondary/white, [str];
		#: Аргумент 'color' может иметь 4 значения: red, blue, green, white;
		"""
		if color == 'white' or color == 'secondary':
			b = [{"action": {"type": 'text', "payload": "{}", "label": text}, "color": color}]
			self.buttons.append(b)
		elif color == 'red':
			b = [{"action": {"type": 'text', "payload": "{}", "label": text}, "color": 'negative'}]
			self.buttons.append(b)
		elif color == 'blue':
			b = [{"action": {"type": 'text', "payload": "{}", "label": text}, "color": 'primary'}]
			self.buttons.append(b)
		elif color == 'green':
			b = [{"action": {"type": 'text', "payload": "{}", "label": text}, "color": 'positive'}]
			self.buttons.append(b)

	def Button_Add_Link(self, text='', url=''):
		"""
		#: Позволяет добавить кнопку с ссылкой в клавиатуру;
		#: Принимает два обязательных аргумента;
		#: 1. text - текст кнопки [str];
		#: 2. url - ссылка на сайт [str];
		"""
		b = [{"action": {"type": 'open_link', "payload": "{}", "link": url, "label": text}}]
		self.buttons.append(b)

	def Buttons(self):
		"""
		#: Объединяет все кнопки созданые ранее в один JSON объект
		для отправки клавиатуры с сообщением.
		#: Не имеет аргументов.
		"""
		a = []
		for i in range(len(self.buttons)):
			a.append(self.buttons[i])
		self.kb.update({"buttons": a})
		kb = json.dumps(self.kb, ensure_ascii=False)
		kb = kb.encode('utf-8').decode('utf-8')
		return kb