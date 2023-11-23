import os

# Get the absolute path of the current script's directory (src)
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate one level up to get the parent directory (the directory containing src and data)
parent_dir = os.path.dirname(current_script_dir)

# Define the path to the data directory
data_directory = os.path.join(parent_dir, 'data')

config = {
    'data_directory': data_directory,
    'new_patients_count': 20,
    # Add more configuration options as needed
}
