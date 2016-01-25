** FREME LOADTEST **

This repository contains a Python script to test the performance of FREME'S NER Service.

All you need is a Python 3 Installation (it will not work with Python 2)

This is done by sending every text file from the `sample_dataset` directory to the NER Service.
We start with 1 (default) thread (wait for response until we send the next request), and continue upwards.

The following parameters exist:

* `min_threads` : Amount of threads we start with. Must be an integer greater than 0. Defaults to 1
* `max_threads` : Amount of threads we end with. Must be an integer greater than min_threads. Defaults to 101
* `step` : Amount of threads we increase by in every run. Must be an integer greater than 0. Defaults to 5
* `n_files` : Number of text files to use. When not given, will use every text file in `sample_dataset`. Must be an integer greater than 0
* `url` : Url to test against. Can not be changed by command line flag, must be changed in source (`loadtest.py`)
* `dataset_directory` : Path to dataset containing files to test. Defaults to `sample_dataset`. Can not be changed by command line flag, must be changed in source (`loadtest.py`)

Of which the first 4 can be set by command line flags.

** Examples **

To run with all defaults on, simply run:

```

python3 loadtest.py

```

To run, starting with 5 threads, ending with 50 threads, and testing every 10 steps, run:

```

python3 loadtest.py -min_threads 5 -max_threads 50 -step 10

```

This repository also contains a deprecated JMeter Test. Further instructions can be found inside the `jmeter-test` directory.