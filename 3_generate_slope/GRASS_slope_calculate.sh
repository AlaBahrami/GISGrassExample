#!/bin/bash

# Set input directory
input_directory="/home/baha2501/scratch/GRASS_example/input"
output_directory="/home/baha2501/scratch/GRASS_example/output"

# delete existing elevation file 
if [ -f "$input_directory/elevationlist.csv" ]; then
	rm $input_directory/elevationlist.csv
fi

# Create a CSV file to store a list of elevation data
# Find all _elv.tif files in the directory and write only their filenames to the CSV file
find "$input_directory/elevation/region1" -type f -name "*_elv.tif" -exec basename {} \; > "$input_directory/elevationlist.csv"
echo "Elevation list generated at $input_directory/elevationlist.csv"

# delete existing slope file 
if [ -f "$input_directory/slopelist.csv" ]; then
	rm $input_directory/slopelist.csv
fi  

# Initialize counter for elv_map and slope_map
counter=1
# Loop through each line in elevationlist.csv
while IFS= read -r elevation_file; do
	if [ -f "$input_directory/elevation/region1/$elevation_file" ]; then
		echo "Elevation file exists. Proceeding with processing."
		# Read elevation raster
		r.in.gdal input="$input_directory/elevation/region1/$elevation_file" output="elv_map$counter" --o
	 
		# Generate slope
		g.region raster="elv_map$counter"
		r.slope.aspect elevation="elv_map$counter" slope="slope_map$counter" --o
    
		# Append slope map filename to slopelist.csv
		echo "slope_map$counter" >> "$input_directory/slopelist.csv"
    
		# Increment counter
		((counter++))
	else 
		echo "ERROR: Elevation file does not exist: $input_directory/elevation/region1/$elevation_file"
	fi 
	
done < "$input_directory/elevationlist.csv"

# Build a mosaic as VRT from the generated slope list
r.buildvrt file="$input_directory/slopelist.csv" output="slope_vrt" --o

# read the vector shape file 
v.in.ogr input="$input_directory"/shape/Global_CLASSIC_grid.shp output=ShapeFile --o

# calculate zonal statistics and export the results
g.region raster=slope_vrt
v.rast.stats map=ShapeFile raster=slope_vrt column_prefix=stats method=average percentile=90
v.db.select map=ShapeFile separator=comma file="$output_directory"/Glob_CLASSIC_slope_stat_region1.csv -c --o