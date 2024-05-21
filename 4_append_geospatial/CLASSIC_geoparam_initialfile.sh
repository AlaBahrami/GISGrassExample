#!/bin/bash
#SBATCH --account=rpp-kshook
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=5G
#SBATCH --time=00:15:00
#SBATCH --job-name=clgeoinit
#SBATCH --error=errors_clgeoinit
#SBATCH --mail-user=ala.bahrami@usask.ca
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END

# module load 
# load modules
module purge
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3
module load gdal/3.5.1 libspatialindex/1.8.5
module load python/3.8.10 scipy-stack/2022a mpi4py/3.0.3

# create and activate virtual environment
rm -rf $HOME/classic-env
virtualenv --no-download $HOME/classic-env				# create the virtual env for the job
source $HOME/classic-env/bin/activate					# activate the virtual env

pip install --no-index --upgrade pip
pip install --no-index netcdf4
pip install --no-index h5netcdf
pip install --no-index xarray
pip install --no-index geopandas

python CLASSIC_geoparam_initialfile.py 

echo "finished"