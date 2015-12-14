**Step 1: Install jmeter**

```sudo apt-get install jmeter``` or download the jar [here](https://jmeter.apache.org/download_jmeter.cgi)

**Step 2: Run jmeter**

This command opens the FREME jmeter test plan
```jmeter -t freme.jmx```

In the GUI, you can run the test plan by clicking on the green play button.
Results are shown in the Summary Report, individual requests and responses in the View Results Tree

This command runs the FREME jmeter test plan without the jmeter GUI:
```jmeter -n -t freme.jmx```

This command runs the FREME jmeter test plan without the jmeter GUI and overrides the default number of threads and the default name of the resulting .csv file:
```jmeter -n -t freme-jmx -J n_threads=30 -J output_csv_file=fremeresults.csv```

Possible parameters are:
- n_threads: number of simulataneous requests that will be made to the api, default: 50
- output_csv_name: name of csv file in which jmeter logs results, default: results.csv
- start_index: index of text documents to start parsing in /sample_textfiles/, needed to avoid scewed results due to caching, default:0

**/sample_textfiles/**

The sample textfiles in this folder each are 30 lines of the English classics "Frankenstein" by Mary Shelley and "The Adventures of Sherlock Holmes" by Arthur Conan Doyle.

**run_freme_loadtest.py to run with various amounts of threads**

This is a python script that runs jmeter with increasing amount of threads. The start_index parameter is chosen so that caching does not scew results.
At the top you can choose some parameters.
The script then parses the resulting .csv file from jmeter and calculates the average elapsed time for each request for each number of threads.
If it could import matplotlib (plotting library), it will visualize the results.
