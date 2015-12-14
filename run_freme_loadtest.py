from __future__ import division
import math
#Parameter
min_threads=1
max_threads=110
increment=5
jmxfile="freme.jmx"
csvfile="results.csv"
#Imports, attempts to import matplotlib(plotting library)
import csv, sys,os
plot=False

try:
    import matplotlib.pyplot as plt
    plot=True
except:
    print("Matplotlib not installed, will not plot runtimes")

#Removes previous csv file
os.system("rm "+csvfile)

#Runs jmeter with variable amount of threads
k=0
for n in range(min_threads,max_threads,increment):
    os.system("jmeter -n -t "+jmxfile+ " -J n_threads="+str(i)+ " -J output_csv_name="+csvfile+" -J start_index="+str(k))
    k+=i
    k%=654

import csv
#Parses result
with open(csvfile,'r') as csvfile:
    table=[x for x in csv.DictReader(csvfile)]

#Calculates 
results=[]
for n in range(min_threads,max_threads,increment):
    current=table[:n]
    #t = elapsed times for each request
    t=[int(line['elapsed']) for line in current]
    
    #ts = timestamps of when each request was sent
    ts=[int(line['timeStamp']) for line in current]
    
    #kb = bytes of each request
    kb=[int(line['bytes']) for line in current]
    
    #t_avg = average elapsed time (average of t)
    t_avg=sum(t)/n
    
    #kb_avg = average bytes
    kb_avg=sum(kb)/n
    
    #total_time_taken=max(t+ts)-min(ts)
    total_time_taken=max([t[x]+ts[x] for x in range(n)])-min(ts)
    
    #time_per_request=total_time_taken/n
    time_per_request=total_time_taken/n
    
    #throughput = (n / total_time_taken)*1000
    throughput= (n / total_time_taken)*1000
    
    #kb / sec = avg_kb * throughput
    kb_sec=(kb_avg/1024)*throughput
    
    std_dev=math.sqrt(sum([(x*x)-t_avg for x in t])/n)
    
    results.append([n,t_avg,kb_avg,time_per_request,throughput,kb_sec,std_dev])

if plot:
    colors="rgbycmk"
    titles=["Average Time per Request (ms)","Average Size of Request (bytes)", "Total time per Request (ms)","Throughput (requests/second)","kb/sec","Standard Deviation"]
    fig=plt.figure()
    for e in range(6):
        num=(200)+30+(e+1)
        print num
        print e
        plt.subplot(num)
        for r in results:
            
            plt.title(titles[e])
            plt.plot(r[0],r[e+1],'ro')
    plt.show()
