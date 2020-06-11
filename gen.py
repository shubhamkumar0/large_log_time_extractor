import csv
import re

output_file = open('result2.txt','a')
for i in range(1000):
    output_file.write("{0}-06-08T01:49:48Z \n".format(1900+i))
output_file.close()
