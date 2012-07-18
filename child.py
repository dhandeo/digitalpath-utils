#!c:/python27x64/python.exe
import time 
import sys

for i in range(20):
    print "Progress = ", i, "%"
    sys.stdout.flush()
    time.sleep(0.2)