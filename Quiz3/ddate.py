from goody import irange, type_as_str

class Date:
    def __init__(self, y, m, d):
        if not isinstance(y, int):
            raise AssertionError("Date.__init__: " + str(y) + " is not an int")
        if not isinstance(m, int):
            raise AssertionError("Date.__init__: " + str(m) + " is not an int")
        if not isinstance(d, int):
            raise AssertionError("Date.__init__: " + str(d) + " is not an int")
        if y < 0 or not (1 <= m <= 12) or not(1 <= d <= self.days_in(y, m)):
            raise AssertionError("Date.__init__: range error")
        self.year = y
        self.month = m
        self.day = d

    def __getitem__(self, item):
        if type(item) is str:
            if item == 'y': return self.year
            elif item == 'm': return self.month
            elif item == 'd': return self.day
            else: raise IndexError("Date.__getitem__: " + str(item) + " is not a correct date input")
        if type(item) is tuple:
            tup_tr = []
            for d_obj in item:
                if d_obj == 'y': tup_tr.append(self.year)
                elif d_obj == 'm': tup_tr.append(self.month)
                elif d_obj == 'd': tup_tr.append(self.day)
                else: raise IndexError("Date.__getitem__: " + str(item) + " is not a correct date input")
            return tuple(tup_tr)
        else: raise IndexError("Date.__getitem__: " + str(item) + " is not a string or tuple")

    def __repr__(self):
        return 'Date(' + str(self.year) + ',' + str(self.month) + ',' + str(self.day) + ')'

    def __str__(self):
        return str(self.month) + '/' + str(self.day) + '/' + str(self.year)

    def __len__(self):
        days_total = 0
        if self.year != 0:
            for years in irange(0, self.year):
                if years != self.year:
                    for months in irange(12):
                        days_total += self.days_in(years, months)
                else:
                    for months in irange(self.month - 1):
                        days_total += self.days_in(years, months)
            days_total += self.day - 1
            return days_total
        for month_self in irange(self.month - 1):
            days_total += self.days_in(self.year, month_self)
        days_total += self.day - 1
        return days_total

    def __eq__(self, right):
        if type(right) is not Date: return False
        else: return self.__str__() == right.__str__()

    def __lt__(self, right):
        if type(right) not in (Date, int):
            raise TypeError
        else:
            return self.__len__() < (right if type(right) is int else right.__len__())

    def __add__(self, right):
        if type(right) not in (Date, int):
            raise TypeError
        days_left = right
        t_year = self.year
        t_month = self.month
        t_day = self.day
        while days_left != 0:
            if days_left > 0:
                if t_day == self.days_in(t_year, t_month):
                    if t_month < 12:
                        t_month += 1
                        t_day = 1
                        days_left -= 1
                    else:
                        t_year += 1
                        t_month = 1
                        t_day = 1
                        days_left -= 1
                else:
                    t_day += 1
                    days_left -= 1
            else:
                if t_day == 1:
                    if t_month > 1:
                        t_month -= 1
                        t_day = self.days_in(t_year, t_month)
                        days_left += 1
                    else:
                        t_year -= 1
                        t_month = 12
                        t_day = self.days_in(t_year, t_month)
                        days_left += 1
                else:
                    t_day -= 1
                    days_left += 1
        return Date(t_year, t_month, t_day)

    def __radd__(self, left):
        return self.__add__(left)

    def __sub__(self, right):
        if type(right) not in (Date, int):
            raise TypeError
        if type(right) is int:
            return self.__add__(-right)
        else:
            # print(self.__len__())
            # print(right.__len__())
            return self.__len__() - right.__len__()

    def __call__(self, y, m, d):
        if not isinstance(y, int):
            raise AssertionError("Date.__call__: " + str(y) + " is not an int")
        if not isinstance(m, int):
            raise AssertionError("Date.__call__: " + str(m) + " is not an int")
        if not isinstance(d, int):
            raise AssertionError("Date.__call__: " + str(d) + " is not an int")
        if y < 0 or not (1 <= m <= 12) or not (1 <= d <= self.days_in(y, m)):
            raise AssertionError("Date.__call__: range error")
        self.year = y
        self.month = m
        self.day = d
        return None

    month_dict = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

    @staticmethod
    def is_leap_year(year):
        return (year%4 == 0 and year%100 != 0) or year%400 == 0
    
    @staticmethod
    def days_in(year,month):
        return Date.month_dict[month] + (1 if month == 2 and Date.is_leap_year(year) else 0)






    
if __name__ == '__main__':
    # Put in your own simple tests for Date before allowing driver to run

    print()
    import driver
    
    driver.default_file_name = 'bscq31.txt'
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
