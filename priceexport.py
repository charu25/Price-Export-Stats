import pandas as pd
import csv
import sys
import os
import math
from math import ceil
import operator
filename = "7daystats10%"
list = [ x for x in os.listdir("/home/charu/price-export2") if not x.startswith(".")]
list.sort()

i=0
s={}
m={}
days={}
stat={}
for st in list:
    #st = sys.argv[1]
    df = pd.read_csv("/home/charu/price-export2/"+st,sep="\t")
    f = open("/home/charu/price-export2/"+st,"rb")
    reader = csv.reader(f,delimiter="\t")
    k=[]
    def stats(j):
        for row in reader:
                    content = [row[i] for i in range(20,20+j)]
                    k.append(content)
    stats(15)
    b=['TOTAL','HOST','STORE_ID']
    for value in k[0]:
       b.append(value)
    f.close()

    def analysis():
        count=0
        for row in zip(df[b[0]],df[b[1]],df[b[2]],df[b[3]],df[b[4]],df[b[5]],df[b[6]],df[b[7]],df[b[8]],df[b[9]],df[b[10]],df[b[11]],df[b[12]],df[b[13]],df[b[14]],df[b[15]],df[b[16]]):
                if(count%2 == 0):
                    row1=row
                else:
                    sumOver14Days = reduce(lambda curr,sofar: curr+sofar, (row[i] for i in range(3,17)))
                    sumOver14Days +=reduce(lambda curr,sofar: curr+sofar, (row1[i] for i in range(3,17)))
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

                    if key in days:
                        days[key].append(b[3])
                    else:
                        days[key] = [b[3]]
                count+=1

    analysis()

def stddev(mov_avg):
    total=0
    avg = sum(mov_avg)/len(mov_avg)
    for value in mov_avg:
        total+=(avg-value)**2
    total=total/len(mov_avg)
    return math.sqrt(total)
    
mov_avg=[]
diplist=[]
stablelist=[]
uplist=[]
status=[]
sd_factor=0.1
for key in s:
    mov_avg=[]
    for i in range(0,len(s[key])-6):
        sum7 = reduce(lambda curr,sofar: curr+sofar, (s[key][i] for i in range(i,7+i)))
        sum7=sum7/7.0
        mov_avg.append(sum7)
    if len(mov_avg) > 0:
        sd=sum(mov_avg)/len(mov_avg)
        i=0
        status = []
        for value in s[key]:
            if i <= (len(s[key])-7):
                if(value < mov_avg[i]-sd_factor*mov_avg[i] or mov_avg[i]==0):
                    diplist.append(key)
                    break
                elif (value <= mov_avg[i]+sd_factor*mov_avg[i]):
                    stablelist.append(key)
                    break
                else:
                    if mov_avg[i] != 0:
                        uplist.append(key)
                        break
                    else:
                        diplist.append(key)
                        break
            i+=1
        if mov_avg[i] == 0:
            stat[key] = -100
        else:
            stat[key]=(s[key][i]-mov_avg[i])*100/mov_avg[i]
    else:
        stat[key]=0
    
sort = sorted(stat.iteritems(), key = operator.itemgetter(1))

string="""<html>
<style>
#red{
    background-color:#E92828;
}
#green{
    background-color:#1CE630;
}
#yellow{
    background-color:yellow;
}
</style>
<body>
    <table cellspacing='10'>
    <thead>
        <tr>
            <td>HostName</td>
            <td>Status</td>
            <td>Deviation</td>"""
for i in days["com.microsoft.www:311"]:
    string+="<td width='10px'>"+i+"</td>"
string+="""</tr></thead><tbody>"""
for key in sort:
    key=key[0]
    if key in diplist:
        string+="<tr><td>"+key+"</td><td id='red'>dip</td>"
    elif key in stablelist:
        string+="<tr><td>"+key+"</td><td id='yellow'>Stable</td>"
    elif key in uplist:
        string+="<tr><td>"+key+"</td><td id='green'>Hike</td>"
    else:
        string+="<tr><td>"+key+"</td><td id='yellow'>Stable</td>"
    val = stat[key]
    string+="<td>"+ str(val)+"</td>"
    for value in s[key]:
        string+="<td width='10px'>"+str(value)+"</td>"
    string+="</tr>"
string+="</tbody></table></body></html>"
Html_file=open("/home/charu/"+filename+".html","wb")
Html_file.write(string)
Html_file.close()
keys=[]

#for key in sort:
    #print key[0]

for key in sort:
    key=key[0]
    keys.append(key)
with open('percent'+filename+'.csv', 'wb') as f:
    writer = csv.writer(f,delimiter=',')
    for key in sort:
        key=key[0]
        stat[key]=ceil(stat[key]*1000)/1000.0
        row=[key,stat[key]]
        if key in diplist:
            row.extend(["dip"])
        elif key in stablelist:
            row.extend(["stable"])
        elif key in uplist:
            row.extend(["Hike"])
        else:
            row.extend(["stable"])
        row.extend(s[key])
        writer.writerow(row)


