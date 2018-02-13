import repeaterbot
import unittest 

class TestNLP(unittest.TestCase):
    def test_whatstheweather(self):
        #test 2 correct, 1 incorrect
        self.assertTupleEqual((True, 'Thunder Bay'), repeaterbot.NLP("What's the weather in Thunder Bay"))
        self.assertTupleEqual((True, 'Toronto'), repeaterbot.NLP("Whats the weather in Toronto?")
        self.assertTupleEqual((False, None), repeaterbot.NLP("What's the weder in Toronto?"))
        
    def test_whatstheweatherlike(self):
        #test 2 correct, 1 incorrect
        self.assertTupleEqual((True, 'Thunder Bay'), repeaterbot.NLP("What's the weather in Thunder Bay"))
        self.assertTupleEqual((True, 'Toronto'), repeaterbot.NLP("Whats the weather in Toronto?")
        self.assertTupleEqual((False, None), repeaterbot.NLP("What's the weder in Toronto?"))
    
    def test_howstheweather(self):
        #test 2 correct, 1 incorrect
        self.assertTupleEqual((True, 'Thunder Bay'), repeaterbot.NLP("How's the weather in Thunder Bay"))
        self.assertTupleEqual((True, 'Toronto'), repeaterbot.NLP("Hows the weather Toronto?")
        self.assertTupleEqual((False, None), repeaterbot.NLP("How is Toronto?"))
    
    def test_weather(self):
        #test 2 correct, 1 incorrect
        self.assertTupleEqual((True, 'Thunder Bay'), repeaterbot.NLP("Weather in Thunder Bay"))
        self.assertTupleEqual((True, 'Toronto'), repeaterbot.NLP("weather Toronto?")
        self.assertTupleEqual((False, None), repeaterbot.NLP("Toronto"))