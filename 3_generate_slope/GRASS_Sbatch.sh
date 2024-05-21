#!/bin/bash
#SBATCH --account=rpp-kshook 
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=80G
#SBATCH --time=10:00:00
#SBATCH --job-name=grsl
#SBATCH --error=errors_grsl
#SBATCH --mail-user=ala.bahrami@usask.ca
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END

# Reference 
# https://grasswiki.osgeo.org/wiki/GRASS_and_Shell#GRASS_Batch_jobs

#### 1) PREPARATION
# module load 
module purge
module load StdEnv/2020 gcc/9.3.0
module load grass/7.8.4
#module load grass/8.2.1

### Note : If we want to load GRASS from apptainer 
# module load apptainer
# export APPTAINER_CACHEDIR=$(pwd) 						# currecnt directory
# rm -rf *.sif cache/
# apptainer pull docker://osgeo/grass-gis:releasebranch_8_3-debian
# apptainer run grass-gis_releasebranch_8_3-debian.sif
# rm -rf GISDATA/ 										# remove possible GISDATA 
# grass -c EPSG:4326 GISDATA 							#create possible GISDATA and start a grass session
####

# create a directory (may be elsewhere) to hold the location used for processing
mkdir -p grassdata

# create new temporary location for the job, exit after creation of this location
grass78 -c epsg:4326 grassdata/temp -e

#### 2) USING THE BATCH JOB
# define job file as environmental variable
export GRASS_BATCH_JOB=./GRASS_slope_calculate.sh

# now we can use this new location and run the job defined via GRASS_BATCH_JOB
grass78 grassdata/temp/PERMANENT

#### 3) CLEANUP
# switch back to interactive mode, for the next GRASS GIS session
unset GRASS_BATCH_JOB

# delete temporary location (consider to export results first in your batch job)
rm -rf grassdata/temp

