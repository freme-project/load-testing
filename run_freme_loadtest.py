from __future__ import division
import math

#Parameters
min_threads=5
max_threads=110
increment=5
jmxfile="freme.jmx"
csvfile="results.csv"
composedlog="composed_summary_reports"
dataset="sample_textfiles"
#Imports, attempts to import matplotlib(plotting library)
import csv, sys,os
plot=False

try:
    import matplotlib.pyplot as plt
    plot=True
except:
    print("Matplotlib not installed, will not plot runtimes")

#Removes previous csv and composed-log file
os.system("rm "+csvfile)
os.system("rm "+composedlog)

#Runs jmeter with variable amount of threads, saves output as csv and append generate report to composedlog
n_docs=len(os.listdir(dataset))
k=0
for i in range(min_threads,max_threads,increment):
    os.system("jmeter -n -t "+jmxfile+ " -J n_threads="+str(i)+ " -J output_csv_name="+csvfile+" -J start_index="+str(k)+" -p freme-loadtest.properties")
    with open("jmeter.log","r") as f:
        report=f.readlines()[-1][:-1]
    os.system("echo \""+report+"\" >> "+composedlog)
    k+=i
    k%=n_docs

#Parses result
with open(csvfile,'r') as csvfile:
    table=[x for x in csv.DictReader(csvfile)]

#Helper function for getting throughput from Summary report in Composedlog
get_throughput=lambda x:float(x[x.rfind("=")+1:x.find("/s")].strip().rstrip())

#Calculates and reads summary report
k=0
results=[]
with open(composedlog,"r") as comp_log:
	throughputs=[get_throughput(line) for line in comp_log.readlines()]
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
    throughput= throughputs[k]
    k+=1
    
    #kb / sec = avg_kb * throughput
    kb_sec=(kb_avg/1024)*throughput
    
    std_dev=math.sqrt(sum([(x*x)-t_avg for x in t])/n)
    
    results.append([n,t_avg,kb_avg,total_time_taken,throughput,time_per_request,std_dev])

if plot:
    titles=["Average Response time per Request (ms)","Average Size of Response (bytes)", "Total time taken for all requests (ms)","Throughput (requests/second)","Total time taken for all requests/ number of parallel requests","Standard Deviation"]
    fig=plt.figure()
    for e in range(6):
        num=230+(e+1)
        print num
        print e
        ax=fig.add_subplot(num)
        for r in results: 
            ax.set_ylabel(titles[e])
            ax.set_xlabel("Number of parallel requests")
            ax.plot(r[0],r[e+1],'ro')
    plt.show()
