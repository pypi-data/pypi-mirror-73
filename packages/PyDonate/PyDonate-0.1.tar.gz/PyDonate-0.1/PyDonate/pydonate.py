import random
from SimpleQIWI import *
from time import sleep

class PyDonate:
	def __init__(self, token=None, phone=None, debug=False):
		self.token = token
		self.phone = phone
		self.debug = debug

	def start(self, price=1):
		try:
			if self.token != None or self.phone != None:
				qiwi = QApi(token=self.token, phone=self.phone)
				comment = qiwi.bill(price)
				if self.debug == True:
					print(f"Comment: {comment}")
				qiwi.start()
				while True:
					if qiwi.check(comment):
						if self.debug == True:
							print('Payment said!')

					sleep(5)

		except Exception as e:
			if self.debug == True:
				print(f"	DEBUG: 	"
					  f"\n\n{e}\n\n")
