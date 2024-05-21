# -*- coding: utf-8 -*-
#Created on Thu May  9 15:49:56 2024

#@author: Ala Bahrami

# the purpose of this program is to download list of Merit Hydro DEM files, 
#unzip them and place them in a specified folder,

import requests
import os
import shutil
import tarfile

def download_file(url, username, password, save_path):
    # Create a session to handle authentication
    session = requests.Session()
    session.auth = (username, password)

    # Send a GET request to the URL
    response = session.get(url, stream=True)

    # Check if request was successful
    if response.status_code == 200:
        # Open a file for writing in binary mode
        with open(save_path, 'wb') as f:
            # Write chunks of the content received
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print("Failed to download file from", url)

def unzip_file(file_path, extract_to):
    # Extract the contents of the TAR file
    with tarfile.open(file_path, 'r') as tar:
        tar.extractall(extract_to)

def move_files(source_dir, destination_dir):
    # Move files from source directory to destination directory
    for file_name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, file_name)
        destination_path = os.path.join(destination_dir, file_name)
        shutil.move(source_path, destination_path)

def main():
    # URL of the folder containing the files
    folder_url = "http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_Hydro/distribute/v1.0/"

    # Files for each region
    regions = {
        "region1": ["elv_n30w120", "elv_n30w150", "elv_n30w180", "elv_n60w120", "elv_n60w150", "elv_n60w180"],
        "region2": ["elv_n60w090", "elv_n60w060", "elv_n60w030", "elv_n30w090", "elv_n30w060", "elv_n30w030"],
        "region3": ["elv_n00w120", "elv_n00w180", "elv_s30w120", "elv_s30w150", "elv_s30w180"],
        "region4": ["elv_n00w030", "elv_n00w060", "elv_n00w090", "elv_s30w030", "elv_s30w060", "elv_s30w090"],
        "region5": ["elv_s60w180", "elv_s60w090", "elv_s60w060", "elv_s60w030"],
        "region6": ["elv_n30e000", "elv_n30e030", "elv_n30e060", "elv_n60e000", "elv_n60e030", "elv_n60e060"],
        "region7": ["elv_n30e090", "elv_n30e120", "elv_n30e150", "elv_n60e090", "elv_n60e120", "elv_n60e150"],
        "region8": ["elv_s30e060", "elv_s30e030", "elv_s30e000", "elv_n00e060", "elv_n00e030", "elv_n00e000"],
        "region9": ["elv_s30e150", "elv_s30e120", "elv_s30e090", "elv_n00e150", "elv_n00e120", "elv_n00e090"],
        "region10": ["elv_s60e000", "elv_s60e030", "elv_s60e060", "elv_s60e090", "elv_s60e120", "elv_s60e150"]
    }

    # Credentials for authentication
    username = "hydrography"
    password = "rivernetwork"

    # Directory to save downloaded files
    save_dir = "/scratch/baha2501/GRASS_example/input/elevation"

    for region, files in regions.items():
        # Create directory for this region
        region_dir = os.path.join(save_dir, region)
        if not os.path.exists(region_dir):
            os.makedirs(region_dir)

        for file in files:
            # Construct the full URL
            file_url = folder_url + file + ".tar"

            # Path to save the downloaded file
            save_path = os.path.join(region_dir, file + ".tar")

            # Download the file
            download_file(file_url, username, password, save_path)

            # Unzip the file
            unzip_file(save_path, region_dir)

            # Remove the source .tar file
            os.remove(save_path)

        # Move files from subdirectories to main directory
        for subdir in os.listdir(region_dir):
            subdir_path = os.path.join(region_dir, subdir)
            if os.path.isdir(subdir_path):
                move_files(subdir_path, region_dir)
                shutil.rmtree(subdir_path)

if __name__ == "__main__":
    main()