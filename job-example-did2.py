#!/usr/bin/env python
#SBATCH --partition=compute
#SBATCH --nodes 1 --ntasks 1 --cpus-per-task=32
#SBATCH --job-name=ex1
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=email@iastate.edu
#SBATCH --signal=TERM@120
#SBATCH --time=7:50:00

import os

parameter_1 = 2
parameter_2 = 3

# in case you want to pass current slurm job_id to the program
# job_id = os.environ.get('SLURM_JOB_ID')

# maybe change to the correct directory to start the job
# print(f"{os.getcwd()}")
# os.chdir('../../')
# print(f"{os.getcwd()}")

# if you run from active conda environment already
os.system('srun -n1 -N1 -c32 --exclusive python example_mp.py %f %f' % (parameter_1, parameter_2) )

# if you want to activate conda environment first
#os.system('source activate environment_name; srun -n1 -N1 -c32 --exclusive python example_mp.py %f %f' % (parameter_1, parameter_2) )

# if you want to use optimized intel compilers and then activate conda environment firest
#os.system('source /shared/intel/bin/compilervars.sh intel64; source /shared/intel/impi/2019.0.117/intel64/bin/mpivars.sh; source activate environment_name; srun -n1 -N1 -c32 --exclusive python example_mp.py %f %f' % (parameter_1, parameter_2) )

# -n1 = --ntasks=1
# -N1 = --nodes=1 =<min_number_nodes>
# -c12 = --cpus-per-task=12