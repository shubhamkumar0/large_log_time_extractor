import csv
import re
import datetime
import os

#globals
datesCheck=[]
idxCheck=[]
def divideFile(inputpath, bucket_size):
    smallfile = None
    with open(inputpath) as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno % bucket_size == 0:
                if smallfile:
                    smallfile.close()
                small_filename = 'small_file_{}.txt'.format(lineno + bucket_size)
                datesCheck.append(datetime.datetime.strptime(line.strip().split(",")[0],'%Y-%m-%dT%H:%M:%SZ'))
                len=lineno
                idxCheck.append(lineno + bucket_size)
                try:
                    if os.path.exists(small_filename):
                        os.remove(small_filename)
                    smallfile = open(small_filename, "w")
                except:
                    print "File create error while creating smaller files"
            smallfile.write(line)
        if smallfile:
            smallfile.close()
    #to save space you can now safely delete the original file
    #os.remove(inputpath)


start_date_entry = str(raw_input('Enter start dateTime (i.e. 2017,7,1,17,05)'))
end_date_entry = str(raw_input('Enter end dateTime (i.e. 2017,7,1,17,05)'))
start_date = datetime.datetime.strptime(start_date_entry, '%Y,%m,%d,%H,%M')
end_date = datetime.datetime.strptime(end_date_entry, '%Y,%m,%d,%H,%M')
filePath = str(raw_input('Enter file path i.e (./largefile.txt)'))
#provide bucket size here
bucket_size = 200

divideFile(filePath, bucket_size)

#binary search for start date
left=0
right=len(datesCheck)
while(left<right):
    mid=(left+right)/2
    if(datesCheck[mid]>start_date):
        right=mid
        if(datesCheck[mid-1]<start_date):
            startIndex=mid-1
            break
    elif(datesCheck[mid]<start_date):
        left=mid+1
    startIndex=mid

#binary search for end date
left=0
right=len(datesCheck)
while(left<right):
    mid=(left+right)/2
    if(datesCheck[mid]>end_date):
        right=mid
        if(datesCheck[mid-1]<end_date):
            endIndex=mid-1
            break
    elif(datesCheck[mid]<end_date):
        left=mid+1
    endIndex=mid

#writing the results from buckets into a result file
print("{}.{}".format(startIndex, endIndex))
i = startIndex
if os.path.exists('binarySeachResult.txt'):
  os.remove('binarySeachResult.txt')
output_file = open('binarySeachResult.txt','a')
while(i<=endIndex):
    input_file = open('small_file_{}.txt'.format((i+1)*bucket_size),'r')
    line = input_file.readline()
    while line!="":
        dateStr= line.strip().split(",")
        date = datetime.datetime.strptime(dateStr[0], '%Y-%m-%dT%H:%M:%SZ')
        if(date > start_date and date < end_date):
            output_file.write(dateStr[0]+'\n')
        elif(date > end_date):
            break
        line = input_file.readline()
    input_file.close()
    i+=1
output_file.close()
