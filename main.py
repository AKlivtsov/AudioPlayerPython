import threading
import speedtest

s = speedtest.Speedtest()

def speedy():
		print(str( int(s.download() //8 //1024 //1024) ))
 
def print_cube(num):
    """
    function to print cube of given num
    """
    print("Cube: {}".format(num * num * num))
 
def print_square(num):
    """
    function to print square of given num
    """
    print(f"Square: {num * num}")

def hard_math(num, times):

	times_ = 0

	while times_ != times:
		num *= num
		times_ += 1

	print(f"Num: {num} and times: {times}")

 
if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))
    t3 = threading.Thread(target=hard_math, args=(3932345234, 10))
    t4 = threading.Thread(target=speedy)
 	
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    # starting thread 3
    t3.start()
    # starting thread 3
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
 
    # both threads completely executed
    print("Done!")