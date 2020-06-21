# Submitter: cencenzo(Encenzo, Chloe)
# Partner  : crsherry(Sherry, Cameron)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming


from goody import type_as_str
import inspect
from distutils.command.check import check
#from builtins import True


class Check_All_OK:
    def __init__(self, *args):
        self._annotations = args

    def __repr__(self):
        return 'Check_All_OK(' + ','.join([str(i) for i in self._annotations]) + ')'

    def __check_annotation__(self, check, param, value, check_history):
        for annot in self._annotations:
            check(param, annot, {param: value},
                  check_history + 'Check_All_OK check: ' + str(annot) + ' while trying: ' + str(self) + '\n')


class Check_Any_OK:

    def __init__(self, *args):
        self._annotations = args

    def __repr__(self):
        return 'Check_Any_OK(' + ','.join([str(i) for i in self._annotations]) + ')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations:
            try:
                check(param, annot, {param: value}, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param) + ' failed annotation check(Check_Any_OK): value = ' + repr(value) + \
                          '\n  tried ' + str(self) + '\n' + check_history


class Check_Annotation:
    checking_on = True

    def __init__(self, f):
        self._f = f
        self._checking_on = True

    def check(self, param, annot, value, check_history=''):
        check_history_list = [check_history]
        
        def error_message():
            if type(annot) is type:
                return "AssertionError: " + repr(param) + " failed annotation check(wrong type): value = " + repr(value[param]) + \
                       "\n   was type " + type_as_str(value[param]) + " ...should be type " + str(annot.__name__) + "\n" + ''.join(check_history_list)
            else:
                return "AssertionError: " + repr(param) + " failed annotation check(wrong type): value = " + repr(value[param]) + \
                       "\n   was type " + type_as_str(value[param]) + " ...should be type " + str(type(annot).__name__) + "\n" + ''.join(check_history_list)

        def check_type():
            if isinstance(value[param], annot):
                return
            else:
                message = error_message()
                print(message)
                assert False, message

        def check_list_or_tuple():
            if isinstance(value[param], type(annot)) and len(value[param]) >= 1:
                if len(annot) == 1:
                    for item in value[param]:
                        check_history = str(type(annot).__name__) + '[' + str(value[param].index(item)) + '] check: ' + str(annot[0]) + '\n'
                        check_history_list.append(check_history)
                        self.check(param, annot[0], {param: item}, ''.join(check_history_list))
                        check_history_list.pop()
                    return
                else:
                    if len(annot) != len(value[param]):
                        message = "AssertionError: " + repr(param) + " failed annotation check(wrong number of elements): value = " + repr(value[param]) + \
                                  "\n   annotation had " + str(len(annot)) + " elements" + str(annot)
                        print(message)
                        assert False, message
                    else:
                        for item in value[param]:
                            check_history = str(type(annot).__name__) + '[' + str(value[param].index(item)) + '] check: ' + str(annot[value[param].index(item)]) + '\n'
                            check_history_list.append(check_history)
                            self.check(param, annot[value[param].index(item)], {param: item}, ''.join(check_history_list))
                            check_history_list.pop()
            else:
                message = error_message()
                print(message)
                assert False, message

        def check_dict():
            if isinstance(value[param], dict):
                if len(annot.items()) == 1:
                    for k in value[param].keys():
                        k_annot = list(annot.keys())[0]
                        check_history = 'dict key check: ' + str(k_annot) + '\n'
                        check_history_list.append(check_history)
                        self.check(param, k_annot, {param: k}, ''.join(check_history_list))
                        check_history_list.pop()
                    for v in value[param].values():
                        v_annot = list(annot.values())[0]
                        check_history = 'dict value check: ' + str(v_annot) + '\n'
                        check_history_list.append(check_history)
                        self.check(param, v_annot, {param: v}, ''.join(check_history_list))
                        check_history_list.pop()
                    return
                else:
                    message = "AssertionError: " + repr(param) + " annotation inconsistency: dict should have 1 item but had 2" + \
                              "\n   annotation = " + str(annot)
                    print(message)
                    assert False, message
            else:
                message = error_message()
                print(message)
                assert False, message

        def check_set_or_frozen_set():
            if isinstance(value[param], type(annot)):
                if len(annot) == 1:
                    s_annot = list(annot)[0]
                    s_to_list = list(value[param])
                    for item in s_to_list:
                        curr_index = s_to_list.index(item)
                        check_history = str(type(annot).__name__) + " value check: " + str(s_annot) + '\n'
                        check_history_list.append(check_history)
                        self.check(param, s_annot, {param: s_to_list[curr_index]}, ''.join(check_history_list))
                        check_history_list.pop()
                    return
                else:
                    message = "AssertionError: " + repr(param) + " annotation inconsistency: " + str(type(annot).__name__) + " should have 1 value but had 2" + \
                              "\n   annotation = " + str(annot)
                    print(message)
                    assert False, message
            else:
                message = error_message()
                print(message)
                assert False, message

        def check_lambda():
            if len(annot.__code__.co_varnames) == 1:
                try:
                    result = annot(value[param])
                except Exception as exceptObj:
                    message = "AssertionError: " + repr(param) + " annotation predicate(" + str(annot) + ") raised exception" + \
                              "\n   exception = " + str(exceptObj) + "\n" + ''.join(check_history_list)
                    print(message)
                    assert False, message
                if result:
                    return
                else:
                    message = "AssertionError: " + repr(param) + " failed annotation check: value = " + repr(value[param]) + \
                              "\n   predicate = " + str(annot) + "\n" + ''.join(check_history_list)
                    print(message)
                    assert False, message
            else:
                message = "predicate should have 1 parameter but had " + str(len(annot.__code__.co_varnames)) + \
                          "\n   predicate = " + str(annot)
                print(message)
                assert False, message

        def check_string():
            param_dict = dict()
            param_dict[param] = value[param]

            def res(result):
                if result:
                    return
                else:
                    message = "Assertion Error: " + repr(param) + " failed annotation check(str predicate: " + \
                               repr(annot) + " args for evaluation: " + str(list(param_dict.keys())[0]) + "->" + \
                               str(list(param_dict.values())[0])
                               
                    if len(list(param_dict.items())) > 1:
                        param_dict_iter = iter(param_dict)
                        next(param_dict_iter)
                        for item in param_dict_iter:
                            message += ", " + str(item) + "->" + str(param_dict[item])
                    message += ''.join(check_history_list) + "\n"
                    print(message)
                    assert False, message

            try:
                while True:
                    try:
                        result = eval(annot, {'_builtins__': {}}, param_dict)
                        res(result)
                        break
                    except NameError as exceptObj:
                        error_param = str(exceptObj).split("'")[1]
                        error_val = value[error_param]
                        param_dict[error_param] = error_val
            except AssertionError:
                raise
            except Exception as exceptObj:
                message = "Assertion Error: " + repr(param) + " annotation check(str predicate: " + \
                           repr(annot) + "raised exception = " + repr(exceptObj) + ''.join(check_history_list) + "\n"
                print(message)
                assert False, message

        def check_other():
            if hasattr(annot, '__check_annotation__'):
                try:
                    annot.__check_annotation__(self.check, param, value[param], ''.join(check_history_list))
                except AssertionError:
                    raise
                except Exception as exceptObj:
                    message = "AssertionError: " + repr(param) + " annotation predicate(" + str(annot) + ") raised exception" + \
                              "\n   exception = " + str(exceptObj) + "\n" + ''.join(check_history_list)
                    print(message)
                    assert False, message
            else:
                message = "Assertion Error: " + repr(param) + " annotation undecipherable: " + \
                           str(type(annot).__name__) + "(" + str(type(param)) + "[" + repr(value[param]) + "])\n"
                print(message)
                assert False, message

        if annot is None:                                               return
        elif isinstance(annot, str):                                    check_string()
        elif type(annot) is type:                                       check_type()
        elif isinstance(annot, list) or isinstance(annot, tuple):       check_list_or_tuple()
        elif isinstance(annot, set) or isinstance(annot, frozenset):    check_set_or_frozen_set()
        elif isinstance(annot, dict):                                   check_dict()
        elif inspect.isfunction(annot):                                 check_lambda()
        else:                                                           check_other()

    def __call__(self, *args, **kargs):
        def param_arg_bindings():
            f_signature = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args, **kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        if not (self.checking_on and self._checking_on):
            return self._f(*args, **kargs)

        param_to_arg = param_arg_bindings()
        try:
            for param, annot in self._f.__annotations__.items():
                if param is 'return':
                    break
                self.check(param, annot, param_to_arg)
            result = self._f(*args, **kargs)
            if 'return' in self._f.__annotations__:
                param_to_arg['_return'] = result
                self.check('_return', self._f.__annotations__['return'], param_to_arg)
            return result

        except AssertionError:
            # print(80*'-')
            # for l in inspect.getsourcelines(self._f)[0]:
            #    print(l.rstrip())
            # print(80*'-')
            raise


if __name__ == '__main__':
    # driver tests
    # @Check_Annotation
    # def f(x: [[int]]): pass
    #
    #
    # f([[1, 2], [3, 4], [5, 'a']])

    import driver
    driver.default_file_name = 'bscp4W19.txt'
    #     driver.default_show_exception= True
    #     driver.default_show_exception_message= True
    #     driver.default_show_traceback= True
    driver.driver()
