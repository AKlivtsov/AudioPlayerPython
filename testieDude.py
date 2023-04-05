import speedtest

s = speedtest.Speedtest()

def speedy():
    print(s.download())

def print_cube(num):
    """
    function to print cube of given num
    """
    print("Cube: {}".format(num * num * num))
 
def print_square(num):
    """
    function to print square of given num
    """
    print("Square: {}".format(num * num))

def hard_math(num, times):

    times_ = 0

    while times_ != times:
        num *= num
        times_ += 1

    print(f"Num: {num} and times: {times}")

speedy()
print_cube(10)
print_square(10)
hard_math(3932345234, 10)
print("Done!")