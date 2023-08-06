
def help():
    message = '\n\nFollowing are the available functionalities with this library\n\n'
    message += '1. add_numbers(*args)\t\t - takes variable agruments and adds them.\n'
    message += '2. subtract_numbers(*args)\t - takes variable agruments and subtracts them.\n'
    message += '3. multiply_numbers(*args)\t - takes variable agruments and multiplies them.\n'
    message += '4. divide_numbers(*args)\t - takes variable agruments and divides them.\n\n'
    message += "In all the above functions, if argument size = 0, function returns float('-inf')\n\n"

    print(message)

def add_numbers(*args):
    if(len(args)>0):
        ans = args[0]
        for arg in args[1:]:
            ans += arg
        return ans
    else:
        return float('-inf')


def subtract_numbers(*args):
    if (len(args) > 0):
        ans = args[0]
        for arg in args[1:]:
            ans -= arg
        return ans
    else:
        return float('-inf')


def multiply_numbers(*args):
    if (len(args) > 0):
        ans = args[0]
        for arg in args[1:]:
            ans *= arg
        return ans
    else:
        return float('-inf')


def divide_numbers(*args):
    if (len(args) > 0):
        ans = args[0]
        for arg in args[1:]:
            ans /= arg
        return ans
    else:
        return float('-inf')
