#!/usr/bin/python3
import sys, getopt
ops, args = getopt.getopt(sys.argv[1:], " ")
word = args[0].lower()
time = 0
for line in sys.stdin:
    words = line.split("\W+")
    for i in words:
        if i==word:
            time += 1
print(word,"occurred", time, "times")
