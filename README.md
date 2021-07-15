# code_examples
Brief collection of code snippets that implement minimal working examples for various situations of interest.

## List of examples
-  `example_mp.py`: parallel execution of function using python multiprocess package. Includes signal handling when SIGTERM or SIGINT signals are received such that program exits gracefully and automatically restarts (via sbatch).
	- `plot_example.py`: matplotlib script to plot the output of `example_mp.py`
	- `job-example-did2.py`: slurm script to start and restart `example_mp.py` program on AL didymium-2 cluster.