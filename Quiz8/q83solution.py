from bag import Bag
import unittest  # use unittest.TestCase
import random    # use random.shuffle, random.randint
  #random.shuffle(alist) mutates its argument alist
  #random.randint(1,10)  returns a random number in the inclusive range 1-10


class Test_Bag(unittest.TestCase):

    def setUp(self):
        self.alist = ['d', 'a', 'b', 'd', 'c', 'b', 'd']
        self.bag = Bag(self.alist)

    def test_len(self):
        random.shuffle(self.alist)
        self.assertTrue(len(self.bag) == 7, 'len of bag not 7')
        for item in self.alist:
            count = len(self.bag)
            self.bag.remove(item)
            self.assertTrue(count - 1 == len(self.bag), 'len of bag did not decrease by 1')
        self.assertTrue(len(self.bag) == 0, 'len of bag did not eventually become 0')
        return True

    def test_unique(self):
        random.shuffle(self.alist)
        self.assertTrue(len(self.bag.counts) == 4, 'incorrect number of initial unique items')
        while len(self.alist) != 0:
            self.bag.remove(self.alist.pop(0))
            self.assertTrue(len(self.bag.counts) == self.bag.unique(), 'incorrect number of unique values')

    def test_contains(self):
        for item in ['a', 'b', 'c', 'd', 'x']:
            self.assertIn(item, self.bag, 'a,b,c,d not in bag') if item is not 'x' else self.assertNotIn(item, self.bag, 'x is in bag')

    def test_count(self):
        self.assertDictEqual(dict(self.bag.counts), {'a': 1, 'b': 2, 'c': 1, 'd': 3}, 'incorrect number of initial values')
        random.shuffle(self.alist)
        for item in self.alist:
            sum_of_counts = sum(self.bag.count(key) for key in ['a', 'b', 'c', 'd'])
            self.bag.remove(item)
            sum_of_counts2 = sum(self.bag.count(key) for key in ['a', 'b', 'c', 'd'])
            self.assertTrue(sum_of_counts - 1 == sum_of_counts2, 'count did not decrease by 1')
        self.assertTrue(sum(self.bag.count(key) for key in ['a', 'b', 'c', 'd']) == 0, 'sum of counts did not reach 0')

    def test_equals(self):
        vals = [random.randint(1, 10) for i in range(1000)]
        bag1 = Bag(vals)
        random.shuffle(vals)
        bag2 = Bag(vals)
        self.assertTrue(bag1 == bag2, 'bags are not equal')
        bag1.remove(vals[0])
        self.assertFalse(bag1 == bag2, 'bags are not supposed to be equal')

    def test_add(self):
        vals = [random.randint(1, 10) for i in range(1000)]
        bag1 = Bag(vals)
        random.shuffle(vals)
        bag2 = Bag()
        for item in vals:
            bag2.add(item)
        self.assertEqual(bag1, bag2, 'bags are not equal')

    def test_remove(self):
        vals = [random.randint(1, 10) for i in range(1000)]
        bag1 = Bag(vals)
        self.assertRaises(ValueError, lambda: bag1.remove(35))
        bag2 = Bag(vals)
        random.shuffle(vals)
        for item in vals:
            bag2.add(item)
        for item in vals:
            bag2.remove(item)
        self.assertEqual(bag1, bag2, 'bags are not equal')



