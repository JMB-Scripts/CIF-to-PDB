# CIF to PDB 
#
# The script will convert in a batch mode CIF files in a folder to PDB in outputs_pdbs,
# 
## Requirements
# - Python 3.x
#
## Python packages:
# - Open Babel
#
# conda install openbabel
#
## USAGE 
#
# python script_name.py path_to_CIFS_files_FOLDER/
#
# 2023 Jean-Marie Bourhis 

import os
import pdb
import subprocess
import sys
from tqdm import tqdm

# Define the input and output directories
output_pdb_directory = "output_pdbs/"

# Check if the command line arguments are provided correctly
if len(sys.argv) < 2:
    print("Please provide the necessary arguments: script_name.py Cifs_files-Folder/")
    sys.exit(1)
    
# Path to the sequence 
input_cif_directory = str(sys.argv[1])

# Create output and temporary directories if they don't exist
os.makedirs(output_pdb_directory, exist_ok=True)

# Get a list of CIF files in the input directory and sort them
cif_files = [f for f in os.listdir(input_cif_directory) if f.endswith(".cif")]
cif_files.sort()  # Sort alphabetically

# Wrap the loop with tqdm to add a progress bar
for cif_file in tqdm(cif_files, desc="Converting files"):
    cif_path = os.path.join(input_cif_directory, cif_file)
    pdb_file = cif_file.replace(".cif", ".pdb")
    pdb_path = os.path.join(output_pdb_directory, pdb_file)

    # Convert CIF to PDB using Open Babel
    obabel_command = ["obabel", cif_path, "-O", pdb_path]
    with open(os.devnull, 'w') as devnull:
        subprocess.run(obabel_command, stdout=devnull, stderr=devnull)

      # Remove headers using awk
    awk_command = ["awk", '/^ATOM |^TER/']
    with open(os.path.join(output_pdb_directory, pdb_file), "rb") as input_file:
        awk_process = subprocess.run(awk_command, stdin=input_file, stdout=subprocess.PIPE, text=True)
        tmp2_content = awk_process.stdout

    with open(os.path.join(output_pdb_directory, pdb_file), "w") as tmp2_file:
        tmp2_file.write(tmp2_content)

print("Conversion complete.")
