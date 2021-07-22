import numpy as np
from numpy import linalg as la
import scipy as sc
import h5py
import multiprocess as mp
import sys
import signal
from functools import partial
from pathlib import Path
import os

def init_records():
	records = {
	'variable_1' : [],
	'observable' : []
	}
	return records

def init_records_temporary():
	records_temporary = {
	'variable_1' : [],
	'variable_1_idx' : [],
	'observable' : [],
	}
	return records_temporary

def combine_records(records_final, records_temporary):
	records_final["variable_1"] = records_temporary["variable_1"]
	records_final["observable"] = records_temporary["observable"]
	return records_final

def write_records(h5_file_path, path, records):
    with h5py.File(f"{h5_file_path}/output_example.h5", "a") as f:
        if path in f: # delete same path if exist
            del f[path]
        for key, val in records.items():
            f[f"{path}/{key}"] = val

def write_records_temporary(h5_file_location, path, records):
	with h5py.File(f"{h5_file_path}/output_example_temporary.h5", "a") as f:
		if path in f:
			del f[path]
		for key, val in records.items():
			f[f"{path}/{key}"] = val

def compute_observables(variable_1, parameter_1, parameter_2):
	observable = parameter_1 + parameter_2*variable_1
	return variable_1, observable

if __name__ == "__main__":
	# specify parameters of simulation

	# default values
	parameter_1 = 1.
	parameter_2 = 2.
	variable_1_steps = 5

	variable_1_init = 0.
	variable_1_final = 1.


	# read in values from shell (if provided). May be generalized to read in other parameters such as initial and final values of variable_1 if needed
	if len(sys.argv) == 4:
		parameter_1 = float(sys.argv[1])
		parameter_2 = float(sys.argv[2])
		variable_1_steps = int(sys.argv[3])

	# check whether temporary output file exists from previous calculation and read in results
	h5_file_location = "."
	h5_group = "Output"
	h5_file_path = Path(f"{h5_file_location}")
	h5_temporary_filename = Path(f"{h5_file_location}/output_example_temporary.h5")

	if h5_temporary_filename.is_file():
		print(f"Found temporary output: will read in file.")
		print(f"Open file {h5_temporary_filename}")
		f = h5py.File(h5_temporary_filename, 'r')
		print(f"File {h5_temporary_filename} opened successfully")
		print(f"Keys in temporary h5 file = {f.keys()}")
		# initialize empty list with temporary records that were previously saved to file
		records_temporary = init_records_temporary()
		# load temporary results from file into dictionary records_temporary
		records_temporary["variable_1"] = f[f"/{h5_group}/variable_1"][()]
		records_temporary["variable_1_idx"] = f[f"/{h5_group}/variable_1_idx"][()]
		records_temporary["observable"] = f[f"/{h5_group}/observable"][()]

		print(f"records_temporary = {records_temporary}")
		# find final variable_1 of interrupted calculation and restart from there
		variable_1_init = records_temporary["variable_1"][-1]
		print(f"variable_1_init = {variable_1_init}")
	else:
		records_temporary = init_records_temporary()

		variable_1_table = np.linspace(variable_1_init, variable_1_final, variable_1_steps - len(records_temporary["variable_1"]))
		print(f"variable_1_table = {variable_1_table}")

	compute_observables_variable_1 = partial(compute_observables, parameter_1 = parameter_1, parameter_2 = parameter_2)
	print(f"observable[0.1] = {compute_observables_variable_1(0.1)}")

	# define callback function that worker in pool appends result to records_temporary
	def collect_results(result):
		records_temporary["variable_1"].append(result[0])
		records_temporary["observable"].append(result[1])

	# pool size = number of CPUs available
	count_workers = mp.cpu_count()
	print(f"count_workers = {count_workers}")

	# translate SIGTERM signal received into KeyboardInterrupt
	def sigterm_handler(signal_received, frame):
	    raise KeyboardInterrupt("SIGTERM received")

	signal.signal(signal.SIGTERM, sigterm_handler)

	# make pool workers ignore signals so that it is only processed by the main thread (who is responsible for gracefully exiting procedure)
	def init_worker():
	    signal.signal(signal.SIGINT, signal.SIG_IGN)

	with mp.Pool(count_workers, init_worker) as pool:
		try:
			# for a single for loop the res.get method works. If you have multiple for loops and want to wait for all inner loop jobs to finish, setting up the res_table is necessary, if you want to process the results of the inner for loop before moving on the iteration of the outer for loop
			#res_table = []
			for idx_1, variable_1 in enumerate(variable_1_table):
				res = pool.apply_async(compute_observables_variable_1, (variable_1,), callback=collect_results)
				res.get(9999999)
				#res_table.append(res)
			#[result.wait() for result in res_table]

		except KeyboardInterrupt:
			print("Caught KeyboardInterrupt, terminating workers")
			print("Will now save current state of program into h5py file.")
			if not h5_file_path.is_dir():
				h5_file_path.mkdir(parents = True, exist_ok = True)
			write_records_terminated(h5_file_location, h5_group, records_temporary)
			print(f"Writing temporary output file {h5_temporary_filename} completed.")
			pool.terminate()
			pool.join()
			print(f"{os.getcwd()}")
			os.chdir(h5_file_location)
			print(f"{os.getcwd()}")
			os.system(f'sbatch job-did2.py') # restart the job on the cluster
			raise OSError("Process terminated externally.")
		else:
			print(f"Normal termination")
			pool.close()
		pool.join()


	# before collecting all results: initialize final records, which stores complete output
	print(f"Parallel calculation finished.")
	# write records to final records variable
	records_final = init_records()
	print(f"Start combining results and write to final records variable.")
	combine_records(records_final, records_temporary)
	print(f"records_temporary = {records_temporary}")
	print(f"records_final = {records_final}")

	if not h5_file_path.is_dir():
	    h5_file_path.mkdir(parents = True, exist_ok = True)
	print(f"Output final results into h5py file: {h5_file_location}/output_example.h5.")
	write_records(h5_file_location, "/Output/", records_final)
	print(f"Successfully written final output file!")
	os.chdir(h5_file_location)

	print(f"Normal exit now.")

