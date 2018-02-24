import repeaterbot
import unittest 

class test(unittest.TestCase):

    #test auto correct
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
        
    #test NLP
    def test_whatstheweather(self):
        #test 2 correct, 1 incorrect
        self.assertTupleEqual((True, 'Thunder Bay'), repeaterbot.NLP("What's the weather in Thunder Bay"))
        self.assertTupleEqual((True, 'Toronto'), repeaterbot.NLP("Whats teh weather in Toronto?"))
        self.assertTupleEqual((False, None), repeaterbot.NLP("What's the weder in Toronto?"))
        
    def test_whatstheweatherlike(self):
        #test 2 correct, 1 incorrect
        self.assertTupleEqual((True, 'Thunder Bay'), repeaterbot.NLP("What's the weather in Thunder Bay"))
        self.assertTupleEqual((True, 'Toronto'), repeaterbot.NLP("Whats teh weather in Toronto?"))
        self.assertTupleEqual((False, None), repeaterbot.NLP("What's the weder in Toronto?"))
    
    def test_howstheweather(self):
        #test 2 correct, 1 incorrect
        self.assertTupleEqual((True, 'Thunder Bay'), repeaterbot.NLP("How's the weather in Thunder Bay"))
        self.assertTupleEqual((True, 'Toronto'), repeaterbot.NLP("Hows teh weather in Toronto?"))
        self.assertTupleEqual((False, None), repeaterbot.NLP("How is Toronto?"))
    
    def test_weather(self):
        #test 2 correct, 1 incorrect
        self.assertTupleEqual((True, 'Thunder Bay'), repeaterbot.NLP("Weather in Thunder Bay"))
        self.assertTupleEqual((True, 'Toronto'), repeaterbot.NLP("weather Toronto?"))
        self.assertTupleEqual((False, None), repeaterbot.NLP("Toronto"))
        
if __name__ == '__main__':
    unittest.main()
