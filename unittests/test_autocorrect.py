import repeaterbot
import unittest 

class test_autocorrect(unittest.TestCase):
    def test_toronto(self):
    
        #test two incorrect and 1 correct
        self.assertEqual('Toronto', repeaterbot.correct('Tronto'))
        self.assertEqual('Toronto', repeaterbot.correct('Tornto'))
        self.assertEqual('Toronto', repeaterbot.correct('Toronto'))
        
    def test_edmonton(self):
    
        #test two incorrect and 1 correct
        self.assertEqual('Edmonton', repeaterbot.correct('Edmoton'))
        self.assertEqual('Edmonton', repeaterbot.correct('Edmontn'))
        self.assertEqual('Edmonton', repeaterbot.correct('Edmonton'))