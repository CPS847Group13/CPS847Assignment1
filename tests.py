import unittest

import repeaterbot

class TestMethods(unittest.TestCase):
	def test_message(self):
		toronto = "Toronto"
		response = repeaterbot.correct(toronto)
		self.assertEqual(toronto, response)
		
		
if __name__ == '__main__':
	unittest.main()
	
