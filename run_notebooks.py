import os
import subprocess

# Set the working directory to the root directory of the project
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Path to the directory containing the notebooks
notebook_dir = "./notebooks"

# Get all notebook files and sort them alphabetically (sequential order based on numbering)
notebooks = sorted([f for f in os.listdir(notebook_dir) if f.endswith(".ipynb")])

# Loop through each notebook in sequential order and execute it
for notebook in notebooks:
    notebook_path = os.path.join(notebook_dir, notebook)
    print(f"Executing {notebook_path}...")
    subprocess.run(["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", notebook_path], check=True)
