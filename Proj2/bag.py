# Submitter: cencenzo(Encenzo, Chloe)
# Partner  : crsherry(Sherry, Cameron)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming

from collections import defaultdict


class Bag:
    def __init__(self, items=[]):
        self.bag = defaultdict(int)
        for i in items:
            self.bag[i] += 1
    
    def __repr__(self):
        bag_list = []
        for k, v in self.bag.items():
            bag_list.extend(list(k*v))
        return 'Bag(' + str(bag_list) + ')'
    
    def __str__(self):
        return 'Bag(' + ','.join(k + '[' + str(v) + ']' for k, v in self.bag.items()) + ')'
    
    def __len__(self):
        return sum(self.bag.values())
    
    def unique(self):
        return len(self.bag.keys())
    
    def __contains__(self, item):
        return item in self.bag
    
    def count(self, item):
        if item in self.bag:
            return self.bag[item]
        return 0
    
    def add(self, item):
        if item in self.bag:
            self.bag[item] += 1
        else:
            self.bag[item] = 1
    
    def __add__(self, right):
        bag1_list, bag2_list = [], []
        if isinstance(self, Bag) and isinstance(right, Bag):
            for k, v in self.bag.items():
                bag1_list.extend(list(k*v))
            for k, v in right.bag.items():
                bag2_list.extend(list(k*v))
            return Bag(bag1_list+bag2_list)
        else:
            return NotImplemented
            
    def remove(self, item):
        if item in self.bag:
            if self.bag[item] == 1:
                del self.bag[item]
            else:
                self.bag[item] -= 1
        else:
            raise ValueError
    
    def __eq__(self, right):
        if isinstance(self, Bag) and isinstance(right, Bag):
            if self.bag.items() == right.bag.items():
                return True
            return False
        else:
            return NotImplemented
    
    def __ne__(self, right):
        return not(self == right)
    
    def __iter__(self):
        bag_list = []
        for k, v in self.bag.items():
            bag_list.extend(list(k*v))
        return iter(bag_list)
    

if __name__ == '__main__':
    b = Bag(['d','a','d','b','c','b','d'])
    print(repr(b))
    print(all((repr(b).count('\''+v+'\'')==c for v,c in dict(a=1,b=2,c=1,d=3).items())))

    b2 = Bag(['a','a','b','x','d'])
    print(repr(b2+b2))
    print(str(b2+b2))
    print([repr(b2+b2).count('\''+v+'\'') for v in 'abdx'])
    b = Bag(['a','b','a'])
    print(repr(b))
    print()

    import driver
    driver.default_file_name = 'bscp21W19.txt'
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
