#!/usr/bin/python3.8

import sys

for line in sys.stdin:
    line=line.strip()
    words=line.split(" ")
    for i in words:
        print('%s\t%s' %  ("",i))
