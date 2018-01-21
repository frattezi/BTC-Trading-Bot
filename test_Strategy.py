"""
Test for strategy functions
"""
from Strategy import BacktestStrategy
import unittest
from mock import MagicMock

class MyTest(unittest.TestCase):

    def __init__(self):
        
   
    def simple_average_test(self):
        """Test for average"""
        simple_av_func = BacktestStrategy.SimpleAVPrice
        print (simple_av_func)
        pass

    def exp_average_test(self):
        """Test for average"""
        pass

if __name__ == '__main__':
    unittest.main()