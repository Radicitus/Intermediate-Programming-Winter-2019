def odd(l):
    try: return tuple([l[0]]) + tuple(odd(l[2:]))
    except: return tuple()

def compare(a,b):
    if len(a) == len(b):
        try:
            if a[0] > b[0]: return ">"
            elif a[0] < b[0]: return "<"
            else:
                try: return compare(a[1:], b[1:])
                except: return "="
        except: return "="
    else:
        if a is "": return "<"
        if b is "": return ">"
        if len(a) > len(b): return "<"
        else: return ">"


def get_assoc(assoc : ((object,object),), key : object) -> object:
    try:
        if assoc[0][0] == key: return assoc[0][1]
        else: return get_assoc(assoc[1:], key)
    except: raise KeyError


def del_assoc(assoc : ((object,object),), key : object) -> ((object,object),):
    if len(assoc) <= 1:
        try:
            if assoc[0][0] == key: return ()
            else: raise KeyError
        except: raise KeyError
    if assoc[0][0] == key: return tuple(assoc[1:])
    else: return tuple([assoc[0]]) + del_assoc(assoc[1:], key)


def set_assoc(assoc : ((object,object),), key : object, value: object) -> ((object,object),):
    if len(assoc) <= 1:
        try:
            if assoc[0][0] == key: return tuple([tuple([key, value])])
            else: return tuple([assoc[0]]) + tuple([tuple([key, value])])
        except: return tuple([tuple([key, value])])
    if assoc[0][0] == key: return tuple([tuple([key, value])]) + tuple(assoc[1:])
    else: return tuple([assoc[0]]) + set_assoc(assoc[1:], key, value)

def immutify(a : 'an int, str, list, tuple, set, or dict') -> 'an int, str, tuple, or frozenset':
        if not a: return ()
        if type(a) in (int, str, frozenset):
            return a
        elif type(a) in (tuple, list):
            return (immutify(a[0]),) + immutify(a[1:])
        elif type(a) is set:
            return frozenset(a)
        elif type(a) is dict:
            return tuple(sorted([(k, immutify(a[k])) for k in a]))
    

def my_str(l : 'int or list of ints with nested lists') -> str:
    elide = set()
    def helper(l : 'int or list of ints with nested lists') -> str:
        pass
    return helper(l)




if __name__=="__main__":
    import predicate,random,driver
    from goody import irange
    
    # print('Testing odd')
    # print(odd(()))
    # print(odd((1,)))
    # print(odd((1,2,3)))
    # print(odd((1,2,3,4,5,6,7,8,9)))
    # print(odd((0,1,2,3,4,5,6,7,8,9)))
    # print(odd(('a','b','c','d','e','f','g','h','i')))
    # print(odd(('a','b','c','d','e','f','g','h','i','j')))
    #
    # print('Testing compare')
    # print('',      compare('',''),          '')
    # print('',      compare('','abc'),       'abc')
    # print('abc',   compare('abc',''),       '')
    # print('abc',   compare('abc','abc'),    'abc')
    # print('bc',    compare('bc','abc'),     'abc')
    # print('abc',   compare('abc','bc'),     'bc')
    # print('aaaxc', compare('aaaxc','aaabc'), 'aaabc')
    # print('aaabc', compare('aaabc','aaaxc'), 'aaaxc')
    #
    # print('\nTesting get_assoc')
    # assoc = ( ('a',1), ('c',3), ('d',4), ('b',2) )
    # print(get_assoc(assoc, 'a'))
    # print(get_assoc(assoc, 'b'))
    # print(get_assoc(assoc, 'c'))
    # print(get_assoc(assoc, 'd'))
    # try:
    #     print(get_assoc(assoc, 'x'))
    # except KeyError:
    #     print('Correctly raised exception on bad key')
    #
    # print('\nTesting del_assoc')
    # assoc = ( ('a',1), ('c',3), ('d',4), ('b',2) )
    # assoc = del_assoc(assoc,'b')
    # print('assoc now =', assoc)
    # try:
    #     assoc = del_assoc(assoc, 'x')
    # except KeyError:
    #     print('Correctly raised exception on bad key')
    # assoc = del_assoc(assoc,'a')
    # print('assoc now =', assoc)
    # assoc = del_assoc(assoc,'c')
    # print('assoc now =', assoc)
    # assoc = del_assoc(assoc,'d')
    # print('assoc now =', assoc)
    #
    # print('\nTesting set_assoc')
    # assoc = ()
    # assoc = set_assoc(assoc,'b', 2)
    # print('assoc now =', assoc)
    # assoc = set_assoc(assoc,'a',1)
    # print('assoc now =', assoc)
    # assoc = set_assoc(assoc,'c',3)
    # print('assoc now =', assoc)
    # assoc = set_assoc(assoc,'d',4)
    # print('assoc now =', assoc)
    # assoc = set_assoc(assoc,'b',102)
    # print('assoc now =', assoc)
    # assoc = set_assoc(assoc,'c',103)
    # print('assoc now =', assoc)
    # assoc = set_assoc(assoc,'d',104)
    # print('assoc now =', assoc)

# ####Remove
#     print('\nTesting is_sorted')
#     print(is_sorted(()))
#     print(is_sorted((0,)))
#     print(is_sorted((-5,-4)))
#     print(is_sorted((1,2,3,4,5,6,7)))
#     print(is_sorted((1,2,3,7,4,5,6)))
#     print(is_sorted((1,2,3,4,5,6,5)))
#     print(is_sorted((7,6,5,4,3,2,1)))
#
#     print('\nTesting sort')
#     print(sort((1,2,3,4,5,6,7)))
#     print(sort((7,6,5,4,3,2,1)))
#     print(sort((4,5,3,1,2,7,6)))
#     print(sort((1,7,2,6,3,5,4)))
#     l = [i+1 for i in range(30)]
#     random.shuffle(l)
#     l = tuple(l)
#     print(l)
#     print(sort(l))
# ####Remove
    
   
    # print('\nTesting immutify')
    # print( immutify(1) )
    # print( immutify('a') )
    # print (immutify( (1, 2, 3)) )
    # print (immutify( frozenset([1, 2, 3])) )
    # print( immutify( [1, 2, 3, 4, 5, 6]) )
    # print( immutify( [1, 2, [3, [4], 5], 6]) )
    # print( immutify( [1, 2, (3, [4], 5), 6]) )
    # print( immutify( [{1,2}, {3,frozenset([4,5])}, {6,7}]))
    # print( immutify( [{1,2}, {3,frozenset([4,5])}, [{5,6}]]))
    # print( immutify( {'b' : [1,2], 'a' : {'ab': {1,2}, 'aa' : (1,2)}}) )
    
    # print('\nTesting my_str')
    # x = [1,[2,3,[4,[[5]],6]]]
    # print(str(x), 'should match the result printed below')
    # print(my_str(x))
    # x = [1,[2],3]
    # x[1] = x
    # print(str(x), 'should match the result printed below')
    # print(my_str(x))
    # x = [1,2,3]
    # x[1] = x
    # y = [10,11,12]
    # x[0] = y
    # y[2] = x
    # print(str(x), 'should match the result printed below')
    # print(my_str(x))
    # print(str(y), 'should match the result printed below')
    # print(my_str(y))
    # print()
    
    driver.default_file_name = 'bscq5W19.txt'
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
    
