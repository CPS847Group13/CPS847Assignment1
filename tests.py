import unittest

import repeaterbot

class TestMethods(unittest.TestCase):
	def test_message(self):
		toronto = "toronto"
		response = repeaterbot.request(toronto)
		self.assertIsNotNone(response)
		
		
if __name__ == '__main__':
	unittest.main()
	
