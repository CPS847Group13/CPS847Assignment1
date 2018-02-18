import unittest

import repeaterbot

class TestMethods(unittest.TestCase):
	def test_message(self):
		response = repeaterbot.request("toronto")
		self.assertIsNotNote(response)
		
		
if __name__ == '__main__':
	unittest.main()
	