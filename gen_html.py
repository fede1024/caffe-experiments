#!/usr/bin/python

import os, sys

#stream = os.popen("bash -c 'python imagenet.py /home/federico/tmp/images/* 2>&1'")
#stream = os.popen("python imagenet.py /home/federico/tmp/images/*")

stream = sys.stdin

print "<html>"
print "<body>"

print "<h1>ImageNet test</h1>"

print "<h2>"
print stream.readline()
print stream.readline()
print "</h2>"

print "<pre>"

for line in stream:
    line = line.strip()
    if line[0:7] == "Image: ":
        print "</pre>"
        print "<h2>", line, "</h2>"
        print "<img src='%s' width='500px'></img>"%(line[7:])
        print "<pre>"
    else:
        print line

print "</pre>"
print "</body>"
print "</html>"
