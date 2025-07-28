import numpy as np
import json
import os

# Define the list of .npy files and corresponding directories
structs = [
    ('vf_30/F30_650.npy', 'inp_files/inp_F30', 'F30'),
    ('vf_30/FA30_650.npy', 'inp_files/inp_FA30', 'FA30'),
    ('vf_30/FAAA30_650.npy', 'inp_files/inp_FAAA30', 'FAAA30'),
    ('vf_30/FC30_650.npy', 'inp_files/inp_FC30', 'FC30'),
    ('vf_30/FCCC30_650.npy', 'inp_files/inp_FCCC30', 'FCCC30'),

    ('vf_40/F40_650.npy', 'inp_files/inp_F40', 'F40'),
    ('vf_40/FA40_650.npy', 'inp_files/inp_FA40', 'FA40'),
    ('vf_40/FAAA40_650.npy', 'inp_files/inp_FAAA40', 'FAAA40'),
    ('vf_40/FC40_650.npy', 'inp_files/inp_FC40', 'FC40'),
    ('vf_40/FCCC40_650.npy', 'inp_files/inp_FCCC40', 'FCCC40'),

    ('vf_50/F50_650.npy', 'inp_files/inp_F50', 'F50'),
    ('vf_50/FA50_650.npy', 'inp_files/inp_FA50', 'FA50'),
    ('vf_50/FAAA50_650.npy', 'inp_files/inp_FAAA50', 'FAAA50'),
    ('vf_50/FC50_650.npy', 'inp_files/inp_FC50', 'FC50'),
    ('vf_50/FCCC50_650.npy', 'inp_files/inp_FCCC50', 'FCCC50')
]

# Domain Size
size = (256, 256)

# Engineering Constants for Matrix Phase
E0 = 3.45e9
P0 = 0.35

# Engineering Constants for Fiber Phase
E1 = 6.50e9
E2 = 6.49e9
E3 = 9.99e10
G12 = 1.99e9
G23 = 2.47e9
G13 = 2.47e9
nu12 = 0.511
nu23 = 0.021
nu13 = 0.021

nu21 = nu12 * E2/E1
nu32 = nu23 * E3/E2
nu31 = nu13 * E3/E1

# Based on Orthotropic Fill on MOOSE
k = 1 - nu12*nu21 - nu23*nu32 - nu31*nu13 - nu12*nu23*nu31 - nu21*nu32*nu13

C1111 = E1*(1-nu23*nu32)/k
C1122 = E1*(nu23*nu31+nu21)/k
C1133 = E1*(nu21*nu32+nu31)/k
C2222 = E2*(1-nu13*nu31)/k
C2233 = E2*(nu12*nu31+nu32)/k
C3333 = E3*(1-nu12*nu21)/k
C2323 = G12
C3131 = G13
C1212 = G23

# print('checking orthotropic stiffness components')
# print(C1111)
# print(C1122)
# print(C1133)
# print(C2222)
# print(C2233)
# print(C3333)
# print(C2323)
# print(C3131)
# print(C1212)

# Read the template file once
with open("linear_elastic_PBC_2D.i", "r") as f:
    base_template = f.read()

# Process each .npy file and structure
for struct_path, directory, outdirectory in structs:
    # Load the .npy file using memory mapping for efficiency
    microstructures = np.load(struct_path, mmap_mode='r')
    print('shape of loaded micros:', microstructures.shape)
    # Process each structure in the file
    for i in range(microstructures.shape[0]):
        arr = microstructures[i]
        # Compute black and white pixel counts
        black_pixels = np.sum(arr == 1)
        white_pixels = np.sum(arr == 0)
        # Compute volume fractions
        volume_fraction_black = black_pixels / (256 * 256)
        volume_fraction_white = white_pixels / (256 * 256)
        print(f"Processing structure {i} in {directory}:")
        print("Volume Fraction of Black Phase:", volume_fraction_black)
        print("Volume Fraction of White Phase:", volume_fraction_white)
        # Prepare subdomain IDs for the template
        nx, ny = arr.shape
        subdomain_ids = "'" + json.dumps(arr.tolist()).replace("[", "").replace("],", "\n").replace("]", "").replace(",", "") + "'"

        # Modify the template with structure-specific values
        customized_template = base_template.replace(r"{{nx}}", str(nx))
        customized_template = customized_template.replace(r"{{ny}}", str(ny))
        customized_template = customized_template.replace(r"{{E0}}", str(E0))
        customized_template = customized_template.replace(r"{{P0}}", str(P0))

        customized_template = customized_template.replace(r"{{C1111}}", str(C1111))
        customized_template = customized_template.replace(r"{{C1122}}", str(C1122))
        customized_template = customized_template.replace(r"{{C1133}}", str(C1133))
        customized_template = customized_template.replace(r"{{C2222}}", str(C2222))
        customized_template = customized_template.replace(r"{{C2233}}", str(C2233))
        customized_template = customized_template.replace(r"{{C3333}}", str(C3333))
        customized_template = customized_template.replace(r"{{C2323}}", str(C2323))
        customized_template = customized_template.replace(r"{{C3131}}", str(C3131))
        customized_template = customized_template.replace(r"{{C1212}}", str(C1212))

        customized_template = customized_template.replace(r"{{base_name}}", f"arr_{i}")
        customized_template = customized_template.replace(r"{{subdomain_ids}}", subdomain_ids)
        customized_template = customized_template.replace(r"{{out_dir}}", outdirectory)
        # Define the output file path for the current structure
        output_file_path = os.path.join(directory, f"arr_{i}.i")

        # Write the customized input file
        with open(output_file_path, "w") as f:
            f.writelines(customized_template)

        print(f"Created {output_file_path}")
