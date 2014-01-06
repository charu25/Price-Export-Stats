import pandas as pd
import csv
import sys
import os
import math
list = [ x for x in os.listdir("REPLACE_PATH") if not x.startswith(".")]
list.sort()

i=0
s={}
for st in list:
    #st = sys.argv[1]
    df = pd.read_csv("REPLACE_PATH"+st,sep="\t")

    b=['TOTAL','HOST','STORE_ID']
    def analysis():
        count=0
        for row in zip(df[b[0]],df[b[1]],df[b[2]]):
                if(count%2 == 0):
                    row1=row
                else:
                    total = row[0]+row1[0]
                    key = row[1]+str(row[2])
                    if key in s:
                        s[key].append(total)
                    else:
                        s[key] = [total]
                count+=1

    analysis()

def stddev(sums):
    total=0
    avg = sum(sums)/len(sums)
    for value in sums:
        total+=(avg-value)**2
    total=total/len(sums)
    return math.sqrt(total)
    
sums=[]
Hostlist=[]
sd_error_factor = 1.5
for key in s:
    sums=[]
    for i in range(0,len(s[key])-6):
        sum7 = reduce(lambda curr,sofar: curr+sofar, (s[key][i] for i in range(i,7+i)))
        sum7=sum7/7.0
        sums.append(sum7)
    if len(sums) > 0:
        sd=stddev(sums)
        i=0
        for value in s[key]:
            if i <= (len(s[key])-7):
                if(math.fabs(value-sums[i])< sd_error_factor * sd):
                    Hostlist.append(key)
                    break
            i+=1

# Displays hosts which show product dip
print Hostlist
print "\n"
print len(Hostlist)