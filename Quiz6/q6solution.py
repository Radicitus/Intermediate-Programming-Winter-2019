import prompt
from goody import irange
from collections import defaultdict


# List Node class and helper functions (to set up problem)

class LN:
    created = 0
    def __init__(self,value,next=None):
        self.value = value
        self.next  = next
        LN.created  += 1

def list_to_ll(l):
    if l == []:
        return None
    front = rear = LN(l[0])
    for v in l[1:]:
        rear.next = LN(v)
        rear = rear.next
    return front

def str_ll(ll):
    answer = ''
    while ll != None:
        answer += str(ll.value)+'->'
        ll = ll.next
    return answer + 'None'



# Tree Node class and helper functions (to set up problem)

class TN:
    def __init__(self,value,left=None,right=None):
        self.value = value
        self.left  = left
        self.right = right

def list_to_tree(alist):
    if alist == None:
        return None
    else:
        return TN(alist[0],list_to_tree(alist[1]),list_to_tree(alist[2])) 
    
def str_tree(atree,indent_char ='.',indent_delta=2):
    def str_tree_1(indent,atree):
        if atree == None:
            return ''
        else:
            answer = ''
            answer += str_tree_1(indent+indent_delta,atree.right)
            answer += indent*indent_char+str(atree.value)+'\n'
            answer += str_tree_1(indent+indent_delta,atree.left)
            return answer
    return str_tree_1(0,atree) 


# Define alternate ITERATIVELY

def alternate_i(ll1 : LN, ll2 : LN) -> LN:
    # Handle the case of ll1 or ll2 being empty
    
    # Set up for iteration (keep track of front and rear of linked list to retur

    
    # while True: with both l1 and l2 not empty and ll1 is in the linked list to return
    while True:
        break
        # return correct result if ll1 or ll2 is empty (after advancing ll1 and ll2)
        # continue looping if both ll1/ll2 are not empty, with ll1 in the linked list to return        


# Define alternate RECURSIVELY

def alternate_r(ll1 : LN, ll2 : LN) -> LN:
    if ll1 is None and ll2 is None:
        return None
    elif ll1 is None:
        return ll2
    elif ll2 is None:
        return ll1
    else:
        ll1.next = alternate_r(ll2, ll1.next)
        return ll1


def count(t,value):
    if t is None:
        return 0
    else:
        if t.value == value:
            return 1 + count(t.left, value) + count(t.right, value)
        else:
            return 0 + count(t.left, value) + count(t.right, value)


class bidict(dict):
    obj_list = []

    def __init__(self, initial = [], **kwargs):
        dict.__init__(self, initial, **kwargs)
        self._rdict = defaultdict(set)
        for k, v in self.items():
            if self._is_hashable(k) and self._is_hashable(v):
                self._rdict[v] = k
        bidict.obj_list.append(self)

    def __setitem__(self, key, value):
        if key in self:
            self._rdict[self[key]].remove(key)
            if self._rdict[self[key]] == set():
                del self._rdict[self[key]]
            self._rdict[value] = key
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        self._rdict[self[key]].remove(key)
        if self._rdict[self[key]] == set():
            del self._rdict[self[key]]
        dict.__delitem__(self, key)

    def __call__(self, value):
        return self._rdict[value]

    def clear(self):
        dict.clear(self)
        self._rdict.clear()

    @staticmethod
    def all_objects():
        return bidict.obj_list

    @staticmethod
    def forget(object):
        bidict.obj_list.remove(object)

    @staticmethod
    def _is_hashable(value):
        if hasattr(value, '__iter__'):
            return all(bidict._is_hashable(it) for it in value)
        if hasattr(value, '__hash__') and getattr(value, '__hash__') is not None:
            return True
        else:
            raise ValueError

    import driver
    driver.default_file_name = 'bscq6W19.txt'
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    print('\n\n')
    driver.driver()
    
