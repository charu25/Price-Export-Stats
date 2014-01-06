import pandas as pd
import csv
import sys
import os
import math
list = [ x for x in os.listdir("PATH") if not x.startswith(".")]
list.sort()

i=0
s={}
m={}
days={}
stat={}
for st in list:
    #st = sys.argv[1]
    df = pd.read_csv("PATH"+st,sep="\t")
    f = open("PATH"+st,"rb")
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

def stddev(sums):
    total=0
    avg = sum(sums)/len(sums)
    for value in sums:
        total+=(avg-value)**2
    total=total/len(sums)
    return math.sqrt(total)
    
sums=[]
diplist=[]
stablelist=[]
uplist=[]
status=[]
sd_factor=0.1
for key in s:
    sums=[]
    for i in range(0,len(s[key])-6):
        sum7 = reduce(lambda curr,sofar: curr+sofar, (s[key][i] for i in range(i,7+i)))
        sum7=sum7/7.0
        sums.append(sum7)
    if len(sums) > 0:
        sd=sum(sums)/len(sums)
        i=0
        status = []
        for value in s[key]:
            if i <= (len(s[key])-7):
                if(value < sums[i]-sd_factor*sums[i]):
                    diplist.append(key)
                    break
                elif (value < sums[i]+sd_factor*sums[i]):
                    stablelist.append(key)
                    break
                else:
                    uplist.append(key)
                    break
            i+=1
        stat[key]=math.fabs(s[key][0]-sums[0])*100/s[key][0]
    else:
        stat[key]=0
       
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
for key in s:
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
Html_file=open("PATH","wb")
Html_file.write(string)
Html_file.close()


