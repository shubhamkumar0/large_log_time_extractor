import csv
import re

#script to write dummy dates in a file
output_file = open('largefile.txt','a')
for i in range(1000):
    output_file.write("{0}-06-08T01:49:48Z \n".format(1900+i))
output_file.close()
