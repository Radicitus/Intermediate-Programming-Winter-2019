from distance_helper import min_dist
import prompt


class Misspelling:
    # __init__ must call this method so I can test Misspelling more easily.
    # This method should consist of only new bindings to attribute names.
    # It should (and will when I grade it) always have a list binding
    #   self.last = some value
    # You may put your own bindings here using any names to test your code;
    #   when I grade your work, I will replace the contents of this method
    #   but the last binding will always be to the attribute last
    def initialize_attributes(self):
        self.amoral = 1
        self.more   = 2
        self.babel  = 3
        self.last   = 4
        
    def __init__(self, fix_when_setting=False):
        self.fix_when_setting = fix_when_setting
        self.initialize_attributes()     

    def closest_matches(self, name):
        attributes = sorted(((k, (min_dist(k, name))) for k, v in self.__dict__.items()), key=lambda x: x[1])
        c_match = []
        val = attributes[0][1]
        for item in attributes:
            if item[1] == val and val <= len(name)/2:
                c_match.append(item[0])
        return c_match

    def __getattr__(self, name):
        c_match = self.closest_matches(name)
        if len(c_match) == 0 or len(c_match) > 1:
            raise NameError("Misspelling.__getattr__: " + str(name) + " has too little or too many matches")
        return self.__dict__[c_match[0]]

    def __setattr__(self, name, value):
        if 'last' not in self.__dict__:
            self.__dict__[name] = value
        elif name in self.__dict__:
            self.__dict__[name] = value
        elif name not in self.__dict__ and not self.fix_when_setting:
            raise NameError("Misspelling.__setattr__: name(" + str(name) + ") not found and spelling correction disabled")
        elif self.fix_when_setting:
            c_match = self.closest_matches(name)
            if len(c_match) == 0 or len(c_match) > 1:
                raise NameError("Misspelling.__setattr__: " + str(name) + " has too little or too many matches")
            self.__dict__[c_match[0]] = value
        else:
            self.__dict__[name] = value

# I cannot supply a batch self-check for this problem until next week.

# You should try to understand the specifications and test your code
#   to ensure it works correctly, according to the specification.
# You are all allowed to ask "what should my code do..." questions online
#   both before and after I post my batch self_check file.
# The driver below will allow you to easily test your code.

if __name__ == '__main__':
    o = Misspelling(prompt.for_bool("Allow fixing mispelling in __setattr__",True))
    # Put code here to test object o the same way each time the code is run
    
    
    # # Use the while loop below to type in code one on-the-fly when prompted
    # while True:
    #     try:
    #         print("\n" + str(o.__dict__))
    #         test = prompt.for_string("Enter test")
    #         if test == "quit":
    #             break;
    #         if '=' not in test:
    #             print(eval(test))
    #         else:
    #             exec(test)
    #     except Exception as exc:
    #         print(exc)



    print()
    import driver
    
    driver.default_file_name = 'bscq32W19.txt'
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
