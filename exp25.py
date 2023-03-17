import time
import traceback

class MyException(Exception):
    pass
def test():
    raise Exception()

while True:
    try:
        test()
    except MyException:
        print('fuck')
    except:
        print("=========exception==========")
        traceback.print_exc()

    time.sleep(2)
