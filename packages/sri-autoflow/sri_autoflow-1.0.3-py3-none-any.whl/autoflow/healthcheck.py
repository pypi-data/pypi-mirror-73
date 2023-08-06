import sys
import time
import datetime

def main(argv):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("SRI TA2: Health Check: " + st)
    exit(0)

if __name__ == "__main__":
    main(sys.argv)