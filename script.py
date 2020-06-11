import csv
import re
import datetime
import time
from itertools import islice

def getIndex(startIdx,endIdx):
    input_file = open('largefile.txt','r')
    output_file = open('result.txt','a')
    # line = input_file.readline()
    line = input_file.readline()
    while line!="":
        if(len(line)>1):
            dateStr= line.strip().split(",")
            date = datetime.datetime.strptime(dateStr[0], '%Y-%m-%dT%H:%M:%SZ')

            if(date > startIdx):
                if(date > endIdx):
                    break
                output_file.write(dateStr[0]+'\n')
                print date
        line = input_file.readline()
    output_file.close()
    input_file.close()

def getStartIndex(path,startDate):
    i=1
    flg=0
    with open(path) as f:
        line = list(islice(f, 0, 1))
        while (line!=""):
            try:
                line = list(islice(f, i-1, i))
                dateStr= line[0].strip().split(",")
                date = datetime.datetime.strptime(dateStr[0], '%Y-%m-%dT%H:%M:%SZ')
                if(date<startDate):
                    i=i*2
                elif (date>=startDate):
                    print date
                    #startIndex is between i/2 & i
                    break
            except StopIteration:
                flg=1#startIndex is between i/2 & EOF
                break
        print i
        if(flg==0):
            left=(i+1)/2
            right=i+1
            mid=(left+right)/2
            try:
                line = list(islice(f, 3, 4))
                dateStr= line[0].strip().split(",")
                midDate = datetime.datetime.strptime(dateStr[0], '%Y-%m-%dT%H:%M:%SZ')
                print midDate
                if(midDate<startDate):
                    right=mid
                else:
                    left=mid+1
                mid=(left+right)/2
                line = list(islice(f, mid, mid+1))
            except StopIteration:
                return mid
        else:
            idx=i/2
            try:
                line = list(islice(f, idx, idx+1))
                while(line!=""):
                    dateStr= line[0].strip().split(",")
                    midDate = datetime.datetime.strptime(dateStr[0], '%Y-%m-%dT%H:%M:%SZ')
                    if(midDate>startDate):
                        return idx
                    idx+=1
                    line = list(islice(f, idx, idx+1))
            except StopIteration:
                return idx

datesCheck=[]
idxCheck=[]
def divideFile(inputpath):
    lines_per_file = 200
    smallfile = None
    with open(inputpath) as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                small_filename = 'small_file_{}.txt'.format(lineno + lines_per_file)
                datesCheck.append(datetime.datetime.strptime(line.strip().split(",")[0],'%Y-%m-%dT%H:%M:%SZ'))
                len=lineno
                idxCheck.append(lineno + lines_per_file)
                smallfile = open(small_filename, "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()
    return len



length=divideFile('result2.txt')
start_date_entry = str(raw_input('Enter start dateTime (i.e. 2017,7,1,17,05)'))
end_date_entry = str(raw_input('Enter end dateTime (i.e. 2017,7,1,17,05)'))
start_date = datetime.datetime.strptime(start_date_entry, '%Y,%m,%d,%H,%M')
end_date = datetime.datetime.strptime(end_date_entry, '%Y,%m,%d,%H,%M')

left=0
right=len(datesCheck)


while(left<=right):
    mid=(left+right)/2
    if(datesCheck[mid]>start_date):
        right=mid
        if(datesCheck[mid-1]<start_date):
            startIndex=mid-1
            break
    elif(datesCheck[mid]<start_date):
        left=mid
    else:
        startIndex=mid
left=0
right=len(datesCheck)
while(left<=right):
    mid=(left+right)/2
    if(datesCheck[mid]>end_date):
        right=mid
        if(datesCheck[mid-1]<end_date):
            endIndex=mid-1
            break
    elif(datesCheck[mid]<end_date):
        left=mid
    else:
        endIndex=mid

print "////"
print startIndex
print endIndex
print "////"

i=startIndex
lines_per_file=200
output_file = open('result.txt','a')
while(i<=endIndex):
    input_file= open('small_file_{}.txt'.format((i+1)*lines_per_file),'r')
    line = input_file.readline()
    while line!="":
        dateStr= line.strip().split(",")
        date = datetime.datetime.strptime(dateStr[0], '%Y-%m-%dT%H:%M:%SZ')
        if(date >start_date and date < end_date):
            output_file.write(dateStr[0]+'\n')
        elif(date > end_date):
            break
        line = input_file.readline()
    input_file.close()
    i+=1
output_file.close()




# t0=time.time()
# startIndex = getStartIndex("largefile.txt",start_date)
# print startIndex
# t1=time.time()

# with open('largefile.txt') as f:
#         line = islice(f, startIndex, endIndex)
#         print line
