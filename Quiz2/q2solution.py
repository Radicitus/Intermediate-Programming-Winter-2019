import re
from goody import irange
from collections import defaultdict

# Before running the driver on the bsc.txt file, ensure you have put a regular
#   expression pattern in the files repattern1a.txt, repattern1b.txt, and
#   repattern2a.txt. The patterns must be all on the first line

def expand_re(pat_dict:{str:str}):
    for pattern in pat_dict:
        for s_pattern in pat_dict:
            if pattern in pat_dict[s_pattern]:
                pat_dict[s_pattern] = re.sub('#'+pattern+'#', "(?:" + str(pat_dict[pattern]) + ")", str(pat_dict[s_pattern]))



def match_params_args(params_string : str, args_string : str, trace = False) -> {str:int}:
    if not params_string and not args_string:
        return {}
    args_pat = re.compile("^(?:(?P<name>[a-zA-Z_][\w]*)=)?(?P<value>[-]?[0-9]+)$")
    params_pat = re.compile("^(?P<star>\*)?(?P<name>[a-zA-z_][\w]*)(?:=(?P<value>[-]?[\w]+))?$")
    list_params = [params_pat.match(param) for param in params_string.split(",")]
    list_args = [args_pat.match(args) for args in args_string.split(",")]
    p_a_dict = {}
    ai = 0
    for param in list_params:
        if param.group("star") is None and param.group("name") is not None and param.group("value") is None:
            if param.group("name") not in p_a_dict and ai < len(list_args):
                p_a_dict[param.group("name")] = int(list_args[ai].group("value"))
                ai += 1
            else:
                raise AssertionError
        if param.group("star") is not None and param.group("name") is not None and param.group("value") is None:
            if param.group("name") not in p_a_dict and ai < len(list_args):
                arg_list = []
                while ai < len(list_args) and list_args[ai] is not None:
                    arg_list.append(int(list_args[ai].group("value")))
                    ai += 1
                p_a_dict[param.group("name")] = tuple(arg_list)
            elif ai == len(list_args):
                p_a_dict[param.group("name")] = ()
            else:
                raise AssertionError
    if ai < len(list_args) and None not in list_args:
        raise AssertionError
    return p_a_dict









if __name__ == '__main__':
    
    p1a = open('repattern1a.txt').read().rstrip() # Read pattern on first line
    print('Testing the pattern p1a: ',p1a)
    for text in open('bm1.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1a,text)
        print(' ','Matched' if m != None else "Not matched")
         
    p1b = open('repattern1b.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p1b: ',p1b)
    for text in open('bm1.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1b,text)
        print('  ','Matched with groups ='+ str(m.groups()) if m != None else 'Not matched' )
         
         
    p2 = open('repattern2.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p2: ',p2)
    for text in open('bm2.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p2,text)
        print(' ','Matched' if m != None else "Not matched")
         
 
    print('\nTesting expand_re')
    pd = dict(digit = r'[0-9]', integer = r'[+-]?#digit##digit#*')
    print('  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary
    # {'digit': '[0-9]', 'integer': '[+-]?(?:[0-9])(?:[0-9])*'}
     
    pd = dict(integer       = r'[+-]?[0-9]+',
              integer_range = r'#integer#(..#integer#)?',
              integer_list  = r'#integer_range#(?,#integer_range#)*',
              integer_set   = r'{#integer_list#?}')
    print('\n  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary 
    # {'integer': '[+-]?[0-9]+',
    #  'integer_range': '(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?',
    #  'integer_list': '(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?)(?,(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?))*',
    #  'integer_set': '{(?:(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?)(?,(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?))*)?}'
    # }
     
    pd = dict(a='correct',b='#a#',c='#b#',d='#c#',e='#d#',f='#e#',g='#f#')
    print('\n  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary 
    # {'a': 'correct',
    #  'b': '(?:correct)',
    #  'c': '(?:(?:correct))',
    #  'd': '(?:(?:(?:correct)))',
    #  'e': '(?:(?:(?:(?:correct))))',
    #  'f': '(?:(?:(?:(?:(?:correct)))))',
    #  'g': '(?:(?:(?:(?:(?:(?:correct))))))'
    # }


    p4a = open('repattern4a.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p4a: ',p4a)
    for text in open('bm4a.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p4a,text)
        print('  ','Matched with groupdict ='+ str(m.groupdict()) if m != None else 'Not matched' )


    p4b = open('repattern4b.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p4b: ',p4b)
    for text in open('bm4b.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p4b,text)
        print('  ','Matched with groupdict ='+ str(m.groupdict()) if m != None else 'Not matched' )


    print('\nTesting match_params_args')
    print('\nTesting name-only parameters and positional arugments')
    print(match_params_args('',''))
    print(match_params_args('a','1'))
    print(match_params_args('a,b,c','1,2,3'))
    try:
        match_params_args('a,b','1,2,3')
        print('Should have raised AssertionError')
    except AssertionError as exc:
        print('***Raised AssertionError:',exc)
    try:
        match_params_args('a,b,c','1,2')
        print('Should have raised AssertionError')
    except AssertionError as exc:
        print('***Raised AssertionError:',exc)

    print('\nTesting includes *name-only parameters too')
    print(match_params_args('*args',''))
    print(match_params_args('*args','1'))
    print(match_params_args('*args','1,2'))
    print(match_params_args('a,b,*args','1,2'))
    print(match_params_args('a,b,*args','1,2,3,4',True))

    print('\nTesting includes named arguments')
    print(match_params_args('a,b,*args,c,d','1,2,3,4,c=5,d=6'))
    try:
        print(match_params_args('a,b,*args,c,d','1,2,3,4,d=5'))
        print('Should have raised AssertionError')
    except AssertionError as exc:
        print('***Raised AssertionError:',exc)
    try:
        print(match_params_args('a,b,*args,c,d','1,2,3,4,x=5'))
        print('Should have raised AssertionError')
    except AssertionError as exc:
        print('***Raised AssertionError:',exc)
    try:
        print(match_params_args('a,b,*args,c,d','1,2,3,4,c=5,d=6,a=7'))
        print('Should have raised AssertionError')
    except AssertionError as exc:
        print('***Raised AssertionError:',exc)

    print('\nTesting includes default-value parameters')
    print(match_params_args('a=1,b','b=2'))
    print(match_params_args('a,b,*args,c=5,d=6','1,2,3,4,d=5'))
        
        
        
    print()
    print()
    import driver
    driver.default_file_name = "bscq2W19.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
