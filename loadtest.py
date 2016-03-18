"""
 * Copyright (C) 2015 Agro-Know, Deutsches Forschungszentrum für Künstliche Intelligenz, iMinds,
 * Institut für Angewandte Informatik e. V. an der Universität Leipzig,
 * Istituto Superiore Mario Boella, Tilde, Vistatec, WRIPL (http://freme-project.eu)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

### Author: Jonathan Sauder / jonathan.sauder@student.hpi.de ###

###############################################################################################
### Default Parameters. All except URI can be changed with command line flags			    ###
###############################################################################################
import sys, os
url="http://api-dev.freme-project.eu/current/e-entity/freme-ner/documents?informat=text&outformat=turtle&language=en&dataset=dbpedia&mode=all"
dataset_directory=os.path.abspath(os.path.dirname(__file__))+"/sample_dataset"
print(dataset_directory)
min_threads=1
max_threads=121
step=5
n_files=999999999


###############################################################################################
### Makes sure that correct Python interpreter is used	and imports dependencies		    ###
###############################################################################################
if not sys.version.startswith("3"):
	print("concurrent.futures and urrlib.request libraries only supported in Python 3 and above!")
	sys.exit(1)
import concurrent.futures, urllib.request
import time


###############################################################################################
### Parses Command Line Options - written for readability and not efficiency / eloquence    ###
###############################################################################################
if "-min_threads" in sys.argv:
	try:
		min_threads=int(sys.argv[sys.argv.index("-min_threads")+1])
		max_threads=max(max_threads,min_threads+1)
		assert min_threads>0
	except:
		raise Exception("-min_threads command line flag has to be followed by an integer value greater than 0")
if "-max_threads" in sys.argv:
	try:
		max_threads=int(sys.argv[sys.argv.index("-max_threads")+1])
		assert max_threads>min_threads
	except:
		raise Exception("-max_threads command line flag has to be followed by an integer value greater than min_threads")
if "-step" in sys.argv:
	try:
		step= int(sys.argv[sys.argv.index("-step") + 1])
		assert step > 0, "step must be at least 1"
	except:
		raise Exception("-step command line flag has to be followed by an integer value")
if "-n_files" in sys.argv:
	try:
		n_files= int(sys.argv[sys.argv.index("-n_files")+1])
		assert n_files>0
	except:
		raise Exception("-n_files command line flag has to be followed by an integer value greater than 0")


##############################################################################################
### Reads Dataset and collects statistics about it					    ###
###############################################################################################
dataset=[]
total_size=0
n=0
for textfile in os.listdir(dataset_directory):
	if n<n_files:
		try:
			f= open(dataset_directory+"/"+textfile,'r')
			n+=1
			total_size+=os.path.getsize(dataset_directory+"/"+textfile)
			dataset.append(f.read().encode('utf-8').decode())
		except:
			print("Could not read %s" % textfile)
print("%d Documents are being used in the dataset, totalling %d kb" % (len(dataset), round(total_size/1024)))
print("Average document size is: %f kb" % round((total_size/1024)/len(dataset),3))


###############################################################################################
### Sends dataset to url given above using executor design pattern and writes time taken    ###
###############################################################################################
timetable={}
k=0
for n_threads in range(min_threads, max_threads, step):
	print("Distributing Datasets onto %d threads" % n_threads)
	requests=[urllib.request.Request(url, data=str.encode(textfile), method="POST") for textfile in dataset[k:k+100]]
	hold=dataset[:n_threads]
	dataset=dataset[n_threads:]+hold
	with concurrent.futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
	# Start the load operations and mark each future with its URL
		t_start=time.time()
		future_to_url = {executor.submit(urllib.request.urlopen, req): req for req in requests}
	
		for future in concurrent.futures.as_completed(future_to_url):
			if future.result().status>210:
				print(future.result().status, future.result().reason)
		t_end=time.time()
		t_total=t_end-t_start
		print("t=%f s"%t_total)
		timetable[n_threads]=t_total
	urllib.request.urlcleanup()

##############################################################################################
### Visualizes Load Test results with matplotlib					   ###
##############################################################################################

try:
	font =  {'weight' : 'bold',
		'size' : 19 }
	import matplotlib.pyplot as plt
	plt.grid(True)
	ticks=[]
	v=min(timetable.values())
	while v<=max(timetable.values())+2:
		ticks.append(v)
		v+=0.5
	plt.yticks(ticks)
	plt.xticks(list(timetable.keys()))
	plt.title("FREME Loadtest Result: "+str(time.asctime()),fontdict = font)
	for k,v in timetable.items():
		plt.plot(k,v,'ro')
		plt.ylabel("Total time taken for dataset ("+str(int(total_size/1024))+" kb total) to be processed (in seconds)",fontdict=font)
		plt.xlabel("Number of parallel threads (in executor pattern)",fontdict=font)
	plt.ylim(plt.ylim()[0],plt.ylim()[1]+1)
	plt.xlim(plt.xlim()[0]-1,plt.xlim()[1]+1)
	plt.show()
except:
	print("Matplotlib is not installed - no graph will be shown - only console output\nTo install matplotlib go with \"sudo apt-get install python3-matplotlib\" or \"sudo python3-pip install matplotlib\"")
