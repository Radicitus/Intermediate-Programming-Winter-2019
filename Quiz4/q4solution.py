import prompt
from helpers import primes, hide, nth, mini_Backwardable_test, Backwardable_test


def running_count(iterable,p):
    count = 0
    for item in iterable:
        if p(item): count += 1
        yield count


def stop_when(iterable,p):
    for item in iterable:
        if not p(item): yield item
        else: return


def yield_and_skip(iterable):
    iterator = iter(iterable)
    for item in iterator:
        if isinstance(item, int):
            count = item
            yield item
            while count != 0:
                try: next(iterator)
                except: return
                count -= 1
        else: yield item


def windows(iterable, n, m=1):
    iterator = iter(iterable)
    i_list = [iterator.__next__() for i in range(n)]
    yield i_list
    n_list = [item for item in i_list[m:]]
    while True:
        try: m_list = [iterator.__next__() for i in range(m)]
        except: return
        l_ret = [item for item in n_list]
        for item in m_list: l_ret.append(item)
        yield [item for item in l_ret]
        n_list = [item for item in l_ret[m:]]


def alternate(*iterables):
    arg_list = [iter(arg) for arg in iterables]
    while True:
        for arg in arg_list:
            try: yield arg.__next__()
            except: return


def myzip(*iterables):
    arg_list = [iter(arg) for arg in iterables]
    t_list, alt_count = [], len(arg_list)
    while True:
        count = 0
        for arg in arg_list:
            try:
               t_list.append(arg.__next__())
            except:
                t_list.append(None)
                count += 1
        if count == alt_count: return
        yield tuple(t_list)
        t_list.clear()


class Backwardable:
    def __init__(self, iterable):
        self._iterable = iterable
            
    def __iter__(self):
        class B_iter:
            def __init__(self, iterable):
                self._all = []
                self._iterator = iter(iterable)
                self._index = -1
        
            def __str__(self):
                return '_all={}, _index={}'.format(self._all, self._index)

            def __next__(self):
                self._index += 1
                if self._index >= len(self._all):
                    try:
                        item = self._iterator.__next__()
                    except:
                        self._index -= 1
                        raise StopIteration
                    self._all.append(item)
                    return item
                else: return self._all[self._index]
                
            def __prev__(self):
                self._index -= 1
                if self._index >= 0:
                    return self._all[self._index]
                else:
                    self._index += 1
                    raise AssertionError
            
            def __clear__(self):
                if 0 <= self._index < len(self._all):
                    del self._all[:self._index]
                    self._index = 0
                else: del self._all[:]
        return B_iter(self._iterable)


def prev(x): return x.__prev__()


def clear(x): x.__clear__()


if __name__ == '__main__':
    
    # Test running_count; you can add your own test cases
    print('\nTesting running_count')
    for i in running_count('bananastand',lambda x : x in 'aeiou'): # is vowel
        print(i,end=' ')
    print()

    for i in running_count(hide('bananastand'),lambda x : x in 'aeiou'): # is vowel
        print(i,end=' ')
    print()

    print(nth(running_count(primes(),lambda x : x%10 == 3),1000))


    # Test stop_when; you can add your own test cases
    print('\nTesting stop_when')
    for c in stop_when('abcdefghijk', lambda x : x >='d'):
        print(c,end='')
    print()

    for c in stop_when(hide('abcdefghijk'), lambda x : x >='d'):
        print(c,end='')
    print('\n')

    print(nth(stop_when(primes(),lambda x : x > 100000),100))


    # Test group_when; you can add your own test cases
    print('\nTesting yield_and_skip')
    for i in yield_and_skip([1, 2, 1, 3, 'a', 'b', 2, 5, 'c', 1, 2, 3, 8, 'x', 'y', 'z', 2]):
        print(i,end=' ')
    print()

    for i in yield_and_skip(hide([1, 2, 1, 3, 'a', 'b', 2, 5, 'c', 1, 2, 3, 8, 'x', 'y', 'z', 2])):
        print(i,end=' ')
    print()

    print(nth(yield_and_skip(primes()),5))


    # Test windows; you can add your own test cases
    print('\nTesting windows')
    for i in windows('abcdefghijk',4,2):
        print(i,end=' ')
    print()

    print('\nTesting windows on hidden')
    for i in windows(hide('abcdefghijk'),4,2):
        print(i,end=' ')
    print()

    print(nth(windows(primes(),10,5),20))


    # Test alternate; add your own test cases
    print('\nTesting alternate')
    for i in alternate('abcde','fg','hijk'):
        print(i,end='')
    print()

    for i in alternate(hide('abcde'), hide('fg'),hide('hijk')):
        print(i,end='')
    print()

    for i in alternate(primes(20), hide('fghi'),hide('jk')):
        print(i,end='')
    print()

    print(nth(alternate(primes(),primes()),50))


    # Test myzip; add your own test cases
    print('\nTesting myzip')
    for i in myzip('abcde','fg','hijk'):
        print(i,end='')
    print()

    for i in myzip(hide('abcde'), hide('fg'),hide('hijk')):
        print(i,end='')
    print()

    for i in myzip(primes(20), hide('fghi'),hide('jk')):
        print(i,end='')
    print('\n')

    print(nth(myzip(primes(),primes()),50))




    # Test Backwardable; add your own test cases
    print('\nTesting Backwardable')
    s = 'abcde'
    i = iter(Backwardable(s))
    print(i)
    print(next(i),i) #a
    print(next(i),i) #b
    print(next(i),i) #c
    print(prev(i),i) #b
    print(prev(i),i) #a
    try:
        print(prev(i),i)
    except AssertionError:
        print('Tried to prev before first value')
    print(next(i),i) #b
    print(next(i),i) #c
    print(clear(i),i)#None: a, b gone]
    print(next(i),i) #d
    print(next(i),i) #e
    print(prev(i),i) #d
    print(prev(i),i) #c
    try:
        print(prev(i),i)
    except AssertionError:
        print('Tried to prev before first value (after clear)')
    print(next(i),i) #d
    print(next(i),i) #e
    try:
        print(next(i),i)
    except StopIteration:
        print('Correctly raised StopIteration')

    # See the mini_Backwardable_test code, which allows you to call
    #  interleaved sequences of next and prev, or quit
    mini_Backwardable_test(iter(Backwardable('abc')))
    mini_Backwardable_test(iter(Backwardable([0,1,2,3,4])))
    mini_Backwardable_test(iter(Backwardable(primes())))

    import driver
    driver.default_file_name = 'bscq4W19.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()

