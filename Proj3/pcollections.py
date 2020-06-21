import re, traceback, keyword


def pnamedtuple(type_name, field_names, mutable =False):
    def show_listing(s):
        for line_num, line_text in enumerate(s.split('\n'),1):
            print(f' {line_num: >3} {line_text.rstrip()}')

    def check_names(t_nm, f_nms):
        def legal_name(name):
            pattern = re.compile('^[a-zA-Z][a-zA-Z1-9_]*$')
            if re.fullmatch(pattern, name) is None or name in keyword.kwlist:
                raise SyntaxError(
                    'pnamedtuple(' + str(name) + ',' + str(field_names) + ',' + str(mutable) + '): ' + str(
                        name) + ' is not a legal name')

        def unique(iterable):
            iterated = set()
            for i in iterable:
                if i not in iterated:
                    iterated.add(i)
                    yield i

        return (t_nm, unique(f_nms)) if legal_name(t_nm) and legal_name(item for item in unique(f_nms)) else None

    # if type(type_name) == str and legal_name(type_name):
    #     pass
    # else: raise SyntaxError
    #
    # if type(field_names) == list:
    #     pass
    # elif type(field_names) == str:
    #     field_names = re.split(r'[,\s]*', field_names)
    # else: raise SyntaxError
    #
    # for name in field_names:
    #     if legal_name(name):
    #         continue
    #     else:
    #         raise SyntaxError

    field_names = list(check_names(type_name, field_names)[1])
    
    class_template = \
    'class'+type_name+':'\
        'def __init__(self, '+','.join([i for i in field_names])+'):'\
            '\n'.join(["self."+i+" = {i}" for i in field_names])

    # bind class_definition (used below) to the string constructed for the class
    class_definition = \
      class_template.format(i = '['+','.join(["'"+i+"'" for i in filters])+']')
      
    # While debugging, uncomment the next line showing source code for the class
    show_listing(class_definition)

    # Execute this class_definition -a str- in a local name space; then, bind the
    #   source_code attribute to class_definition; after the try, return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):     
        show_listing(class_definition)
        traceback.print_exc() 
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test pnamedtuple below in script: use Point = pnamedtuple('Point','x,y')

    #driver tests
    import driver
    driver.default_file_name = 'bscp3W19.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
