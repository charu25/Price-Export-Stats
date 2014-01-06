import pandas as pd
import csv
import sys
import os
import math
list = [ x for x in os.listdir("/home/charu/currentstats") if not x.startswith(".")]
list.sort()

i=0
s={}
m={}
for st in list:
    #st = sys.argv[1]
    df = pd.read_csv("/home/charu/currentstats/"+st,sep="\t")
    f = open("/home/charu/currentstats/"+st,"rb")
    reader = csv.reader(f,delimiter="\t")
    k=[]
    def stats(j):
        for row in reader:
                    content = [row[i] for i in range(20,20+j)]
                    k.append(content)
    stats(14)
    b=['TOTAL','HOST','STORE_ID']
    for value in k[0]:
       b.append(value)
    f.close()

    def analysis():
        count=0
        for row in zip(df[b[0]],df[b[1]],df[b[2]],df[b[3]],df[b[4]],df[b[5]],df[b[6]],df[b[7]],df[b[8]],df[b[9]],df[b[10]],df[b[11]],df[b[12]],df[b[13]],df[b[14]],df[b[15]]):
                if(count%2 == 0):
                    row1=row
                else:
                    sumOver14Days = reduce(lambda curr,sofar: curr+sofar, (row[i] for i in range(3,16)))
                    sumOver14Days +=reduce(lambda curr,sofar: curr+sofar, (row1[i] for i in range(3,16)))
                    total = row[0]+row1[0]
                    key = row[1]+str(row[2])
                    if key in s:
                        s[key].append(sumOver14Days)
                    else:
                        s[key] = [sumOver14Days]

                    if key in m:
                        m[key].append(total)
                    else:
                        m[key] = [total]
                count+=1

    analysis()
