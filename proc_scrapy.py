import os
import sys
import subprocess
file_object = open('list.txt')
for line in file_object:
    print line

p=subprocess.Popen('scrapy crawl -a dt=20150327 dmoz',shell=True)
