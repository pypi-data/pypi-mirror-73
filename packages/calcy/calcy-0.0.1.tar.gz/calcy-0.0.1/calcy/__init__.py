
def add_numbers(*args):
    if(len(args)>0):
        ans = args[0]
        for arg in args[1:]:
            ans += arg
        return ans
    else:
        return "[Argument Error] : input atleast one argument\n"


def subtract_numbers(*args):
    if (len(args) > 0):
        ans = args[0]
        for arg in args[1:]:
            ans -= arg
        return ans
    else:
        return "[Argument Error] : input atleast one argument\n"


def multiply_numbers(*args):
    if (len(args) > 0):
        ans = args[0]
        for arg in args[1:]:
            ans *= arg
        return ans
    else:
        return "[Argument Error] : input atleast one argument\n"


def divide_numbers(*args):
    if (len(args) > 0):
        ans = args[0]
        for arg in args[1:]:
            ans /= arg
        return ans
    else:
        return "[Argument Error] : input atleast one argument\n"

