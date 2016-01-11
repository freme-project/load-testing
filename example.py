import concurrent.futures
import urllib.request, os, sys
import time
url="http://api-dev.freme-project.eu/current/e-entity/freme-ner/documents?informat=text&outformat=turtle&language=en&dataset=dbpedia&mode=all"
dataset_directory="/home/jonathan/FREME/load-testing/sample_textfiles"
min_threads=1
max_threads=101
increment=2
n_files=3900



###############################################################################################
### Parses Command Line Options - written for readability and not efficiency / eloquence    ###
###############################################################################################
if "-min_threads" in sys.argv:
	try:
		min_threads=int(sys.argv[sys.argv.index("-min_threads")+1])
		max_threads=min_threads+1
		assert min_threads>0
	except:
		raise Exception("-min_threads command line flag has to be followed by an integer value greater than 0")
if "-max_threads" in sys.argv:
	try:
		max_threads=int(sys.argv[sys.argv.index("-max_threads")+1])
		assert max_threads>min_thread
	except:
		raise Exception("-max_threads command line flag has to be followed by an integer value greater than min_threads")
if "-increment" in sys.argv:
	try:
		increment= int(sys.argv[sys.argv.index("-increment")+1])
		assert increment>0, "increment must be at least 1"
	except:
		raise Exception("-increment command line flag has to be followed by an integer value")
if "-n_files" in sys.argv:
	try:
		n_files= int(sys.argv[sys.argv.index("-n_files")+1])
		assert n_files>0
	except:
		raise Exception("-n_files command line flag has to be followed by an integer value greater than 0")





###############################################################################################
### Reads Dataset and collects statistics about it					    ###
###############################################################################################
dataset=[]
total_size=0
n=0
for textfile in os.listdir(dataset_directory):
	if n<n_files:
		try:
			f= open(dataset_directory+"/"+textfile,'r')
			total_size+=os.path.getsize(dataset_directory+"/"+texftile)
			dataset.append(f.read().encode('utf-8').decode())
		except:
			print("could not read %s" % textfile)
print("%d Documents are being used in the dataset, totalling %d bytes" % (len(dataset), n_files))






###############################################################################################
### Sends dataset to url given above using executor design pattern and writes time taken    ###
###############################################################################################
timetable={}
k=0
for n_threads in range(min_threads, max_threads, increment):
	print("Distributing Datasets onto %d threads" % n_threads)
	requests=[urllib.request.Request(url,data=str.encode(textfile),method="POST") for textfile in dataset[k:k+100]]
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
	import matplotlib.pyplot as plt
	for k,v in timetable.items():
		plt.plot(k,v,'ro')
	plt.show()
except:
	print("Matplotlib is not installed - no graph will be shown - only console output\nTo install matplotlib go with \"sudo apt-get install python3-matplotlib\" or \"sudo python3-pip install matplotlib\"")
