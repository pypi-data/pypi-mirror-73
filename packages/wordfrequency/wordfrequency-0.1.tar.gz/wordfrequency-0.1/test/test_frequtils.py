
import unittest
import categorize.freq_utils as futils
class Test_TestFreqUtils(unittest.TestCase):

    def test_removal_of_uoms(self):
        wordlist=['1543m','1545m3','hello','1546meters','1543.3m','1543,3m3']
        
        result=futils.remove_uoms(wordlist)
        #make sure we do not have 1543m and 1545m3 in the list that is returned
        self.assertEqual('1543m' in result,False)
        self.assertEqual('1545m3' in result,False)
        self.assertEqual('hello' in result,True)
        self.assertEqual('1546meters' in result,True)
        self.assertEqual('1543.3m' in result,False)
        self.assertEqual('1543,3m3' in result,False)
    
    def test_removal_of_numerics(self):
        wordlist=[u'1543',u'1001',u'hello']
        result=futils.remove_numerics(wordlist)
        self.assertEqual('1543' in result,False)
        self.assertEqual('1001' in result,False)
        self.assertEqual('hello' in result,True)

    def test_removal_of_decimals(self):
        wordlist=['1543.4','1543.3453','1543','1543,567']
        result=futils.remove_decimals(wordlist)
        self.assertEqual('1543.4' in result,False)
        self.assertEqual('1543.3453' in result,False)
        self.assertEqual('1543,567' in result,False)
        self.assertEqual('1543' in result,True)
        
    
    def test_lowercasing(self):
        wordlist=["HELLO","WHAT","1234"]
        result=futils.lowercase_words(wordlist)
        self.assertEqual('1234' in result,True)
        self.assertEqual('hello' in result,True)
        self.assertEqual('what' in result,True)
    
    def test_stemwords(self):
        wordlist=["hello","dogs","friends","walked"]
        result=futils.stem_words(wordlist)
        self.assertEqual('hello' in result,True)
        self.assertEqual('dog' in result,True)
        self.assertEqual('friend' in result,True)
        self.assertEqual('walk' in result,True)
        self.assertEqual('walked' in result,False)
    
    def test_count_frequency(self):
        wordlist=["hello","hello","pizza","pizza","pizza","toast"]
        freq=futils.count_frequency(wordlist)
        counts={}
        for word,frequency in freq.items():
            counts[word]=frequency
        self.assertEqual(counts['hello'],2)
        self.assertEqual(counts['pizza'],3)
        self.assertEqual(counts['toast'],1)
       
        
        

if __name__ == '__main__':
    unittest.main()